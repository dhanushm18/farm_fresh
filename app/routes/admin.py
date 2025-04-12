from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Product, Order, OrderItem
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def dashboard():
    # Count statistics for dashboard
    user_count = User.query.count()
    farmer_count = User.query.filter_by(user_type='farmer').count()
    customer_count = User.query.filter_by(user_type='customer').count()
    product_count = Product.query.count()
    order_count = Order.query.count()
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        user_count=user_count,
        farmer_count=farmer_count,
        customer_count=customer_count,
        product_count=product_count,
        order_count=order_count,
        recent_orders=recent_orders
    )

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:id>')
@login_required
@admin_required
def user_details(id):
    user = User.query.get_or_404(id)
    return render_template('admin/user_details.html', user=user)

@admin.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    # Don't allow deleting yourself
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('admin.users'))

@admin.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin.route('/products/<int:id>')
@login_required
@admin_required
def product_details(id):
    product = Product.query.get_or_404(id)
    return render_template('admin/product_details.html', product=product)

@admin.route('/products/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash(f'Product {product.name} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'danger')
    
    return redirect(url_for('admin.products'))

@admin.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/orders/<int:id>')
@login_required
@admin_required
def order_details(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_details.html', order=order)

@admin.route('/orders/<int:id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    status = request.form.get('status')
    
    if status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = status
        db.session.commit()
        flash(f'Order status updated to {status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
    
    return redirect(url_for('admin.order_details', id=id))
