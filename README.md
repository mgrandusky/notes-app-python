# 📝 Notes App - Comprehensive Note-Taking Web Application

A feature-rich, secure note-taking web application built with Python Flask, PostgreSQL, and modern web technologies. This application provides a seamless experience for creating, managing, sharing, and exporting notes with OAuth authentication support.

## ✨ Features

### 🔐 Authentication & Security
- **OAuth 2.0 Authentication**: Sign in with Google or GitHub
- **Secure Session Management**: JWT-based authentication with secure cookies
- **CSRF Protection**: All forms protected against Cross-Site Request Forgery
- **Input Sanitization**: Protection against XSS attacks
- **SQL Injection Prevention**: Using SQLAlchemy ORM with parameterized queries

### 📄 Note Management
- **Create Notes**: Rich text editor with formatting options
- **View Notes**: Clean, organized interface with search and filtering
- **Edit Notes**: Full editing capabilities with auto-save support
- **Delete Notes**: Soft delete with confirmation dialogs
- **Archive Notes**: Archive notes to keep workspace clean
- **Rich Text Editing**: Support for bold, italic, lists, headings, and more
- **Tags/Categories**: Organize notes with comma-separated tags
- **Timestamps**: Automatic creation and update tracking

### 🤝 Sharing & Collaboration
- **Share with Users**: Share notes with other registered users by username/email
- **Public Links**: Generate shareable links with optional expiration
- **Permission Control**: Set view-only or edit permissions
- **Email Notes**: Send notes directly via email
- **Export Options**:
  - 📄 PDF export with professional formatting
  - 📝 Plain text export
  - 📧 Email delivery

### 🎨 User Experience
- **Responsive Design**: Mobile-friendly interface
- **Dark Mode**: Toggle between light and dark themes
- **Real-time Search**: Filter notes by title, content, or tags
- **Sorting Options**: Sort by date or title, ascending/descending
- **AJAX Operations**: Seamless interactions without page reloads
- **Loading Indicators**: Visual feedback for async operations
- **Toast Notifications**: User-friendly success/error messages

## 🛠️ Technology Stack

- **Backend**: Python 3.8+ with Flask framework
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Authentication**: Authlib for OAuth 2.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Email**: Flask-Mail with SMTP
- **PDF Generation**: ReportLab
- **Security**: Flask-WTF (CSRF), Bleach (XSS protection)

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12+ (or use SQLite for development)
- Google OAuth credentials (for Google login)
- GitHub OAuth credentials (for GitHub login)
- SMTP email account (for email features)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mgrandusky/notes-app.git
cd notes-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the `.env.example` file to `.env` and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/notesapp
# Or use SQLite for development:
# DATABASE_URL=sqlite:///notes.db

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=development
FLASK_APP=app.py

# Google OAuth (see section below)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth (see section below)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Email Configuration (see section below)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Application Configuration
APP_URL=http://localhost:5000
```

### 5. Database Setup

#### Using PostgreSQL (Recommended for Production)

```bash
# Create database
createdb notesapp

# Or using psql
psql -U postgres
CREATE DATABASE notesapp;
\q
```

#### Using SQLite (Development Only)

No setup needed - database file will be created automatically.

### 6. Initialize Database Tables

```bash
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.models import db; db.create_all()"
```

Or run the application once - tables will be created automatically.

## 🔑 OAuth Configuration

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure consent screen if prompted
6. Application type: "Web application"
7. Add authorized redirect URIs:
   - `http://localhost:5000/auth/login/google/callback` (development)
   - `https://yourdomain.com/auth/login/google/callback` (production)
8. Copy Client ID and Client Secret to your `.env` file

### GitHub OAuth Setup

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in application details:
   - Application name: "Notes App"
   - Homepage URL: `http://localhost:5000` (or your domain)
   - Authorization callback URL: `http://localhost:5000/auth/login/github/callback`
4. Copy Client ID and generate Client Secret
5. Add both to your `.env` file

## 📧 Email Configuration

### Using Gmail

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Copy the generated password
3. Use your Gmail address as `MAIL_USERNAME`
4. Use the App Password as `MAIL_PASSWORD`

### Using Other SMTP Providers

Update these settings in `.env`:
- `MAIL_SERVER`: Your SMTP server (e.g., smtp.sendgrid.net)
- `MAIL_PORT`: Usually 587 for TLS or 465 for SSL
- `MAIL_USE_TLS`: True or False
- `MAIL_USERNAME`: Your SMTP username
- `MAIL_PASSWORD`: Your SMTP password

## 🎮 Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode

```bash
# Set environment
export FLASK_ENV=production

# Using Gunicorn (recommended)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with more workers
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

## 📖 Usage Guide

### Creating Your First Note

1. Sign in using Google or GitHub
2. Click "New Note" button
3. Enter a title
4. Use the rich text editor toolbar for formatting:
   - **B** for bold
   - *I* for italic
   - Lists, headings, and more
5. Add optional tags (comma-separated)
6. Click "Save Note"

### Managing Notes

- **Search**: Use the search box to find notes by title or content
- **Filter by Tag**: Click on tag filters to show specific notes
- **Sort**: Choose sorting by date or title
- **Archive**: Archive notes to remove from main view
- **Delete**: Permanently delete notes (with confirmation)

### Sharing Notes

1. Open a note
2. Click "Share" button
3. Choose sharing method:
   - **Share with User**: Enter username/email, set permissions
   - **Create Link**: Generate public link with optional expiration
   - **Email**: Send note content via email
   - **Export**: Download as PDF or text file

### Using Dark Mode

- Click the moon/sun icon in the navigation bar
- Theme preference is saved automatically

## 🏗️ Project Structure

```
notes-app/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── note.py          # Note model
│   │   └── shared_note.py   # Shared notes model
│   ├── routes/              # Route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── notes.py         # Note CRUD routes
│   │   └── sharing.py       # Sharing & export routes
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── oauth_service.py # OAuth handling
│   │   ├── email_service.py # Email functionality
│   │   └── pdf_service.py   # PDF generation
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── notes/
│   │   ├── shared/
│   │   └── errors/
│   └── static/              # Static files
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── main.js
│           ├── notes.js
│           ├── editor.js
│           └── view.js
├── config.py                # Configuration
├── app.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔒 Security Features

- **OAuth 2.0**: Secure third-party authentication
- **CSRF Protection**: All forms include CSRF tokens
- **XSS Prevention**: HTML content sanitized with Bleach
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Secure Sessions**: HTTPOnly, Secure, and SameSite cookies
- **Password Hashing**: Not applicable (OAuth only)
- **Environment Variables**: Sensitive data kept out of code

## 🧪 API Endpoints

### Authentication
- `GET /auth/login` - Login page
- `GET /auth/login/google` - Initiate Google OAuth
- `GET /auth/login/github` - Initiate GitHub OAuth
- `GET /auth/logout` - Logout user
- `GET /auth/profile` - User profile page

### Notes
- `GET /notes` - List all notes (HTML)
- `GET /api/notes` - Get notes (JSON)
- `POST /api/notes` - Create note
- `GET /api/notes/<id>` - Get note by ID
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note
- `POST /api/notes/<id>/archive` - Archive/unarchive note
- `GET /api/tags` - Get all tags

### Sharing
- `POST /share/api/notes/<id>/share` - Share note
- `GET /share/api/notes/<id>/shares` - Get note shares
- `DELETE /share/api/shares/<id>` - Revoke share
- `GET /share/<id>` - View shared note
- `GET /share/public/<token>` - View public note
- `GET /share/api/notes/<id>/export/pdf` - Export to PDF
- `GET /share/api/notes/<id>/export/text` - Export to text
- `POST /share/api/notes/<id>/email` - Email note

## 🐛 Troubleshooting

### Database Connection Issues

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
- Verify PostgreSQL is running: `pg_ctl status`
- Check DATABASE_URL in `.env`
- Ensure database exists: `psql -l`
- For SQLite, no action needed

### OAuth Redirect URI Mismatch

**Problem**: OAuth fails with redirect URI error

**Solution**:
- Verify callback URLs in OAuth console match your `.env` APP_URL
- Development: `http://localhost:5000/auth/login/<provider>/callback`
- Production: `https://yourdomain.com/auth/login/<provider>/callback`

### Email Not Sending

**Problem**: Notes not sending via email

**Solution**:
- Check SMTP credentials in `.env`
- For Gmail, ensure App Password is used (not account password)
- Verify firewall allows outbound SMTP connections
- Check email logs in console for errors

### Import Errors

**Problem**: `ModuleNotFoundError` or import errors

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### CSS/JS Not Loading

**Problem**: Styles or scripts not applying

**Solution**:
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check browser console for 404 errors
- Verify static files exist in `app/static/`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Flask framework and community
- All contributors and testers
- OAuth providers (Google, GitHub)
- Icon sources and design inspiration

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review closed issues for solutions

---

**Note**: This is a development version. For production deployment, additional security measures and optimizations are recommended, including:
- SSL/TLS certificates
- Rate limiting
- Database connection pooling
- CDN for static files
- Monitoring and logging
- Regular backups
