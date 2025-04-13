from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Initialize CSRF Protection
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.farmer import farmer
    from app.routes.customer import customer
    from app.routes.payment import payment
    from app.routes.admin import admin

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(farmer)
    app.register_blueprint(customer)
    app.register_blueprint(payment)
    app.register_blueprint(admin)

    # Create database tables and initialize admin user
    with app.app_context():
        db.create_all()

        # Check if admin user exists
        from app.models.user import User
        from app.models.product import Product

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

        # Seed sample data if database is empty
        if User.query.count() <= 1 and Product.query.count() == 0:  # Only admin user exists
            # Create farmer users
            farmers = [
                {
                    'username': 'farmer1',
                    'email': 'farmer1@example.com',
                    'password': 'password123',
                    'farm_name': 'Green Valley Farm',
                    'farm_location': 'Karnataka, India',
                    'phone': '9876543210'
                },
                {
                    'username': 'farmer2',
                    'email': 'farmer2@example.com',
                    'password': 'password123',
                    'farm_name': 'Sunshine Organics',
                    'farm_location': 'Tamil Nadu, India',
                    'phone': '9876543211'
                }
            ]

            farmer_objects = []
            for farmer_data in farmers:
                farmer = User(
                    username=farmer_data['username'],
                    email=farmer_data['email'],
                    user_type='farmer',
                    farm_name=farmer_data['farm_name'],
                    farm_location=farmer_data['farm_location'],
                    phone=farmer_data['phone']
                )
                farmer.set_password(farmer_data['password'])
                db.session.add(farmer)
                farmer_objects.append(farmer)

            # Create customer users
            customers = [
                {
                    'username': 'customer1',
                    'email': 'customer1@example.com',
                    'password': 'password123'
                },
                {
                    'username': 'customer2',
                    'email': 'customer2@example.com',
                    'password': 'password123'
                }
            ]

            for customer_data in customers:
                customer = User(
                    username=customer_data['username'],
                    email=customer_data['email'],
                    user_type='customer'
                )
                customer.set_password(customer_data['password'])
                db.session.add(customer)

            db.session.commit()

            # Get farmer IDs after commit
            farmer1 = User.query.filter_by(username='farmer1').first()
            farmer2 = User.query.filter_by(username='farmer2').first()

            # Create products
            products = [
                {
                    'name': 'Organic Rice',
                    'description': 'Freshly harvested organic rice from our farm. No pesticides used.',
                    'price': 80.00,
                    'quantity': 100,
                    'category': 'Grains',
                    'seller_id': farmer1.id
                },
                {
                    'name': 'Basmati Rice',
                    'description': 'Premium quality basmati rice with aromatic flavor.',
                    'price': 120.00,
                    'quantity': 50,
                    'category': 'Grains',
                    'seller_id': farmer1.id
                },
                {
                    'name': 'Organic Wheat',
                    'description': 'Stone-ground organic wheat for healthy baking.',
                    'price': 60.00,
                    'quantity': 75,
                    'category': 'Grains',
                    'seller_id': farmer2.id
                },
                {
                    'name': 'Fresh Vegetables Pack',
                    'description': 'Assorted fresh vegetables harvested daily.',
                    'price': 150.00,
                    'quantity': 30,
                    'category': 'Vegetables',
                    'seller_id': farmer2.id
                },
                {
                    'name': 'Organic Pulses Mix',
                    'description': 'Mix of various organic pulses for a balanced diet.',
                    'price': 95.00,
                    'quantity': 40,
                    'category': 'Pulses',
                    'seller_id': farmer1.id
                }
            ]

            for product_data in products:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    quantity=product_data['quantity'],
                    category=product_data['category'],
                    seller_id=product_data['seller_id'],
                    image_url='images/default-product.jpg'  # Default image
                )
                db.session.add(product)

            db.session.commit()
            print("Sample data added successfully!")

    return app
