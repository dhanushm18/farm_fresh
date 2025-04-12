import unittest
from app import create_app, db
from app.models import User, Product

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create test users
            farmer = User(
                username='test_farmer',
                email='farmer@test.com',
                user_type='farmer',
                farm_name='Test Farm',
                farm_location='Test Location',
                phone='1234567890'
            )
            farmer.set_password('password')
            
            customer = User(
                username='test_customer',
                email='customer@test.com',
                user_type='customer'
            )
            customer.set_password('password')
            
            db.session.add(farmer)
            db.session.add(customer)
            db.session.commit()
            
            # Create test product
            product = Product(
                name='Test Rice',
                description='High quality rice for testing',
                price=50.0,
                quantity=100.0,
                category='rice',
                seller_id=farmer.id
            )
            db.session.add(product)
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FarmFresh', response.data)
    
    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About FarmFresh', response.data)
    
    def test_products_page(self):
        response = self.client.get('/customer/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Browse Products', response.data)
    
    def test_login(self):
        response = self.client.post('/login', data={
            'email': 'customer@test.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
    
    def test_register(self):
        response = self.client.post('/register', data={
            'username': 'new_user',
            'email': 'new@test.com',
            'password': 'password',
            'confirm_password': 'password',
            'user_type': 'customer'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

if __name__ == '__main__':
    unittest.main()
