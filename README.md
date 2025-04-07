# Flask Application with Zero-code Authentication Demo

A simple Flask application demonstrating zero-code authentication where the load balancer handles the authentication process.

Implementation details: https://dev.to/hoangquochung1110/deploy-oidc-authentication-on-aws-with-no-coding-using-aws-cognito-and-application-load-balancer-1g8o

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Start the application:
```
python app.py
```

The application will be available at http://localhost:5000.

## Features

- Zero-code authentication - authentication is handled by the load balancer
- No OIDC client implementation needed in the application code
- User profile display with information passed from the load balancer
- Simplified application architecture focusing on business logic

## Project Structure

The project has a simple structure with no authentication code in the application itself:

```
.
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── index.html      # Landing page
│   └── profile.html    # User profile page
└── .env                # Environment configuration
```

## How It Works

In this demonstration:

1. The load balancer acts as the authentication service
2. When a user accesses a protected resource, the load balancer:
   - Intercepts the request
   - Redirects to an authentication provider if needed
   - Handles all OIDC/authentication flows
   - Passes user information to the application

3. The application focuses solely on its core functionality, with no authentication code

## Benefits of Zero-code Authentication

- **Simplified Application Code**: No need to implement and maintain authentication code
- **Centralized Security**: Authentication is managed at the infrastructure level
- **Reduced Dependencies**: No authentication libraries required in the application
- **Consistent Security**: Uniform authentication across multiple applications
- **Easier Maintenance**: Authentication updates happen at the load balancer level

## Configuration

Because authentication is handled by the load balancer, minimal configuration is needed in the application itself.

## Environment Setup

For demonstration purposes, the application expects the load balancer to pass user information via headers or environment variables, which are then used to display user details in the profile page. 