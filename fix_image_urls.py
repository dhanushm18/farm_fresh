from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    products = Product.query.all()
    print('Fixing image URLs...')
    for p in products:
        if p.image_url:
            # Replace backslashes with forward slashes
            p.image_url = p.image_url.replace('\\', '/')
            print(f'Updated ID: {p.id}, Name: {p.name}, New Image URL: {p.image_url}')
    
    # Commit the changes
    db.session.commit()
    print('All image URLs fixed!')
