from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app import db
from app.models import Product, CartItem, Order, OrderItem
import uuid

customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route('/products')
def products():
    category = request.args.get('category')
    search = request.args.get('search')

    query = Product.query

    if category:
        query = query.filter_by(category=category)

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    products = query.all()
    categories = db.session.query(Product.category).distinct().all()

    return render_template('customer/products.html', products=products, categories=categories)

@customer.route('/product/<int:id>')
def product_details(id):
    product = Product.query.get_or_404(id)
    return render_template('customer/product_details.html', product=product)

@customer.route('/cart')
@login_required
def cart():
    if current_user.user_type != 'customer':
        flash('Access denied. Customer account required.', 'danger')
        return redirect(url_for('main.index'))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render_template('customer/cart.html', cart_items=cart_items, total=total)

@customer.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if current_user.user_type != 'customer':
        flash('Access denied. Customer account required.', 'danger')
        return redirect(url_for('main.index'))

    product = Product.query.get_or_404(product_id)
    quantity = float(request.form.get('quantity', 1))

    # Check if the product is already in the cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    flash('Product added to cart!', 'success')
    return redirect(url_for('customer.cart'))

@customer.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    if current_user.user_type != 'customer':
        flash('Access denied. Customer account required.', 'danger')
        return redirect(url_for('main.index'))

    cart_item = CartItem.query.get_or_404(item_id)

    # Check if the cart item belongs to the current user
    if cart_item.user_id != current_user.id:
        flash('You do not have permission to update this cart item.', 'danger')
        return redirect(url_for('customer.cart'))

    quantity = float(request.form.get('quantity', 1))

    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity

    db.session.commit()

    flash('Cart updated!', 'success')
    return redirect(url_for('customer.cart'))

@customer.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    if current_user.user_type != 'customer':
        flash('Access denied. Customer account required.', 'danger')
        return redirect(url_for('main.index'))

    cart_item = CartItem.query.get_or_404(item_id)

    # Check if the cart item belongs to the current user
    if cart_item.user_id != current_user.id:
        flash('You do not have permission to remove this cart item.', 'danger')
        return redirect(url_for('customer.cart'))

    db.session.delete(cart_item)
    db.session.commit()

    flash('Item removed from cart!', 'success')
    return redirect(url_for('customer.cart'))

@customer.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if current_user.user_type != 'customer':
        flash('Access denied. Customer account required.', 'danger')
        return redirect(url_for('main.index'))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('customer.cart'))

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        try:
            # Construct full address from form fields
            address = f"{request.form.get('address')}, {request.form.get('city')}, {request.form.get('state')} - {request.form.get('pincode')}"
            phone = request.form.get('phone')

            # Group cart items by farmer
            farmer_items = {}
            for item in cart_items:
                farmer_id = item.product.seller_id
                if farmer_id not in farmer_items:
                    farmer_items[farmer_id] = []
                farmer_items[farmer_id].append(item)

            # Create an order for each farmer
            orders = []
            for farmer_id, items in farmer_items.items():
                order_total = sum(item.product.price * item.quantity for item in items)

                # Create order
                order = Order(
                    order_number=str(uuid.uuid4().hex)[:10].upper(),
                    total_amount=order_total,
                    customer_id=current_user.id,
                    farmer_id=farmer_id,
                    shipping_address=address
                )

                db.session.add(order)
                db.session.flush()  # Get the order ID
                orders.append(order)

                # Create order items
                for item in items:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                    db.session.add(order_item)

                    # Update product quantity
                    product = item.product
                    product.quantity -= item.quantity

                    # Remove item from cart
                    db.session.delete(item)

            db.session.commit()

            # If there's only one order, redirect to payment for that order
            if len(orders) == 1:
                return redirect(url_for('payment.process_payment', order_id=orders[0].id))

            # If there are multiple orders, redirect to the first one for now
            # In a real application, you might want to handle multiple payments differently
            if len(orders) > 1:
                flash('Multiple orders created. You will be redirected to pay for each order separately.', 'info')
                return redirect(url_for('payment.process_payment', order_id=orders[0].id))

            # If no orders were created (shouldn't happen)
            flash('No orders were created. Please try again.', 'danger')
            return redirect(url_for('customer.cart'))

        except Exception as e:
            db.session.rollback()
            print(f"Error creating order: {str(e)}")
            flash(f'An error occurred while processing your order: {str(e)}', 'danger')
            return redirect(url_for('customer.checkout'))

    return render_template('customer/checkout.html', cart_items=cart_items, total=total)

@customer.route('/orders')
@login_required
def orders():
    if current_user.user_type != 'customer':
        flash('Access denied. Customer account required.', 'danger')
        return redirect(url_for('main.index'))

    orders = Order.query.filter_by(customer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/orders.html', orders=orders)

@customer.route('/orders/<int:id>')
@login_required
def order_details(id):
    if current_user.user_type != 'customer':
        flash('Access denied. Customer account required.', 'danger')
        return redirect(url_for('main.index'))

    order = Order.query.get_or_404(id)

    # Check if the order belongs to the current user
    if order.customer_id != current_user.id:
        flash('You do not have permission to view this order.', 'danger')
        return redirect(url_for('customer.orders'))

    return render_template('customer/order_details.html', order=order)
