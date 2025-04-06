#!/bin/bash
# EC2 User Data script for Amazon Linux 2023
# Updates system and installs necessary dependencies

# Update system packages
dnf update -y

# Install Python, pip, git and other required packages
dnf install -y python3 python3-pip git nginx

# Create directory for application
mkdir -p /opt/flask-app

# Clone the application (replace with your actual repository if needed)
git clone https://github.com/yourusername/flask-oidc-client-demo.git /opt/flask-app

# Alternative: If you're deploying code via other means (e.g., AWS CodeDeploy)
# the below commands assume code is already in /opt/flask-app

# Set up virtual environment
python3 -m venv /opt/flask-app/venv
source /opt/flask-app/venv/bin/activate

# Install application dependencies
pip install -r /opt/flask-app/requirements.txt

# Create systemd service file for the application
cat > /etc/systemd/system/flask-app.service << 'EOL'
[Unit]
Description=Flask Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/opt/flask-app
ExecStart=/opt/flask-app/venv/bin/gunicorn -b 127.0.0.1:5000 -w 4 'app:app'
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# Configure Nginx as a reverse proxy
cat > /etc/nginx/conf.d/flask-app.conf << 'EOL'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOL

# Remove default nginx config
rm -f /etc/nginx/conf.d/default.conf

# Enable and start services
systemctl enable nginx
systemctl start nginx
systemctl enable flask-app
systemctl start flask-app

# Set proper permissions
chown -R ec2-user:ec2-user /opt/flask-app

echo "Installation completed" 