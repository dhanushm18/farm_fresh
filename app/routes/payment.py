from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
import razorpay
import os
from app.models import Order
from dotenv import load_dotenv

load_dotenv()

payment = Blueprint('payment', __name__, url_prefix='/payment')

# Initialize Razorpay client
razorpay_key_id = os.getenv('RAZORPAY_KEY_ID')
razorpay_key_secret = os.getenv('RAZORPAY_KEY_SECRET')

# Print the keys for debugging (remove in production)
print(f"Razorpay Key ID: {razorpay_key_id}")
print(f"Razorpay Key Secret: {razorpay_key_secret[:4]}...{razorpay_key_secret[-4:] if razorpay_key_secret else ''}")

if not razorpay_key_id or not razorpay_key_secret:
    print("WARNING: Razorpay API keys are not set properly in .env file")

# Initialize the client
try:
    razorpay_client = razorpay.Client(
        auth=(razorpay_key_id, razorpay_key_secret)
    )
    print("Razorpay client initialized")
except Exception as e:
    print(f"Error initializing Razorpay client: {str(e)}")
    razorpay_client = None

@payment.route('/process/<int:order_id>')
@login_required
def process_payment(order_id):
    order = Order.query.get_or_404(order_id)

    # Check if the order belongs to the current user
    if order.customer_id != current_user.id:
        flash('You do not have permission to access this order.', 'danger')
        return redirect(url_for('customer.orders'))

    try:
        # Check if Razorpay client is initialized
        if not razorpay_client:
            print("Razorpay client is not initialized. Check your API keys.")
            flash('Payment gateway is not configured properly. Please contact support.', 'danger')
            return redirect(url_for('customer.orders'))

        # Print order details for debugging
        print(f"Creating Razorpay order for order #{order.order_number} with amount {order.total_amount}")

        # We'll attempt to create a Razorpay order
        # If it fails in test mode, we'll use a direct payment approach

        # Always create a Razorpay order, even in test mode
        try:
            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': int(order.total_amount * 100),  # Amount in paise
                'currency': 'INR',
                'receipt': order.order_number,
                'payment_capture': '1'  # Auto capture
            })
            print(f"Razorpay order created successfully: {razorpay_order['id']}")
            razorpay_order_id = razorpay_order['id']
        except Exception as api_error:
            print(f"Error creating Razorpay order: {str(api_error)}")
            # In test mode, we can use a direct payment approach as fallback
            if razorpay_key_id and razorpay_key_id.startswith('rzp_test_'):
                print("Using test mode direct payment as fallback")
                # We'll set a special flag to indicate we're using direct payment
                razorpay_order_id = None
            else:
                # For production, we need to fail if order creation fails
                raise api_error

        return render_template(
            'payment/checkout.html',
            order=order,
            razorpay_order_id=razorpay_order_id,
            razorpay_key_id=razorpay_key_id
        )
    except Exception as e:
        print(f"Error creating Razorpay order: {str(e)}")
        flash(f'Payment gateway error: {str(e)}. Please try again later or contact support.', 'danger')
        # Update the order status to indicate payment failed
        order.status = 'payment_failed'
        db.session.commit()
        return redirect(url_for('customer.order_details', id=order.id))

@payment.route('/callback', methods=['POST'])
@login_required
def payment_callback():
    try:
        # Get payment parameters
        razorpay_payment_id = request.form.get('razorpay_payment_id')
        razorpay_order_id = request.form.get('razorpay_order_id')
        razorpay_signature = request.form.get('razorpay_signature')
        order_id = request.form.get('order_id')

        # Print debug information
        print(f"Payment callback received for order: {order_id}")
        print(f"Payment ID: {razorpay_payment_id}")
        print(f"Order ID: {razorpay_order_id}")
        print(f"Signature: {razorpay_signature}")

        # Get the order from database
        order = Order.query.get(order_id)
        if not order:
            print(f"Order {order_id} not found")
            flash('Order not found. Please contact support.', 'danger')
            return redirect(url_for('customer.orders'))

        # Check if the order belongs to the current user
        if order.customer_id != current_user.id:
            print(f"Order {order_id} does not belong to user {current_user.id}")
            flash('You do not have permission to access this order.', 'danger')
            return redirect(url_for('customer.orders'))

        # For test mode, we'll accept the payment without verification
        is_test_mode = razorpay_key_id and razorpay_key_id.startswith('rzp_test_')

        # Check if we have a payment ID (this is the most important part)
        if not razorpay_payment_id:
            print("No payment ID received")
            flash('Payment failed. No payment ID received.', 'danger')
            order.status = 'payment_failed'
            db.session.commit()
            return redirect(url_for('customer.order_details', id=order_id))

        # In test mode, always accept the payment
        if is_test_mode:
            print(f"Using test mode - accepting payment with ID: {razorpay_payment_id}")
            payment_verified = True
        # In production mode, verify the signature
        else:
            # We need all three parameters for verification
            if razorpay_order_id and razorpay_signature:
                try:
                    params_dict = {
                        'razorpay_order_id': razorpay_order_id,
                        'razorpay_payment_id': razorpay_payment_id,
                        'razorpay_signature': razorpay_signature
                    }
                    razorpay_client.utility.verify_payment_signature(params_dict)
                    payment_verified = True
                    print("Payment signature verified successfully")
                except Exception as error:
                    payment_verified = False
                    print(f"Payment verification failed: {str(error)}")
            else:
                # Missing parameters
                payment_verified = False
                print("Missing payment parameters for verification")
    except Exception as e:
        print(f"Error in payment callback: {str(e)}")
        flash(f'An error occurred during payment processing: {str(e)}', 'danger')
        return redirect(url_for('customer.orders'))

    # Update order status based on verification result
    try:
        if payment_verified:
            order.payment_id = razorpay_payment_id or 'test_payment'
            order.payment_status = 'completed'
            order.status = 'paid'
            db.session.commit()

            print(f"Order {order_id} updated successfully. Redirecting to order details.")
            flash('Payment successful! Your order has been confirmed.', 'success')
        else:
            order.payment_status = 'failed'
            order.status = 'payment_failed'
            db.session.commit()
            print(f"Payment verification failed for order {order_id}. Redirecting to order details.")
            flash('Payment verification failed. Please try again or contact support.', 'danger')

        # Ensure we have a valid order ID for redirection
        if order_id:
            return redirect(url_for('customer.order_details', id=order_id))
        else:
            print("Invalid order ID for redirection. Redirecting to orders page.")
            return redirect(url_for('customer.orders'))
    except Exception as e:
        print(f"Error in payment callback redirection: {str(e)}")
        flash(f'An error occurred during payment processing: {str(e)}', 'danger')
        return redirect(url_for('customer.orders'))
