from flask import Blueprint, request, jsonify, make_response
import requests
import json

location_bp = Blueprint('location', __name__)

@location_bp.route('/track', methods=['GET'])
def track_location():
    """
    Track visitor location based on IP address and return detailed location data.
    This endpoint uses the ipinfo.io API to get location data including street information.
    """
    # Get visitor's IP address
    ip_address = request.remote_addr
    if ip_address == '127.0.0.1':
        # For local testing, use a default IP
        ip_address = '8.8.8.8'  # Google's public DNS as example
    
    # Call ipinfo.io API to get location data
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        if response.status_code == 200:
            location_data = response.json()
            
            # Create response with location data
            resp = make_response(jsonify({
                'success': True,
                'location': location_data
            }))
            
            # Set cookie with location data (expires in 30 days)
            max_age = 30 * 24 * 60 * 60  # 30 days in seconds
            resp.set_cookie('user_location', json.dumps(location_data), max_age=max_age, httponly=True, samesite='Strict')
            
            return resp
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve location data',
                'status_code': response.status_code
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@location_bp.route('/current', methods=['GET'])
def get_current_location():
    """
    Retrieve the current location data from the cookie if available.
    """
    location_cookie = request.cookies.get('user_location')
    
    if location_cookie:
        try:
            location_data = json.loads(location_cookie)
            return jsonify({
                'success': True,
                'location': location_data,
                'source': 'cookie'
            })
        except json.JSONDecodeError:
            return jsonify({
                'success': False,
                'error': 'Invalid location data in cookie'
            }), 400
    else:
        return jsonify({
            'success': False,
            'error': 'No location data found in cookie'
        }), 404

@location_bp.route('/clear', methods=['POST'])
def clear_location():
    """
    Clear the location cookie.
    """
    resp = make_response(jsonify({
        'success': True,
        'message': 'Location cookie cleared'
    }))
    resp.delete_cookie('user_location')
    return resp
