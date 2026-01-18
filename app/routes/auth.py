from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from app.services.oauth_service import oauth, get_google_user_info, get_github_user_info

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    """Display login page"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login/google')
def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        token = oauth.google.authorize_access_token()
        user_info = get_google_user_info(token)
        
        if not user_info:
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('auth.login'))
        
        # Find or create user
        user = User.query.filter_by(oauth_provider='google', oauth_id=user_info['oauth_id']).first()
        
        if not user:
            # Check if email already exists
            user = User.query.filter_by(email=user_info['email']).first()
            if user:
                # Link Google account to existing user
                user.oauth_provider = 'google'
                user.oauth_id = user_info['oauth_id']
                user.profile_picture = user_info['profile_picture']
            else:
                # Create new user
                username = user_info['username']
                # Ensure unique username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{user_info['username']}{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=user_info['email'],
                    oauth_provider='google',
                    oauth_id=user_info['oauth_id'],
                    profile_picture=user_info['profile_picture']
                )
                db.session.add(user)
        
        db.session.commit()
        login_user(user, remember=True)
        
        flash(f'Welcome, {user.username}!', 'success')
        
        # Redirect to next page or dashboard
        next_page = session.get('next') or url_for('notes.index')
        session.pop('next', None)
        return redirect(next_page)
        
    except Exception as e:
        print(f"Google OAuth error: {e}")
        flash('An error occurred during Google login. Please try again.', 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/login/github')
def github_login():
    """Initiate GitHub OAuth login"""
    redirect_uri = url_for('auth.github_callback', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@auth_bp.route('/login/github/callback')
def github_callback():
    """Handle GitHub OAuth callback"""
    try:
        token = oauth.github.authorize_access_token()
        user_info = get_github_user_info(oauth.github)
        
        if not user_info or not user_info.get('email'):
            flash('Failed to get user information from GitHub. Please make sure your email is public or grant email access.', 'error')
            return redirect(url_for('auth.login'))
        
        # Find or create user
        user = User.query.filter_by(oauth_provider='github', oauth_id=user_info['oauth_id']).first()
        
        if not user:
            # Check if email already exists
            user = User.query.filter_by(email=user_info['email']).first()
            if user:
                # Link GitHub account to existing user
                user.oauth_provider = 'github'
                user.oauth_id = user_info['oauth_id']
                user.profile_picture = user_info['profile_picture']
            else:
                # Create new user
                username = user_info['username']
                # Ensure unique username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{user_info['username']}{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=user_info['email'],
                    oauth_provider='github',
                    oauth_id=user_info['oauth_id'],
                    profile_picture=user_info['profile_picture']
                )
                db.session.add(user)
        
        db.session.commit()
        login_user(user, remember=True)
        
        flash(f'Welcome, {user.username}!', 'success')
        
        # Redirect to next page or dashboard
        next_page = session.get('next') or url_for('notes.index')
        session.pop('next', None)
        return redirect(next_page)
        
    except Exception as e:
        print(f"GitHub OAuth error: {e}")
        flash('An error occurred during GitHub login. Please try again.', 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """Display user profile"""
    return render_template('auth/profile.html', user=current_user)
