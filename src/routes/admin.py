from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import hashlib
import os
import json
import time

admin_bp = Blueprint('admin', __name__)

# Admin credentials
ADMIN_USERNAME = "sinner"
# Store password hash instead of plaintext
ADMIN_PASSWORD_HASH = hashlib.sha256("Cetemiri?7".encode()).hexdigest()

# In-memory storage for visitor data (in production, use a database)
visitors_data = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin', methods=['GET'])
def admin_redirect():
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials
        if username == ADMIN_USERNAME and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            error = "Invalid credentials. Please try again."
    
    return render_template('admin/login.html', error=error)

@admin_bp.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/admin/logout', methods=['GET'])
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin/api/visitors', methods=['GET'])
@login_required
def get_visitors():
    """API endpoint to get all visitor data for the map"""
    return jsonify(list(visitors_data.values()))

@admin_bp.route('/admin/api/stats', methods=['GET'])
@login_required
def get_stats():
    """API endpoint to get visitor statistics"""
    total_visitors = len(visitors_data)
    browser_stats = {}
    os_stats = {}
    
    for visitor in visitors_data.values():
        browser = visitor.get('browser', 'Unknown')
        os_name = visitor.get('os', 'Unknown')
        
        if browser in browser_stats:
            browser_stats[browser] += 1
        else:
            browser_stats[browser] = 1
            
        if os_name in os_stats:
            os_stats[os_name] += 1
        else:
            os_stats[os_name] = 1
    
    return jsonify({
        'total_visitors': total_visitors,
        'browser_stats': browser_stats,
        'os_stats': os_stats
    })

# Function to register a visitor (called from location.py)
def register_visitor(visitor_id, location_data, user_agent_data):
    """Register or update a visitor in the tracking system"""
    if visitor_id in visitors_data:
        # Update existing visitor
        visitors_data[visitor_id].update({
            'last_seen': time.time(),
            'location': location_data,
            **user_agent_data
        })
    else:
        # New visitor
        visitors_data[visitor_id] = {
            'id': visitor_id,
            'first_seen': time.time(),
            'last_seen': time.time(),
            'location': location_data,
            **user_agent_data
        }
    
    return visitors_data[visitor_id]
