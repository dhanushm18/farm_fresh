from app import create_app, db
from app.models import User, Product
import random

def init_db():
    app = create_app()
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Check if there are already users in the database
        if User.query.count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create farmer users
        farmers = [
            {
                'username': 'farmer1',
                'email': 'farmer1@example.com',
                'password': 'password',
                'user_type': 'farmer',
                'farm_name': 'Green Fields Farm',
                'farm_location': 'Punjab, India',
                'phone': '9876543210'
            },
            {
                'username': 'farmer2',
                'email': 'farmer2@example.com',
                'password': 'password',
                'user_type': 'farmer',
                'farm_name': 'Sunrise Organics',
                'farm_location': 'Haryana, India',
                'phone': '9876543211'
            }
        ]
        
        for farmer_data in farmers:
            farmer = User(
                username=farmer_data['username'],
                email=farmer_data['email'],
                user_type=farmer_data['user_type'],
                farm_name=farmer_data['farm_name'],
                farm_location=farmer_data['farm_location'],
                phone=farmer_data['phone']
            )
            farmer.set_password(farmer_data['password'])
            db.session.add(farmer)
        
        # Create customer users
        customers = [
            {
                'username': 'customer1',
                'email': 'customer1@example.com',
                'password': 'password',
                'user_type': 'customer'
            },
            {
                'username': 'customer2',
                'email': 'customer2@example.com',
                'password': 'password',
                'user_type': 'customer'
            }
        ]
        
        for customer_data in customers:
            customer = User(
                username=customer_data['username'],
                email=customer_data['email'],
                user_type=customer_data['user_type']
            )
            customer.set_password(customer_data['password'])
            db.session.add(customer)
        
        # Commit users to get their IDs
        db.session.commit()
        
        # Get farmer IDs
        farmer1 = User.query.filter_by(username='farmer1').first()
        farmer2 = User.query.filter_by(username='farmer2').first()
        
        # Create products
        products = [
            {
                'name': 'Premium Basmati Rice',
                'description': 'High-quality aromatic basmati rice grown in the foothills of the Himalayas. Perfect for biryanis and pulao.',
                'price': 120.0,
                'quantity': 500.0,
                'category': 'rice',
                'seller_id': farmer1.id
            },
            {
                'name': 'Organic Brown Rice',
                'description': 'Nutrient-rich brown rice grown without pesticides. High in fiber and essential minerals.',
                'price': 90.0,
                'quantity': 300.0,
                'category': 'rice',
                'seller_id': farmer1.id
            },
            {
                'name': 'Whole Wheat',
                'description': 'Stone-ground whole wheat with all the bran and germ intact. Perfect for making chapatis and rotis.',
                'price': 45.0,
                'quantity': 400.0,
                'category': 'wheat',
                'seller_id': farmer1.id
            },
            {
                'name': 'Organic Paddy',
                'description': 'Freshly harvested organic paddy from our sustainable farm. Can be processed as per your requirements.',
                'price': 35.0,
                'quantity': 1000.0,
                'category': 'paddy',
                'seller_id': farmer2.id
            },
            {
                'name': 'Pearl Millet (Bajra)',
                'description': 'Nutritious pearl millet rich in protein, fiber, and essential minerals. Great for making rotis and porridge.',
                'price': 60.0,
                'quantity': 250.0,
                'category': 'millet',
                'seller_id': farmer2.id
            },
            {
                'name': 'Yellow Corn',
                'description': 'Sweet yellow corn kernels, perfect for making corn flour or direct cooking.',
                'price': 50.0,
                'quantity': 350.0,
                'category': 'corn',
                'seller_id': farmer2.id
            }
        ]
        
        for product_data in products:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity'],
                category=product_data['category'],
                seller_id=product_data['seller_id']
            )
            db.session.add(product)
        
        # Commit all changes
        db.session.commit()
        
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db()
