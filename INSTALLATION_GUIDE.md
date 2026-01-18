# 🚀 Quick Installation Guide

## Prerequisites Checklist

Before you begin, ensure you have:
- [ ] Python 3.8+ installed
- [ ] pip package manager
- [ ] PostgreSQL (optional, SQLite works for development)
- [ ] Google OAuth credentials (optional, for Google login)
- [ ] GitHub OAuth credentials (optional, for GitHub login)
- [ ] SMTP email account (optional, for email features)

## Step-by-Step Installation

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/mgrandusky/notes-app.git
cd notes-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Required: SECRET_KEY
# Optional: OAuth credentials, Email settings
```

### 3. Database Setup

#### Option A: SQLite (Development - No Setup Required)
Just run the app - database will be created automatically!

#### Option B: PostgreSQL (Production Recommended)
```bash
# Create database
createdb notesapp

# Update DATABASE_URL in .env:
DATABASE_URL=postgresql://username:password@localhost/notesapp
```

### 4. OAuth Setup (Optional but Recommended)

#### Google OAuth:
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google+ API
3. Create OAuth 2.0 credentials
4. Add redirect URI: `http://localhost:5000/auth/login/google/callback`
5. Copy Client ID and Secret to `.env`

#### GitHub OAuth:
1. Visit [GitHub Settings](https://github.com/settings/developers)
2. New OAuth App
3. Callback URL: `http://localhost:5000/auth/login/github/callback`
4. Copy Client ID and Secret to `.env`

### 5. Email Setup (Optional)

For Gmail:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
```

### 6. Run the Application

```bash
# Development mode
python app.py

# Visit: http://localhost:5000
```

## Minimal Setup (No OAuth)

If you want to test without OAuth:

1. Skip OAuth credentials
2. You can manually create users in database for testing:

```python
from app import create_app
from app.models import User, db

app = create_app()
with app.app_context():
    user = User(
        username='testuser',
        email='test@example.com',
        oauth_provider='test',
        oauth_id='123'
    )
    db.session.add(user)
    db.session.commit()
    print(f"Created user: {user.username}")
```

## Production Deployment

### Using Gunicorn:

```bash
# Install gunicorn (already in requirements.txt)
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With more options:
gunicorn -w 4 \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  app:app
```

### Environment Variables for Production:

```env
FLASK_ENV=production
SECRET_KEY=generate-strong-random-key
DATABASE_URL=postgresql://user:pass@host/db
SESSION_COOKIE_SECURE=True
```

## Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Database Errors
```bash
# Recreate database tables
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Port Already in Use
```bash
# Change port in app.py or use:
python app.py --port 5001
```

## Verify Installation

Run the validation script:

```bash
python -c "from app import create_app; app = create_app(); print('✓ Application works!')"
```

If you see "✓ Application works!" - you're ready to go!

## Next Steps

1. Access the application at http://localhost:5000
2. Sign in with Google or GitHub
3. Create your first note
4. Explore sharing and export features

## Need Help?

- Check README.md for detailed documentation
- Review FEATURES.md for implemented features
- Check application logs in console
- Open an issue on GitHub

Happy note-taking! 📝
