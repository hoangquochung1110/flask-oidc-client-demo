# Flask OIDC Client Demo with Authlib

A simple Flask application demonstrating OpenID Connect client integration using Authlib.

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure your OIDC provider:
   - Copy `.env.example` to `.env`
   - Update the `.env` file with your OIDC provider details

## Running the Application

Start the application:
```
python app.py
```

The application will be available at http://localhost:5000.

## Features

- OpenID Connect authentication with Authlib
- User profile display with information from ID token
- Logout functionality
- Environment-based configuration for security
- Modular authentication with separation of concerns

## Project Structure

The project now uses a modular approach with authentication code separated:

```
.
├── app.py              # Main Flask application
├── auth/               # Authentication module
│   ├── __init__.py     # Module initialization
│   └── oidc.py         # OIDC implementation
├── templates/          # HTML templates
│   ├── index.html      # Landing page
│   └── profile.html    # User profile page
└── .env                # Environment configuration
```

## Authentication Module

The `auth` module provides the following functions:

- `setup_oidc(app)`: Initialize OIDC with your Flask app
- `login_required`: Decorator to protect routes
- `get_user_info()`: Get the authenticated user's information
- `authenticate()`: Redirect to the authentication provider
- `process_callback()`: Process the authentication callback
- `logout()`: Clear user session data

## Token Exchange Process

In the OIDC authentication flow, the token exchange happens during the callback processing. Authlib abstracts away the complex details of this process:

1. **Authorization Code Extraction**:
   - Automatically extracts the code from Flask's request object

2. **CSRF Protection**:
   - Validates the state parameter to prevent cross-site request forgery

3. **Token Exchange Request**:
   - Constructs a properly formatted HTTP POST request to the token endpoint
   - Includes client credentials via HTTP Basic Authentication
   - Sends the authorization code and other required parameters

4. **Token Validation**:
   - Verifies the JWT signature using the provider's JSON Web Keys (JWKs)
   - Validates expiration time, issuer, and audience claims
   - Performs other security checks

5. **User Information Extraction**:
   - Decodes the ID token and extracts user claims
   - Makes the user information available via the 'userinfo' field

All of this complex logic is encapsulated in a single function call:
```python
token = oauth.oidc.authorize_access_token()
```

## Configuration

Edit the `.env` file to configure your OIDC provider:

```
# OIDC Provider Configuration
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
OIDC_AUTHORITY=https://your-auth-server.com/your-tenant-id
OIDC_DISCOVERY_URL=https://your-auth-server.com/your-tenant-id/.well-known/openid-configuration
OIDC_REDIRECT_URI=http://localhost:5000/auth/callback
```

Replace placeholder values with your actual OIDC provider configuration.

## Manual Configuration (Alternative)

If your provider doesn't support OpenID Connect discovery, you can manually configure the endpoints in the `auth/oidc.py` file:

```python
oauth.register(
    name='oidc',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    access_token_url='https://your-auth-server.com/token',
    authorize_url='https://your-auth-server.com/authorize',
    userinfo_endpoint='https://your-auth-server.com/userinfo',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
``` 