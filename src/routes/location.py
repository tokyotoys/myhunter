from flask import Blueprint, request, jsonify, make_response
import requests
import json
import uuid
from datetime import datetime, timedelta
import re

# Import the admin visitor registration function
try:
    from routes.admin import register_visitor
except ImportError:
    # Fallback if admin module not available
    def register_visitor(visitor_id, location_data, user_agent_data):
        return None

location_bp = Blueprint('location', __name__)

def parse_user_agent(user_agent_string):
    """Parse user agent string to extract browser, OS and device information"""
    ua_data = {
        'browser': 'Unknown',
        'os': 'Unknown',
        'device': 'Unknown'
    }
    
    # Browser detection
    if 'Chrome' in user_agent_string and 'Chromium' not in user_agent_string:
        ua_data['browser'] = 'Chrome'
    elif 'Firefox' in user_agent_string:
        ua_data['browser'] = 'Firefox'
    elif 'Safari' in user_agent_string and 'Chrome' not in user_agent_string:
        ua_data['browser'] = 'Safari'
    elif 'Edge' in user_agent_string:
        ua_data['browser'] = 'Edge'
    elif 'MSIE' in user_agent_string or 'Trident/' in user_agent_string:
        ua_data['browser'] = 'Internet Explorer'
    elif 'Opera' in user_agent_string or 'OPR/' in user_agent_string:
        ua_data['browser'] = 'Opera'
    
    # OS detection
    if 'Windows' in user_agent_string:
        ua_data['os'] = 'Windows'
        match = re.search(r'Windows NT (\d+\.\d+)', user_agent_string)
        if match:
            nt_version = match.group(1)
            if nt_version == '10.0':
                ua_data['os'] = 'Windows 10/11'
            elif nt_version == '6.3':
                ua_data['os'] = 'Windows 8.1'
            elif nt_version == '6.2':
                ua_data['os'] = 'Windows 8'
            elif nt_version == '6.1':
                ua_data['os'] = 'Windows 7'
    elif 'Macintosh' in user_agent_string:
        ua_data['os'] = 'macOS'
    elif 'Linux' in user_agent_string and 'Android' not in user_agent_string:
        ua_data['os'] = 'Linux'
    elif 'Android' in user_agent_string:
        ua_data['os'] = 'Android'
        ua_data['device'] = 'Mobile'
    elif 'iPhone' in user_agent_string:
        ua_data['os'] = 'iOS'
        ua_data['device'] = 'iPhone'
    elif 'iPad' in user_agent_string:
        ua_data['os'] = 'iOS'
        ua_data['device'] = 'iPad'
    
    # Device type detection
    if 'Mobile' in user_agent_string:
        ua_data['device'] = 'Mobile'
    elif 'Tablet' in user_agent_string:
        ua_data['device'] = 'Tablet'
    elif ua_data['device'] == 'Unknown':
        ua_data['device'] = 'Desktop'
    
    return ua_data

@location_bp.route('/api/location/track', methods=['GET'])
def track_location():
    """Track user location based on IP address"""
    # Get user's IP address
    ip_address = request.remote_addr
    
    # For testing, use a fixed IP if we're in a local environment
    if ip_address == '127.0.0.1' or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
        ip_address = '8.8.8.8'  # Use Google's DNS as a test IP
    
    # Get or generate visitor ID from cookie
    visitor_id = request.cookies.get('visitor_id')
    if not visitor_id:
        visitor_id = str(uuid.uuid4())
    
    # Parse user agent
    user_agent_string = request.headers.get('User-Agent', '')
    user_agent_data = parse_user_agent(user_agent_string)
    
    try:
        # Call ipinfo.io API to get location data
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        location_data = response.json()
        
        # Register visitor with admin tracking system
        register_visitor(visitor_id, location_data, user_agent_data)
        
        # Set cookie with location data
        max_age = 30 * 24 * 60 * 60  # 30 days in seconds
        expires = datetime.utcnow() + timedelta(days=30)
        
        # Prepare response
        resp = make_response(jsonify({
            'success': True,
            'location': location_data,
            'visitor_id': visitor_id,
            'user_agent': user_agent_data,
            'cookie_info': {
                'name': 'user_location',
                'value': json.dumps(location_data),
                'max_age': max_age,
                'expires': expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            }
        }))
        
        # Set cookies
        resp.set_cookie('user_location', json.dumps(location_data), max_age=max_age)
        resp.set_cookie('visitor_id', visitor_id, max_age=365*24*60*60)  # 1 year for visitor ID
        
        return resp
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
