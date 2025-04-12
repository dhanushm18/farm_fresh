from app import create_app
from app.models import Product

app = create_app()
with app.app_context():
    products = Product.query.all()
    print('Products:')
    for p in products:
        print(f'ID: {p.id}, Name: {p.name}, Image URL: {p.image_url}')
