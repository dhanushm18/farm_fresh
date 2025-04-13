import os
from app import create_app, db
from app.models.user import User

def init_database():
    """Initialize the database and create an admin user if it doesn't exist."""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(user_type='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@farmfresh.com',
                user_type='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    init_database()
