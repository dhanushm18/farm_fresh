from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # in kg
    unit = db.Column(db.String(10), default='kg')
    category = db.Column(db.String(50))  # e.g., 'paddy', 'wheat', 'rice', etc.
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Keys
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True, cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.name}>'
