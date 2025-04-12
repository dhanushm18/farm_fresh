from app import create_app, db
from app.models import User

def create_admin_user(username, email, password):
    app = create_app()
    with app.app_context():
        # Check if admin user already exists
        existing_admin = User.query.filter_by(user_type='admin').first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username} ({existing_admin.email})")
            return
        
        # Create new admin user
        admin = User(
            username=username,
            email=email,
            user_type='admin'
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"Admin user created successfully: {username} ({email})")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 4:
        print("Usage: python create_admin.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_admin_user(username, email, password)
