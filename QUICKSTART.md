# Quick Start Guide

Get the app running in 5 minutes!

## Prerequisites Check

```bash
python3 --version  # Should be 3.9+
node --version     # Should be 18+
psql --version     # Should be 14+
```

## 1. Database Setup (2 minutes)

```bash
# Create database
createdb dating_app

# Or using psql:
psql -U postgres -c "CREATE DATABASE dating_app;"

# Run schema
psql -U postgres -d dating_app -f database/schema.sql
```

## 2. Backend Setup (2 minutes)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dating_app
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
HOST=0.0.0.0
PORT=8000
EOF

# Start backend
python main.py
```

Backend will run on `http://localhost:8000`

## 3. Frontend Setup (1 minute)

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

## 4. Test It!

1. Open `http://localhost:5173`
2. Register with a `.edu` email
3. Check console/terminal for verification token (if email not configured)
4. Verify email and login
5. Start exploring!

## Optional: Enable Email Verification

1. Sign up at [resend.com](https://resend.com)
2. Get API key
3. Add to backend `.env`:
   ```
   RESEND_API_KEY=your_key_here
   FROM_EMAIL=noreply@yourdomain.com
   ```

## Optional: Enable AI Matching

1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Get API key
3. Add to backend `.env`:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Troubleshooting

**Database connection error?**
- Make sure PostgreSQL is running: `pg_isready`
- Check DATABASE_URL in `.env` matches your setup

**Port already in use?**
- Change PORT in backend `.env`
- Or kill the process: `lsof -ti:8000 | xargs kill`

**Frontend can't connect to backend?**
- Make sure backend is running
- Check CORS settings in backend

For detailed setup, see [SETUP.md](./SETUP.md)

