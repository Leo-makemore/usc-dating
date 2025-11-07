"""
Main FastAPI application.
Defines all API routes and endpoints.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from database import get_db, engine, Base
from models import User, DateRequest, Event, EventAttendee, Message
from schemas import (
    UserCreate, UserResponse, UserUpdate, UserLogin, Token,
    UserRegisterStep1, UserRegisterStep2, EmailOnly, GoogleAuthRequest,
    DateRequestCreate, DateRequestResponse, DateRequestUpdate,
    EventCreate, EventResponse, EventUpdate, EventRSVP,
    MessageCreate, MessageResponse, MatchResponse, VerificationRequest
)
from auth import get_password_hash, verify_password, create_access_token
from dependencies import get_current_user, get_current_verified_user
from email_service import generate_verification_token, send_verification_email, get_verification_token_expiry
from matching import get_recommended_matches
from google_auth import verify_google_token, validate_usc_email
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="University Dating App API",
    description="Backend API for university-exclusive dating app",
    version="1.0.0"
)

# Configure CORS
# Allow common Vite dev server ports
allowed_origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:5176",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== AUTHENTICATION ROUTES ====================

@app.post("/api/auth/google", response_model=dict)
async def google_auth(auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Authenticate with Google OAuth.
    Verifies the Google token and checks if email is @usc.edu.
    Creates or logs in user.
    """
    try:
        print(f"[GOOGLE AUTH] Received token, length: {len(auth_data.token) if auth_data.token else 0}")
        print(f"[GOOGLE AUTH] GOOGLE_CLIENT_ID configured: {bool(settings.GOOGLE_CLIENT_ID)}")
        
        # Verify Google token
        google_user = verify_google_token(auth_data.token)
        
        if not google_user:
            print("[GOOGLE AUTH] Token verification returned None")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token. Please check backend logs for details."
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[GOOGLE AUTH] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )
    
    print(f"[GOOGLE AUTH] Token verified successfully. Email: {google_user.get('email')}")
    
    email = google_user.get('email')
    if not email:
        print("[GOOGLE AUTH] No email found in token")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not found in Google account"
        )
    
    print(f"[GOOGLE AUTH] Validating email: {email}")
    
    # Validate USC email
    if not validate_usc_email(email):
        print(f"[GOOGLE AUTH] Email validation failed: {email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only USC students (@usc.edu) are allowed to register. Your email ({email}) is not a USC email."
        )
    
    print(f"[GOOGLE AUTH] Email validated: {email}")
    
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Existing user - login
        # Mark as verified if not already
        if not user.is_verified:
            user.is_verified = True
        
        # Update avatar if available
        if google_user.get('picture') and not user.avatar_url:
            user.avatar_url = google_user.get('picture')
        
        db.commit()
        db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "profile_completed": user.profile_completed
            },
            "is_new_user": False
        }
    else:
        # New user - create account
        verification_token = generate_verification_token()
        
        # Extract school name
        school_name = "University of Southern California"
        
        # Generate a random password (user won't need it with Google OAuth)
        temp_password = generate_verification_token()
        
        new_user = User(
            email=email,
            password_hash=get_password_hash(temp_password),
            name=google_user.get('name', ''),  # Use Google name if available
            school=school_name,
            year="",  # Will be filled in step 2
            interests=[],
            avatar_url=google_user.get('picture'),
            is_verified=True,  # Google OAuth already verifies email
            profile_completed=False,
            verification_token=verification_token,
            verification_token_expires=get_verification_token_expiry()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create temporary token for profile completion (expires in 1 hour)
        temp_token = create_access_token(
            data={"sub": new_user.id, "step": "register_step2"},
            expires_delta=timedelta(hours=1)
        )
        
        # Create access token for immediate login
        access_token = create_access_token(data={"sub": new_user.id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "temp_token": temp_token,  # For profile completion
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name,
                "profile_completed": new_user.profile_completed
            },
            "is_new_user": True,
            "needs_profile": True
        }


@app.get("/api/auth/check-school")
async def check_school(email: str):
    """
    Check if email belongs to a known school and return school info.
    Used for school-specific login redirects.
    """
    if not email or "@" not in email:
        return {"has_school_login": False}
    
    domain = email.split("@")[1].lower()
    
    # Known schools with custom login pages
    school_configs = {
        "usc.edu": {
            "has_school_login": True,
            "school_name": "University of Southern California",
            "login_url": "https://shibboleth.usc.edu/idp/profile/SAML2/Redirect/SSO",
            "school_domain": "usc.edu"
        },
        "ucla.edu": {
            "has_school_login": True,
            "school_name": "University of California, Los Angeles",
            "login_url": "https://login.ucla.edu/cas/login",
            "school_domain": "ucla.edu"
        },
        "berkeley.edu": {
            "has_school_login": True,
            "school_name": "University of California, Berkeley",
            "login_url": "https://auth.berkeley.edu/cas/login",
            "school_domain": "berkeley.edu"
        }
    }
    
    if domain in school_configs:
        return school_configs[domain]
    
    # Generic .edu domain
    if domain.endswith(".edu"):
        return {
            "has_school_login": False,
            "school_domain": domain,
            "message": "Generic university email"
        }
    
    return {"has_school_login": False, "error": "Not a university email"}


@app.post("/api/auth/register-with-email", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_with_email(email_data: EmailOnly, db: Session = Depends(get_db)):
    """
    Registration with email only (for SSO flow).
    Creates a temporary account that will be completed after SSO authentication.
    """
    email = email_data.email
    
    # Validate university email
    if not email.endswith(".edu"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only university email addresses (.edu domain) are allowed"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Extract school name from email domain
    email_domain = email.split("@")[1].lower()
    school_name = "University of Southern California" if email_domain == "usc.edu" else "University"
    
    # Create new user with minimal info (no password for SSO flow)
    verification_token = generate_verification_token()
    
    # Generate a temporary password hash (will be updated after SSO verification)
    temp_password = generate_verification_token()  # Use token as temp password
    
    new_user = User(
        email=email,
        password_hash=get_password_hash(temp_password),  # Temporary password
        name="",  # Will be filled in step 2
        school=school_name,
        year="",  # Will be filled in step 2
        interests=[],
        is_verified=False,  # Will be verified after SSO
        profile_completed=False,
        verification_token=verification_token,
        verification_token_expires=get_verification_token_expiry()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create temporary token for step 2 (expires in 1 hour)
    temp_token = create_access_token(
        data={"sub": new_user.id, "step": "register_step2"},
        expires_delta=timedelta(hours=1)
    )
    
    return {
        "user_id": new_user.id,
        "temp_token": temp_token,
        "message": "Account created. Please complete your profile."
    }


@app.post("/api/auth/register-step1", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_step1(user_data: UserRegisterStep1, db: Session = Depends(get_db)):
    """
    Registration step 1: Create account with email and password only.
    Returns a temporary token for step 2.
    """
    # Validate university email
    if not user_data.email.endswith(".edu"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only university email addresses (.edu domain) are allowed"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with minimal info
    verification_token = generate_verification_token()
    
    # Extract school name from email domain
    email_domain = user_data.email.split("@")[1].lower()
    school_name = "University of Southern California" if email_domain == "usc.edu" else "University"
    
    new_user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        name="",  # Will be filled in step 2
        school=school_name,
        year="",  # Will be filled in step 2
        interests=[],
        is_verified=False,
        profile_completed=False,
        verification_token=verification_token,
        verification_token_expires=get_verification_token_expiry()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create temporary token for step 2 (expires in 1 hour)
    temp_token = create_access_token(
        data={"sub": new_user.id, "step": "register_step2"},
        expires_delta=timedelta(hours=1)
    )
    
    return {
        "user_id": new_user.id,
        "temp_token": temp_token,
        "message": "Step 1 completed. Please complete your profile."
    }


@app.post("/api/auth/register-step2", response_model=dict, status_code=status.HTTP_200_OK)
async def register_step2(
    user_data: UserRegisterStep2,
    db: Session = Depends(get_db),
    authorization: str = Header(None, alias="Authorization")
):
    """
    Registration step 2: Complete profile with personal information.
    Requires temp_token from step 1 in Authorization header.
    """
    from fastapi import Header
    from auth import decode_access_token
    
    # Get token from Authorization header
    if authorization and authorization.startswith("Bearer "):
        temp_token = authorization.split(" ")[1]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization token"
        )
    
    # Verify temp token
    print(f"[REGISTER STEP2] Attempting to decode token: {temp_token[:30]}...")
    payload = decode_access_token(temp_token)
    if not payload:
        print(f"[REGISTER STEP2] Token decode failed. Token length: {len(temp_token)}")
        print(f"[REGISTER STEP2] SECRET_KEY configured: {bool(settings.SECRET_KEY)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired registration token. Please try registering again."
        )
    
    print(f"[REGISTER STEP2] Token decoded successfully. Payload: {payload}")
    
    if payload.get("step") != "register_step2":
        print(f"[REGISTER STEP2] Token step mismatch. Expected 'register_step2', got: {payload.get('step')}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid registration token. Please try registering again."
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user with profile information
    user.name = user_data.name
    user.school = user_data.school
    user.year = user_data.year
    user.interests = user_data.interests or []
    user.height_cm = user_data.height_cm
    user.weight_kg = user_data.weight_kg
    user.nationality = user_data.nationality
    user.ethnicity = user_data.ethnicity
    user.photos = user_data.photos or []
    user.profile_completed = True
    
    db.commit()
    db.refresh(user)
    
    # Send verification email
    send_verification_email(user.email, user.verification_token, user.name)
    
    # Create access token for immediate login
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "profile_completed": user.profile_completed
        }
    }


@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Validates university email domain (.edu) and sends verification email.
    """
    # Validate university email
    if not user_data.email.endswith(".edu"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only university email addresses (.edu domain) are allowed"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    verification_token = generate_verification_token()
    new_user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        name=user_data.name,
        school=user_data.school,
        year=user_data.year,
        interests=user_data.interests or [],
        height_cm=user_data.height_cm,
        weight_kg=user_data.weight_kg,
        nationality=user_data.nationality,
        ethnicity=user_data.ethnicity,
        photos=user_data.photos or [],
        profile_completed=True,
        is_verified=False,
        verification_token=verification_token,
        verification_token_expires=get_verification_token_expiry()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send verification email
    send_verification_email(new_user.email, verification_token, new_user.name)
    
    return new_user


@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    Uses OAuth2PasswordRequestForm for compatibility with frontend.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/auth/verify-email", response_model=dict)
async def verify_email(verification: VerificationRequest, db: Session = Depends(get_db)):
    """
    Verify user email using verification token.
    """
    user = db.query(User).filter(User.verification_token == verification.token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
    
    if user.verification_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Mark user as verified
    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    
    db.commit()
    
    return {"message": "Email verified successfully"}


# ==================== USER ROUTES ====================

@app.get("/api/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's information."""
    return current_user


@app.put("/api/users/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.school is not None:
        current_user.school = user_update.school
    if user_update.year is not None:
        current_user.year = user_update.year
    if user_update.interests is not None:
        current_user.interests = user_update.interests
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url
    if user_update.height_cm is not None:
        current_user.height_cm = user_update.height_cm
    if user_update.weight_kg is not None:
        current_user.weight_kg = user_update.weight_kg
    if user_update.nationality is not None:
        current_user.nationality = user_update.nationality
    if user_update.ethnicity is not None:
        current_user.ethnicity = user_update.ethnicity
    if user_update.photos is not None:
        current_user.photos = user_update.photos
    if user_update.profile_completed is not None:
        current_user.profile_completed = user_update.profile_completed
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get user information by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ==================== MATCHING ROUTES ====================

@app.get("/api/matches", response_model=List[MatchResponse])
async def get_matches(
    limit: int = 10,
    use_ai: bool = False,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Get recommended matches for current user.
    Supports basic matching and optional AI-powered matching.
    """
    matches = get_recommended_matches(db, current_user.id, limit=limit, use_ai=use_ai)
    return matches


# ==================== DATE REQUEST ROUTES ====================

@app.post("/api/date-requests", response_model=DateRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_date_request(
    date_request: DateRequestCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Send a date invitation to another user."""
    # Check if receiver exists
    receiver = db.query(User).filter(User.id == date_request.receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    if receiver.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send date request to yourself"
        )
    
    # Check if request already exists
    existing_request = db.query(DateRequest).filter(
        DateRequest.sender_id == current_user.id,
        DateRequest.receiver_id == date_request.receiver_id
    ).first()
    
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date request already sent"
        )
    
    # Create date request
    new_request = DateRequest(
        sender_id=current_user.id,
        receiver_id=date_request.receiver_id,
        message=date_request.message,
        proposed_date=date_request.proposed_date,
        status="pending"
    )
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    # Load relationships
    db.refresh(new_request, ["sender", "receiver"])
    
    return new_request


@app.get("/api/date-requests", response_model=List[DateRequestResponse])
async def get_date_requests(
    status_filter: str = None,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Get date requests for current user.
    Can filter by status: 'pending', 'accepted', 'rejected'.
    """
    query = db.query(DateRequest).filter(
        (DateRequest.sender_id == current_user.id) |
        (DateRequest.receiver_id == current_user.id)
    )
    
    if status_filter:
        query = query.filter(DateRequest.status == status_filter)
    
    requests = query.order_by(DateRequest.created_at.desc()).all()
    
    # Load relationships
    for req in requests:
        db.refresh(req, ["sender", "receiver"])
    
    return requests


@app.put("/api/date-requests/{request_id}", response_model=DateRequestResponse)
async def update_date_request(
    request_id: int,
    update: DateRequestUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update date request status (accept or reject)."""
    date_request = db.query(DateRequest).filter(DateRequest.id == request_id).first()
    
    if not date_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Date request not found"
        )
    
    # Only receiver can update status
    if date_request.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the receiver can update the request status"
        )
    
    if date_request.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date request has already been processed"
        )
    
    date_request.status = update.status
    db.commit()
    db.refresh(date_request)
    db.refresh(date_request, ["sender", "receiver"])
    
    return date_request


# ==================== EVENT ROUTES ====================

@app.post("/api/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Create a new campus event."""
    new_event = Event(
        creator_id=current_user.id,
        title=event.title,
        description=event.description,
        location=event.location,
        event_time=event.event_time,
        tags=event.tags or [],
        max_attendees=event.max_attendees,
        image_url=event.image_url
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    db.refresh(new_event, ["creator"])
    
    # Get attendee count
    attendee_count = db.query(EventAttendee).filter(
        EventAttendee.event_id == new_event.id,
        EventAttendee.rsvp_status == "going"
    ).count()
    
    event_dict = {
        **new_event.__dict__,
        "attendee_count": attendee_count
    }
    
    return event_dict


@app.get("/api/events", response_model=List[EventResponse])
async def get_events(
    limit: int = 20,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get all events, ordered by event time."""
    events = db.query(Event).order_by(Event.event_time.asc()).limit(limit).all()
    
    result = []
    for event in events:
        db.refresh(event, ["creator"])
        attendee_count = db.query(EventAttendee).filter(
            EventAttendee.event_id == event.id,
            EventAttendee.rsvp_status == "going"
        ).count()
        
        event_dict = {
            **event.__dict__,
            "attendee_count": attendee_count
        }
        result.append(event_dict)
    
    return result


@app.get("/api/events/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get event details by ID."""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.refresh(event, ["creator"])
    attendee_count = db.query(EventAttendee).filter(
        EventAttendee.event_id == event.id,
        EventAttendee.rsvp_status == "going"
    ).count()
    
    event_dict = {
        **event.__dict__,
        "attendee_count": attendee_count
    }
    
    return event_dict


@app.put("/api/events/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update an event (only creator can update)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator can update the event"
        )
    
    if event_update.title is not None:
        event.title = event_update.title
    if event_update.description is not None:
        event.description = event_update.description
    if event_update.location is not None:
        event.location = event_update.location
    if event_update.event_time is not None:
        event.event_time = event_update.event_time
    if event_update.tags is not None:
        event.tags = event_update.tags
    if event_update.max_attendees is not None:
        event.max_attendees = event_update.max_attendees
    if event_update.image_url is not None:
        event.image_url = event_update.image_url
    
    db.commit()
    db.refresh(event)
    db.refresh(event, ["creator"])
    
    attendee_count = db.query(EventAttendee).filter(
        EventAttendee.event_id == event.id,
        EventAttendee.rsvp_status == "going"
    ).count()
    
    event_dict = {
        **event.__dict__,
        "attendee_count": attendee_count
    }
    
    return event_dict


@app.post("/api/events/{event_id}/rsvp", response_model=dict)
async def rsvp_to_event(
    event_id: int,
    rsvp: EventRSVP,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """RSVP to an event (going, interested, or declined)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if RSVP already exists
    existing_rsvp = db.query(EventAttendee).filter(
        EventAttendee.event_id == event_id,
        EventAttendee.user_id == current_user.id
    ).first()
    
    if existing_rsvp:
        # Update existing RSVP
        existing_rsvp.rsvp_status = rsvp.rsvp_status
        db.commit()
        return {"message": "RSVP updated successfully"}
    else:
        # Create new RSVP
        new_rsvp = EventAttendee(
            event_id=event_id,
            user_id=current_user.id,
            rsvp_status=rsvp.rsvp_status
        )
        db.add(new_rsvp)
        db.commit()
        return {"message": "RSVP created successfully"}


# ==================== MESSAGE ROUTES ====================

@app.post("/api/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Send a message to another user."""
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    if receiver.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send message to yourself"
        )
    
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        content=message.content,
        is_read=False
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    db.refresh(new_message, ["sender", "receiver"])
    
    return new_message


@app.get("/api/messages", response_model=List[MessageResponse])
async def get_messages(
    other_user_id: int = None,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Get messages for current user.
    If other_user_id is provided, returns conversation with that user.
    Otherwise, returns all messages.
    """
    if other_user_id:
        # Get conversation with specific user
        messages = db.query(Message).filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == other_user_id)) |
            ((Message.sender_id == other_user_id) & (Message.receiver_id == current_user.id))
        ).order_by(Message.created_at.asc()).all()
    else:
        # Get all messages involving current user
        messages = db.query(Message).filter(
            (Message.sender_id == current_user.id) |
            (Message.receiver_id == current_user.id)
        ).order_by(Message.created_at.desc()).all()
    
    # Load relationships
    for msg in messages:
        db.refresh(msg, ["sender", "receiver"])
    
    return messages


@app.put("/api/messages/{message_id}/read", response_model=MessageResponse)
async def mark_message_read(
    message_id: int,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Mark a message as read."""
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    if message.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the receiver can mark messages as read"
        )
    
    message.is_read = True
    db.commit()
    db.refresh(message)
    db.refresh(message, ["sender", "receiver"])
    
    return message


# ==================== HEALTH CHECK ====================

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

