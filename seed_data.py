from app import create_app, db
from app.models.user import User
from app.models.product import Product
import os
import random

def seed_database():
    """Seed the database with sample data for demonstration."""
    app = create_app()
    with app.app_context():
        # Check if we already have data
        if User.query.count() > 1:  # More than just the admin user
            print("Database already has data. Skipping seed.")
            return
        
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
        
        # Create products
        products = [
            {
                'name': 'Organic Rice',
                'description': 'Freshly harvested organic rice from our farm. No pesticides used.',
                'price': 80.00,
                'quantity': 100,
                'category': 'Grains',
                'seller_id': farmer_objects[0].id
            },
            {
                'name': 'Basmati Rice',
                'description': 'Premium quality basmati rice with aromatic flavor.',
                'price': 120.00,
                'quantity': 50,
                'category': 'Grains',
                'seller_id': farmer_objects[0].id
            },
            {
                'name': 'Organic Wheat',
                'description': 'Stone-ground organic wheat for healthy baking.',
                'price': 60.00,
                'quantity': 75,
                'category': 'Grains',
                'seller_id': farmer_objects[1].id
            },
            {
                'name': 'Fresh Vegetables Pack',
                'description': 'Assorted fresh vegetables harvested daily.',
                'price': 150.00,
                'quantity': 30,
                'category': 'Vegetables',
                'seller_id': farmer_objects[1].id
            },
            {
                'name': 'Organic Pulses Mix',
                'description': 'Mix of various organic pulses for a balanced diet.',
                'price': 95.00,
                'quantity': 40,
                'category': 'Pulses',
                'seller_id': farmer_objects[0].id
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

if __name__ == '__main__':
    seed_database()
