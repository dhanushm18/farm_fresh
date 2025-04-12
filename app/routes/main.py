from flask import Blueprint, render_template, redirect, url_for
from app.models import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get featured products
    featured_products = Product.query.limit(6).all()
    return render_template('index.html', products=featured_products)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')
