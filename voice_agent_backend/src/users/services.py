import logging
from .models import User, db

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def get_all_users():
        """Get all users"""
        try:
            users = User.query.all()
            return [user.to_dict() for user in users]
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            raise
    
    @staticmethod
    def create_user(username, email):
        """Create a new user"""
        try:
            # Validate input
            if not username or not email:
                raise ValueError("Username and email are required")
            
            # Check if user already exists
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    raise ValueError("Username already exists")
                if existing_user.email == email:
                    raise ValueError("Email already exists")
            
            # Create new user
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"User created: {username}")
            return user.to_dict()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {e}")
            raise
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
            return user.to_dict()
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise
    
    @staticmethod
    def update_user(user_id, username=None, email=None):
        """Update user"""
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Check for duplicate username/email if being updated
            if username and username != user.username:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    raise ValueError("Username already exists")
                user.username = username
            
            if email and email != user.email:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    raise ValueError("Email already exists")
                user.email = email
            
            db.session.commit()
            
            logger.info(f"User updated: {user_id}")
            return user.to_dict()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            raise
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
            
            db.session.delete(user)
            db.session.commit()
            
            logger.info(f"User deleted: {user_id}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting user {user_id}: {e}")
            raise