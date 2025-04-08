# Installation Guide

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

## Environment Setup

For demonstration purposes, the application expects the load balancer to pass user information via headers or environment variables, which are then used to display user details in the profile page.