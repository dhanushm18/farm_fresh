from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'farmer', 'customer', or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Farmer specific fields
    farm_name = db.Column(db.String(100))
    farm_location = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    # Relationships
    products = db.relationship('Product', backref='seller', lazy=True)
    orders_placed = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.customer_id')
    orders_received = db.relationship('Order', backref='farmer', lazy=True, foreign_keys='Order.farmer_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
