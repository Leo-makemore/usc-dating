# Project Overview - University Dating App MVP

## 📁 Project Structure

```
usc dating/
├── backend/                    # FastAPI backend application
│   ├── main.py                # Main FastAPI app with all routes
│   ├── config.py              # Configuration and settings
│   ├── database.py            # Database connection and session management
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic schemas for request/response validation
│   ├── auth.py                # JWT authentication utilities
│   ├── dependencies.py        # FastAPI dependencies (auth, user verification)
│   ├── email_service.py       # Email verification service (Resend)
│   ├── matching.py            # Matching algorithm (basic + AI-powered)
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── Dockerfile             # Docker configuration for deployment
│   └── .gitignore             # Git ignore rules
│
├── frontend/                  # React + Vite frontend application
│   ├── src/
│   │   ├── App.jsx            # Main app component with routing
│   │   ├── main.jsx           # React entry point
│   │   ├── index.css          # Global styles with TailwindCSS
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx # Authentication context provider
│   │   ├── services/
│   │   │   └── api.js          # Axios API client configuration
│   │   ├── components/
│   │   │   └── Layout.jsx     # Main layout with navigation
│   │   └── pages/
│   │       ├── Login.jsx      # Login page
│   │       ├── Register.jsx   # Registration page
│   │       ├── VerifyEmail.jsx # Email verification page
│   │       ├── Profile.jsx    # User profile page
│   │       ├── Matches.jsx    # Matches/recommendations page
│   │       ├── DateRequests.jsx # Date invitations page
│   │       ├── Events.jsx     # Campus events page
│   │       └── Messages.jsx   # Messaging page
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # TailwindCSS configuration
│   ├── postcss.config.js      # PostCSS configuration
│   ├── index.html             # HTML template
│   ├── .env.example           # Environment variables template
│   └── .gitignore             # Git ignore rules
│
├── database/
│   └── schema.sql             # PostgreSQL database schema
│
├── README.md                  # Project introduction
├── SETUP.md                   # Comprehensive setup guide
├── QUICKSTART.md              # Quick start guide
└── PROJECT_OVERVIEW.md        # This file
```

## 🎯 Features Implemented

### 1. User Registration & Verification ✅
- University email validation (.edu domain only)
- Email verification with token-based system
- Password hashing with bcrypt
- User profile storage (email, name, school, year, interests, avatar)

### 2. User Profile ✅
- View and update profile information
- Manage interests (stored as array/tags)
- Avatar URL support

### 3. Matching System ✅
- Basic matching algorithm based on:
  - Shared interests (40% weight)
  - Same school (40% weight)
  - Same year (20% weight)
- Optional AI-powered matching using OpenAI embeddings
- Match score calculation and ranking

### 4. Date Invitations ✅
- Send date invitations to matches
- Status tracking: pending, accepted, rejected
- View sent and received invitations
- Accept/reject functionality

### 5. Event System ✅
- Create campus events with:
  - Title, description, location
  - Event time
  - Tags
  - Max attendees
  - Image URL
- RSVP system: going, interested, declined
- View all events and attendee counts

### 6. Messaging System ✅
- Send messages to matches
- View conversation history
- Mark messages as read
- Real-time ready (polling support, WebSocket can be added)

### 7. Backend ✅
- FastAPI with REST API
- JWT authentication
- Password hashing
- Input validation with Pydantic
- Error handling
- CORS configuration
- Database models with SQLAlchemy

### 8. Database ✅
- PostgreSQL schema
- Tables: Users, DateRequests, Events, EventAttendees, Messages, Matches
- Proper relationships and constraints
- Indexes for performance

### 9. Frontend ✅
- React + Vite
- TailwindCSS for styling
- Pages: Login, Register, Verify Email, Profile, Matches, Date Requests, Events, Messages
- API integration with Axios
- Protected routes
- Authentication context

### 10. Deployment Ready ✅
- Dockerfile for backend
- Environment variable configuration
- Deployment instructions for:
  - Frontend: Vercel
  - Backend: Render / Google Cloud Run
  - Database: Render PostgreSQL / Railway

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/verify-email` - Verify email with token

### Users
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/{user_id}` - Get user by ID

### Matches
- `GET /api/matches` - Get recommended matches

### Date Requests
- `POST /api/date-requests` - Send date request
- `GET /api/date-requests` - Get date requests
- `PUT /api/date-requests/{id}` - Update request status

### Events
- `POST /api/events` - Create event
- `GET /api/events` - Get all events
- `GET /api/events/{id}` - Get event by ID
- `PUT /api/events/{id}` - Update event
- `POST /api/events/{id}/rsvp` - RSVP to event

### Messages
- `POST /api/messages` - Send message
- `GET /api/messages` - Get messages
- `PUT /api/messages/{id}/read` - Mark message as read

## 🗄️ Database Schema

### Tables
1. **users** - User accounts and profiles
2. **date_requests** - Date invitations between users
3. **events** - Campus events
4. **event_attendees** - RSVP status for events
5. **messages** - Chat messages between users
6. **matches** - Mutual matches (optional tracking)

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Email verification required for full access
- University email domain validation
- Input validation with Pydantic
- SQL injection protection (SQLAlchemy ORM)
- CORS configuration

## 🚀 Getting Started

1. **Quick Start**: See [QUICKSTART.md](./QUICKSTART.md) for 5-minute setup
2. **Detailed Setup**: See [SETUP.md](./SETUP.md) for comprehensive instructions
3. **Deployment**: See [SETUP.md](./SETUP.md#deployment) for deployment guide

## 📝 Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `RESEND_API_KEY` - Email service API key (optional)
- `OPENAI_API_KEY` - OpenAI API key for AI matching (optional)
- `FRONTEND_URL` - Frontend URL for CORS

### Frontend (.env)
- `VITE_API_URL` - Backend API URL

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **JWT** - Authentication tokens
- **Pydantic** - Data validation
- **Resend** - Email service
- **OpenAI** - AI embeddings (optional)

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client

## 📚 Documentation

- **API Documentation**: Available at `http://localhost:8000/docs` when backend is running
- **Setup Guide**: [SETUP.md](./SETUP.md)
- **Quick Start**: [QUICKSTART.md](./QUICKSTART.md)

## 🎨 UI/UX Features

- Responsive design with TailwindCSS
- Clean, modern interface
- Navigation bar with all main sections
- User-friendly forms with validation
- Match cards with scores and interests
- Event cards with RSVP buttons
- Messaging interface with conversation list

## 🔄 Next Steps (Future Enhancements)

- Real-time messaging with WebSocket
- Image upload for avatars and events
- Push notifications
- Advanced filtering and search
- Block/report users
- Admin dashboard
- Analytics and insights
- Mobile app (React Native)

## 📄 License

This is an MVP project. Customize and use as needed.

## 🤝 Support

For setup issues, refer to:
1. [QUICKSTART.md](./QUICKSTART.md) - Quick setup
2. [SETUP.md](./SETUP.md) - Detailed guide
3. Troubleshooting section in SETUP.md

