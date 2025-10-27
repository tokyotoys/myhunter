from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import secrets

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='static')

# Configure secret key for session management
app.secret_key = secrets.token_hex(16)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import and register blueprints
from routes.location import location_bp
from routes.admin import admin_bp

app.register_blueprint(location_bp)
app.register_blueprint(admin_bp)

# Default route
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Admin template routes
@app.route('/admin/login')
def admin_login_template():
    return app.send_static_file('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard_template():
    if session.get('admin_logged_in'):
        return app.send_static_file('admin/dashboard.html')
    else:
        return app.redirect('/admin/login')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
