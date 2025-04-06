import os
from flask import Flask, redirect, url_for, render_template, request


# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

@app.route('/')
def index():
    """Render the public homepage."""
    return render_template('index.html')


@app.route('/profile')
def profile():
    """Render user profile page."""
    user_info = {}
    return render_template('profile.html', user_info=user_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
