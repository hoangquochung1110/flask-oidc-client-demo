import os
from flask import Flask, redirect, url_for, render_template
from dotenv import load_dotenv
from auth import setup_oidc, login_required, get_user_info

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# Initialize OIDC
from auth.oidc import authenticate, process_callback, logout

# Setup OIDC with our Flask app
setup_oidc(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return authenticate()

@app.route('/authorize')
def callback():
    """Process the OIDC authentication callback.

    This route handles the OAuth 2.0 callback from the identity provider.
    The actual processing is delegated to our auth module.
    
    For detailed documentation about the token exchange process and
    the abstractions Authlib provides, see the process_callback()
    function in auth/oidc.py.
    
    Returns:
        redirect: Redirects to profile page after successful authentication
    """
    process_callback()
    return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    user_info = get_user_info()
    return render_template('profile.html', user_info=user_info)

@app.route('/logout')
def logout_route():
    logout()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 