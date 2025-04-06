"""
OIDC Authentication implementation.
"""

import os
from flask import redirect, url_for, session
from functools import wraps
from authlib.integrations.flask_client import OAuth

# Globals
oauth = None

def setup_oidc(app):
    """
    Set up OIDC authentication with the Flask app.
    
    Args:
        app: Flask application instance
    
    Returns:
        OAuth instance configured for OIDC
    """
    global oauth
    
    # Validate required environment variables
    required_env_vars = ['CLIENT_ID', 'CLIENT_SECRET', 'OIDC_AUTHORITY', 
                        'OIDC_DISCOVERY_URL', 'OIDC_REDIRECT_URI']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Initialize OAuth
    oauth = OAuth(app)
    
    # Register OIDC provider
    oauth.register(
        name='oidc',
        authority=os.getenv('OIDC_AUTHORITY'),
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        server_metadata_url=os.getenv('OIDC_DISCOVERY_URL'),
        client_kwargs={'scope': 'email openid phone'}
    )
    
    return oauth

def login_required(f):
    """
    Decorator to protect routes that require authentication.
    
    Args:
        f: The route function to protect
    
    Returns:
        Wrapped function that checks for authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_user_info():
    """
    Get the authenticated user's information from the session.
    
    Returns:
        dict: User information or None if not authenticated
    """
    return session.get('user')

def authenticate(redirect_uri=None):
    """
    Redirect the user to the OIDC provider for authentication.
    
    Args:
        redirect_uri: Optional redirect URI, defaults to the one in environment
        
    Returns:
        Response: Redirect to the OIDC provider
    """
    if not redirect_uri:
        redirect_uri = os.getenv('OIDC_REDIRECT_URI')
    return oauth.oidc.authorize_redirect(redirect_uri)

def process_callback():
    """
    Process the OIDC authentication callback.
    
    This handles the OAuth 2.0 callback from the identity provider.
    
    Behind the scenes, Authlib abstracts away complex token exchange by:
    1. Extracting the authorization code from request.args.get('code')
    2. Validating the 'state' parameter to prevent CSRF attacks
    3. Performing the token exchange by:
       - Constructing a POST request to the token endpoint
       - Including the client credentials for authentication
       - Sending the authorization code and redirect URI
    4. Validating the returned tokens:
       - Verifies the JWT signature using JWKs from the provider
       - Validates token expiration, issuer, and audience claims
       - Checks other security parameters
    5. Decodes the ID token and extracts user information into 'userinfo'
    
    Without this abstraction, we would need dozens of lines of code to:
    - Access the Flask request object to get the code
    - Construct proper HTTP requests with correct headers
    - Handle JWT validation and signature verification
    - Extract user claims from the decoded token
    - Implement various security checks
    
    Returns:
        dict: User information extracted from the ID token
    """
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    if 'email' in user:
        session['email'] = user['email']
    return user

def logout():
    """
    Log the user out by clearing the session.
    
    Returns:
        None
    """
    session.pop('user', None)
    session.pop('email', None) 