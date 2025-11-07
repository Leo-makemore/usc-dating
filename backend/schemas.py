"""
Pydantic schemas for request/response validation.
Defines the structure of API request and response bodies.
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    name: str
    school: str
    year: str
    interests: Optional[List[str]] = []
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    nationality: Optional[str] = None
    ethnicity: Optional[str] = None
    photos: Optional[List[str]] = []


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    avatar_url: Optional[str]
    profile_completed: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = None
    school: Optional[str] = None
    year: Optional[str] = None
    interests: Optional[List[str]] = None
    avatar_url: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    nationality: Optional[str] = None
    ethnicity: Optional[str] = None
    photos: Optional[List[str]] = None
    profile_completed: Optional[bool] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserRegisterStep1(BaseModel):
    """Schema for registration step 1: email and password."""
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class EmailOnly(BaseModel):
    """Schema for email-only registration (SSO flow)."""
    email: EmailStr


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth authentication."""
    token: str  # Google ID token


class UserRegisterStep2(BaseModel):
    """Schema for registration step 2: personal information."""
    name: str
    school: str
    year: str
    interests: Optional[List[str]] = []
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    nationality: Optional[str] = None
    ethnicity: Optional[str] = None
    photos: Optional[List[str]] = []


# Auth Schemas
class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""
    user_id: Optional[int] = None


# Date Request Schemas
class DateRequestCreate(BaseModel):
    """Schema for creating a date request."""
    receiver_id: int
    message: Optional[str] = None
    proposed_date: Optional[datetime] = None


class DateRequestResponse(BaseModel):
    """Schema for date request response."""
    id: int
    sender_id: int
    receiver_id: int
    status: str
    message: Optional[str]
    proposed_date: Optional[datetime]
    created_at: datetime
    sender: UserResponse
    receiver: UserResponse
    
    class Config:
        from_attributes = True


class DateRequestUpdate(BaseModel):
    """Schema for updating date request status."""
    status: str  # 'accepted' or 'rejected'
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ['accepted', 'rejected']:
            raise ValueError('Status must be "accepted" or "rejected"')
        return v


# Event Schemas
class EventCreate(BaseModel):
    """Schema for creating an event."""
    title: str
    description: Optional[str] = None
    location: str
    event_time: datetime
    tags: Optional[List[str]] = []
    max_attendees: Optional[int] = None
    image_url: Optional[str] = None


class EventResponse(BaseModel):
    """Schema for event response."""
    id: int
    creator_id: int
    title: str
    description: Optional[str]
    location: str
    event_time: datetime
    tags: Optional[List[str]]
    max_attendees: Optional[int]
    image_url: Optional[str]
    created_at: datetime
    creator: UserResponse
    attendee_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


class EventUpdate(BaseModel):
    """Schema for updating an event."""
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    event_time: Optional[datetime] = None
    tags: Optional[List[str]] = None
    max_attendees: Optional[int] = None
    image_url: Optional[str] = None


# Event Attendee Schemas
class EventRSVP(BaseModel):
    """Schema for RSVP to an event."""
    rsvp_status: str  # 'going', 'interested', 'declined'
    
    @validator('rsvp_status')
    def validate_rsvp_status(cls, v):
        if v not in ['going', 'interested', 'declined']:
            raise ValueError('RSVP status must be "going", "interested", or "declined"')
        return v


# Message Schemas
class MessageCreate(BaseModel):
    """Schema for creating a message."""
    receiver_id: int
    content: str


class MessageResponse(BaseModel):
    """Schema for message response."""
    id: int
    sender_id: int
    receiver_id: int
    content: str
    is_read: bool
    created_at: datetime
    sender: UserResponse
    receiver: UserResponse
    
    class Config:
        from_attributes = True


# Match Schemas
class MatchResponse(BaseModel):
    """Schema for match response."""
    id: int
    name: str
    school: str
    year: str
    interests: Optional[List[str]]
    avatar_url: Optional[str]
    match_score: float


# Verification Schema
class VerificationRequest(BaseModel):
    """Schema for email verification."""
    token: str

