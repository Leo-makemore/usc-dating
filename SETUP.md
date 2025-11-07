# Setup Instructions - University Dating App MVP

This guide will walk you through setting up the full-stack dating app from scratch.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [API Keys & External Services](#api-keys--external-services)
6. [Running the Application](#running-the-application)
7. [Deployment](#deployment)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** and **npm** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 14+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** - [Download Git](https://git-scm.com/downloads)

---

## Database Setup

### 1. Install PostgreSQL

Follow the installation instructions for your operating system from the PostgreSQL website.

### 2. Create Database

Open your PostgreSQL client (psql, pgAdmin, or command line) and run:

```sql
CREATE DATABASE dating_app;
```

### 3. Create Database User (Optional but Recommended)

```sql
CREATE USER dating_app_user WITH PASSWORD 'LBE50q17!';
GRANT ALL PRIVILEGES ON DATABASE dating_app TO dating_app_user;
```

### 4. Run Database Schema

Execute the SQL schema file to create all tables:

```bash
psql -U dating_app_user -d dating_app -f database/schema.sql
```

Or if using the default postgres user:

```bash
psql -U postgres -d dating_app -f database/schema.sql
```

**Note:** The backend will also automatically create tables using SQLAlchemy, but running the schema manually ensures proper setup.

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and fill in your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://dating_app_user:your_secure_password@localhost:5432/dating_app

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Service (Resend API) - See API Keys section
RESEND_API_KEY=your-resend-api-key-here
FROM_EMAIL=noreply@yourdomain.com

# OpenAI API (for AI matching) - Optional
OPENAI_API_KEY=your-openai-api-key-here

# CORS Configuration
FRONTEND_URL=http://localhost:5173

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Important:** 
- Generate a secure `SECRET_KEY` using: `openssl rand -hex 32`
- Replace `your_secure_password` with your actual PostgreSQL password
- See [API Keys & External Services](#api-keys--external-services) for obtaining API keys

### 5. Test Backend

Run the development server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

You can test it by visiting:
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables (Optional)

Create a `.env` file in the `frontend` directory if you need to change the API URL:

```env
VITE_API_URL=http://localhost:8000
```

**Note:** The default is `http://localhost:8000`, so this is only needed if your backend runs on a different URL.

### 4. Test Frontend

Run the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## API Keys & External Services

### 1. Email Service (Resend)

**Purpose:** Send verification emails to users

**Steps:**
1. Go to [Resend.com](https://resend.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key to your `.env` file as `RESEND_API_KEY`
6. Add your sending domain or use Resend's test domain
7. Set `FROM_EMAIL` to your verified email address

**Free Tier:** 3,000 emails/month

**Alternative:** For development, the app will print verification tokens to console if Resend is not configured.

### 2. OpenAI API (Optional - for AI Matching)

**Purpose:** Enhanced matching using AI embeddings

**Steps:**
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key to your `.env` file as `OPENAI_API_KEY`

**Free Tier:** $5 free credits for new users

**Note:** The app works without OpenAI - it will use basic matching based on interests, school, and year.

### 3. Cloud Storage (Optional - for Avatars and Event Images)

**Options:**
- **Cloudinary** - [cloudinary.com](https://cloudinary.com) - Free tier: 25GB storage
- **AWS S3** - [aws.amazon.com/s3](https://aws.amazon.com/s3) - Free tier: 5GB storage
- **Google Cloud Storage** - [cloud.google.com/storage](https://cloud.google.com/storage)

**Implementation:** You'll need to add file upload endpoints to the backend and integrate with your chosen service.

---

## Running the Application

### Development Mode

1. **Start PostgreSQL** (if not running as a service)

2. **Start Backend:**
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python main.py
   ```

3. **Start Frontend** (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access the Application:**
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### Testing the Application

1. **Register a new user:**
   - Go to `http://localhost:5173/register`
   - Use a `.edu` email address
   - Fill in all required fields

2. **Verify email:**
   - Check your email (or console logs if Resend is not configured)
   - Click the verification link

3. **Login:**
   - Go to `http://localhost:5173/login`
   - Enter your credentials

4. **Explore features:**
   - View matches
   - Send date requests
   - Create events
   - Send messages

---

## Deployment

### Frontend Deployment (Vercel)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Configure Environment Variables:**
   - Go to Vercel dashboard → Your project → Settings → Environment Variables
   - Add `VITE_API_URL` with your backend URL (e.g., `https://your-backend.onrender.com`)

5. **Update Backend CORS:**
   - In your backend `.env`, set `FRONTEND_URL` to your Vercel deployment URL

### Backend Deployment (Render)

1. **Create a Render Account:**
   - Go to [render.com](https://render.com)
   - Sign up for free

2. **Create a Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `backend` directory

3. **Configure Build Settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   - Go to Environment section
   - Add all variables from your `.env` file:
     - `DATABASE_URL` (use Render PostgreSQL connection string)
     - `SECRET_KEY`
     - `RESEND_API_KEY`
     - `OPENAI_API_KEY` (optional)
     - `FRONTEND_URL` (your Vercel URL)
     - `FROM_EMAIL`

5. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy your backend

### Database Deployment (Render PostgreSQL)

1. **Create PostgreSQL Database:**
   - In Render dashboard, click "New" → "PostgreSQL"
   - Choose a name and region
   - Click "Create Database"

2. **Get Connection String:**
   - Copy the "Internal Database URL" or "External Database URL"
   - Use this as your `DATABASE_URL` in backend environment variables

3. **Run Schema:**
   - Connect to the database using a PostgreSQL client
   - Run the schema: `psql <connection_string> -f database/schema.sql`

### Alternative: Google Cloud Run (Backend)

1. **Install Google Cloud SDK:**
   ```bash
   # Follow instructions at: https://cloud.google.com/sdk/docs/install
   ```

2. **Create a Dockerfile** (create in `backend/` directory):
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

3. **Build and Deploy:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/dating-app-backend
   gcloud run deploy dating-app-backend --image gcr.io/YOUR_PROJECT_ID/dating-app-backend --platform managed
   ```

4. **Set Environment Variables:**
   - In Cloud Run console, go to your service → Edit & Deploy New Revision
   - Add environment variables under "Variables & Secrets"

### Alternative: Railway (Database & Backend)

1. **Create Railway Account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create PostgreSQL Database:**
   - Click "New Project" → "Add PostgreSQL"
   - Railway will create a database automatically

3. **Deploy Backend:**
   - Click "New" → "GitHub Repo" → Select your repository
   - Set root directory to `backend`
   - Add environment variables
   - Railway will auto-detect Python and deploy

---

## Troubleshooting

### Backend Issues

**Database Connection Error:**
- Verify PostgreSQL is running: `pg_isready`
- Check `DATABASE_URL` in `.env` matches your database credentials
- Ensure database exists: `psql -l` to list databases

**Import Errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Port Already in Use:**
- Change `PORT` in `.env` or kill the process using port 8000

### Frontend Issues

**API Connection Error:**
- Verify backend is running
- Check `VITE_API_URL` in frontend `.env`
- Check CORS settings in backend

**Build Errors:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 18+)

### Email Verification Issues

**Emails Not Sending:**
- Check Resend API key is correct
- Verify `FROM_EMAIL` is a verified domain in Resend
- Check backend logs for error messages
- In development, check console for verification tokens

---

## Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use HTTPS for all connections
- [ ] Set secure CORS origins (not `*`)
- [ ] Enable rate limiting
- [ ] Use environment variables for all secrets
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Review and update dependencies regularly
- [ ] Implement input validation on all endpoints
- [ ] Use prepared statements (SQLAlchemy does this automatically)

---

## Next Steps

After setup:

1. **Customize the UI:** Modify TailwindCSS classes in frontend components
2. **Add Features:** Implement additional features like:
   - Image upload for avatars
   - Push notifications
   - Advanced filtering
   - Block/report users
3. **Optimize:** 
   - Add caching
   - Implement pagination
   - Optimize database queries
4. **Test:** Write unit and integration tests
5. **Monitor:** Set up error tracking (Sentry, etc.)

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review backend logs: `tail -f backend/logs/app.log` (if logging is configured)
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly
5. Ensure all services (PostgreSQL, backend, frontend) are running

---

## License

This is an MVP project. Customize and use as needed for your purposes.

