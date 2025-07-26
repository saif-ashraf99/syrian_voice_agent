import logging
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.users.services import UserService

logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@cross_origin()
def get_users():
    """Get all users"""
    try:
        users = UserService.get_all_users()
        return jsonify(users)
    except Exception as e:
        logger.error(f"Get users error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users', methods=['POST'])
@cross_origin()
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        email = data.get('email')
        
        if not username or not email:
            return jsonify({'error': 'Username and email are required'}), 400
        
        user = UserService.create_user(username, email)
        return jsonify(user), 201
        
    except ValueError as e:
        logger.warning(f"User creation validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Create user error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user(user_id):
    """Get user by ID"""
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify(user)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Get user error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@cross_origin()
def update_user(user_id):
    """Update user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        email = data.get('email')
        
        user = UserService.update_user(user_id, username, email)
        return jsonify(user)
        
    except ValueError as e:
        logger.warning(f"User update validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Update user error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@cross_origin()
def delete_user(user_id):
    """Delete user"""
    try:
        UserService.delete_user(user_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Delete user error: {e}")
        return jsonify({'error': 'Internal server error'}), 500