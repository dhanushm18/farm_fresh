from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Order
from app.forms.product import ProductForm
import os
from werkzeug.utils import secure_filename
import uuid

farmer = Blueprint('farmer', __name__, url_prefix='/farmer')

# Configure upload settings
UPLOAD_FOLDER = os.path.join('app', 'static', 'images', 'products')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        # Create a unique filename to prevent overwriting
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"

        # Ensure the upload folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        # Return the relative path for storing in the database
        # Use forward slashes for URLs
        return 'images/products/' + unique_filename

    return None

@farmer.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type != 'farmer':
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    products = Product.query.filter_by(seller_id=current_user.id).all()
    recent_orders = Order.query.filter_by(farmer_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()

    return render_template('farmer/dashboard.html', products=products, orders=recent_orders)

@farmer.route('/products')
@login_required
def products():
    if current_user.user_type != 'farmer':
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    products = Product.query.filter_by(seller_id=current_user.id).all()
    return render_template('farmer/products.html', products=products)

@farmer.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.user_type != 'farmer':
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data,
            category=form.category.data,
            seller_id=current_user.id
        )

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image_path = save_image(file)
                if image_path:
                    product.image_url = image_path
                    print(f"Image saved at: {image_path}")
                else:
                    flash('Invalid image format. Please upload a valid image (PNG, JPG, JPEG, GIF).', 'warning')

        db.session.add(product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('farmer.products'))

    return render_template('farmer/add_product.html', form=form)

@farmer.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.user_type != 'farmer':
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    product = Product.query.get_or_404(id)

    # Check if the product belongs to the current user
    if product.seller_id != current_user.id:
        flash('You do not have permission to edit this product.', 'danger')
        return redirect(url_for('farmer.products'))

    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.category = form.category.data

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image_path = save_image(file)
                if image_path:
                    # Store the old image path for deletion if needed
                    old_image_path = product.image_url

                    # TODO: Delete the old image file if needed
                    # This could be implemented similar to the delete_product function

                    # Update the product with the new image path
                    product.image_url = image_path
                    print(f"Image updated at: {image_path}")

                    # TODO: Delete the old image file if needed
                else:
                    flash('Invalid image format. Please upload a valid image (PNG, JPG, JPEG, GIF).', 'warning')

        db.session.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('farmer.products'))

    return render_template('farmer/edit_product.html', form=form, product=product)

@farmer.route('/products/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    print(f"Delete product request received for product ID: {id}")

    if current_user.user_type != 'farmer':
        print(f"Access denied: User {current_user.id} is not a farmer")
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    product = Product.query.get_or_404(id)
    print(f"Found product: {product.name} (ID: {product.id})")

    # Check if the product belongs to the current user
    if product.seller_id != current_user.id:
        print(f"Permission denied: Product belongs to user {product.seller_id}, not {current_user.id}")
        flash('You do not have permission to delete this product.', 'danger')
        return redirect(url_for('farmer.products'))

    try:
        # Check if the product is referenced in any orders
        if product.order_items and len(product.order_items) > 0:
            print(f"Product {product.name} is referenced in {len(product.order_items)} order items")
            # Delete all order items associated with this product
            for item in product.order_items:
                print(f"Deleting order item {item.id} from order {item.order_id}")
                db.session.delete(item)
            db.session.commit()
            print(f"All order items for product {product.name} deleted")

        # Store the image path for deletion if it exists
        image_path = product.image_url
        print(f"Preparing to delete product {product.name} with image: {image_path}")

        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()
        print(f"Product {product.name} deleted from database")

        # Delete the image file if it exists
        if image_path:
            try:
                file_path = os.path.join('app', 'static', image_path)
                print(f"Checking for image file at: {file_path}")
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted image file: {file_path}")
                else:
                    print(f"Image file not found: {file_path}")
            except Exception as e:
                print(f"Error deleting image file: {str(e)}")

        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting product: {str(e)}")
        flash(f'An error occurred while deleting the product: {str(e)}', 'danger')

    print("Redirecting to products page")
    return redirect(url_for('farmer.products'))

@farmer.route('/orders')
@login_required
def orders():
    if current_user.user_type != 'farmer':
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    orders = Order.query.filter_by(farmer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('farmer/orders.html', orders=orders)

@farmer.route('/orders/<int:id>')
@login_required
def order_details(id):
    if current_user.user_type != 'farmer':
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    order = Order.query.get_or_404(id)

    # Check if the order belongs to the current user
    if order.farmer_id != current_user.id:
        flash('You do not have permission to view this order.', 'danger')
        return redirect(url_for('farmer.orders'))

    return render_template('farmer/order_details.html', order=order)

@farmer.route('/orders/update-status/<int:id>', methods=['POST'])
@login_required
def update_order_status(id):
    if current_user.user_type != 'farmer':
        flash('Access denied. Farmer account required.', 'danger')
        return redirect(url_for('main.index'))

    order = Order.query.get_or_404(id)

    # Check if the order belongs to the current user
    if order.farmer_id != current_user.id:
        flash('You do not have permission to update this order.', 'danger')
        return redirect(url_for('farmer.orders'))

    status = request.form.get('status')
    if status in ['pending', 'paid', 'shipped', 'delivered', 'cancelled']:
        order.status = status
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    else:
        flash('Invalid status.', 'danger')

    return redirect(url_for('farmer.order_details', id=id))
