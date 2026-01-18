from authlib.integrations.flask_client import OAuth
from flask import url_for

oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth providers"""
    oauth.init_app(app)
    
    # Google OAuth
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    # GitHub OAuth
    oauth.register(
        name='github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )
    
    return oauth

def get_google_user_info(token):
    """Extract user info from Google OAuth token"""
    if not token:
        return None
    
    userinfo = token.get('userinfo')
    if not userinfo:
        return None
    
    return {
        'oauth_id': userinfo.get('sub'),
        'email': userinfo.get('email'),
        'username': userinfo.get('email').split('@')[0] if userinfo.get('email') else None,
        'profile_picture': userinfo.get('picture'),
        'oauth_provider': 'google'
    }

def get_github_user_info(oauth_client):
    """Fetch user info from GitHub API"""
    try:
        resp = oauth_client.get('user')
        user_data = resp.json()
        
        # Get email if not public
        email = user_data.get('email')
        if not email:
            emails_resp = oauth_client.get('user/emails')
            emails = emails_resp.json()
            for email_data in emails:
                if email_data.get('primary'):
                    email = email_data.get('email')
                    break
        
        return {
            'oauth_id': str(user_data.get('id')),
            'email': email,
            'username': user_data.get('login'),
            'profile_picture': user_data.get('avatar_url'),
            'oauth_provider': 'github'
        }
    except Exception as e:
        print(f"Error fetching GitHub user info: {e}")
        return None
