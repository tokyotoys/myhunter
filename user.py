from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint to verify API is working.
    """
    return jsonify({
        'status': 'ok',
        'message': 'API is running'
    })
