import os
import logging
import json
import base64
import requests
from flask import Flask, redirect, url_for, render_template, request
from dotenv import load_dotenv
from jwt import PyJWT

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration variables
config = {
    # AWS Region where ALB is deployed
    'region': os.getenv('AWS_REGION', 'ap-southeast-1'),
    
    # ALB ARN for JWT validation
    'alb_arn': os.getenv('ALB_ARN', 'arn:aws:elasticloadbalancing:region-code:account-id:loadbalancer/app/load-balancer-name/load-balancer-id'),
    
    # Cognito configuration for logout
    'cognito_domain': os.getenv('COGNITO_DOMAIN', 'your-cognito-domain.auth.region.amazoncognito.com'),
    'client_id': os.getenv('CLIENT_ID', 'your-client-id'),
    'logout_redirect_uri': os.getenv('LOGOUT_REDIRECT_URI', 'https://app.hung.codes')
}

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

@app.before_request
def log_request_info():
    """Log request headers and body for debugging purposes."""
    logger.info('Headers: %s', dict(request.headers))
    logger.info('Body: %s', request.get_data())

@app.route('/')
def index():
    """Render the public homepage."""
    return render_template('index.html')


@app.route('/profile')
def profile():
    """
    Render the protected profile page after validating JWT tokens.
    This endpoint validates the JWT token from ALB and extracts user information.
    """
    user_info = {}
    
    try:
        if 'x-amzn-oidc-data' in request.headers:
            # Step 1: Extract and validate the JWT token
            encoded_jwt = request.headers.get('x-amzn-oidc-data')
            jwt_headers = encoded_jwt.split('.')[0]
            
            # Fix padding for base64 decoding
            jwt_headers += '=' * (-len(jwt_headers) % 4)
            decoded_jwt_headers = base64.b64decode(jwt_headers)
            decoded_jwt_headers = decoded_jwt_headers.decode("utf-8")
            decoded_json = json.loads(decoded_jwt_headers)
            
            # Validate the signer
            received_alb_arn = decoded_json['signer']
            logger.info(f"Received ALB ARN: {received_alb_arn}")
            logger.info(f"Expected ALB ARN: {config['alb_arn']}")
            
            if config['alb_arn'] != received_alb_arn:
                logger.error("Invalid Signer")
                return "Authentication error: Invalid token signer", 401
            
            # Step 2: Get the key ID from JWT headers
            kid = decoded_json['kid']
            
            # Step 3: Get the public key from ALB regional endpoint
            url = f"https://public-keys.auth.elb.{config['region']}.amazonaws.com/{kid}"
            logger.info(f"Fetching public key from: {url}")
            req = requests.get(url)
            pub_key = req.text
            
            # Step 4: Decode the JWT payload
            jwt_decoder = PyJWT()
            payload = jwt_decoder.decode(encoded_jwt, pub_key, algorithms=['ES256'])
            
            # Extract user information from payload
            user_info = {
                'email': payload.get('email', 'Not provided'),
                'name': payload.get('name', 'Not provided'),
                'sub': payload.get('sub', 'Not provided')
            }
            
            logger.info(f"User authenticated: {user_info}")
            
    except Exception as e:
        logger.error(f"Error processing JWT: {str(e)}")
        user_info = {'error': str(e)}
    
    return render_template('profile.html', user_info=user_info)


@app.route('/logout')
def logout():
    """
    Handle user logout by redirecting to Cognito logout URL.
    This will invalidate the user's session and redirect to the specified URL.
    """
    logout_url = f"https://{config['cognito_domain']}/logout?client_id={config['client_id']}&logout_uri={config['logout_redirect_uri']}"
    logger.info(f"Redirecting to logout URL: {logout_url}")
    return redirect(logout_url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
