# 🌾 FarmFresh - Direct from Farmers

**FarmFresh** is a comprehensive web application that connects farmers directly with customers, eliminating middlemen and ensuring fair prices for both parties. This platform allows farmers to list their products and customers to purchase them directly, with support for **UPI-based payments through Razorpay**. Built with **Python Flask**, Bootstrap, and integrated with **Razorpay** for secure payments.

## 📌 Table of Contents

- [🚀 Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#️-installation--setup)
- [👥 User Roles and Access](#-user-roles-and-access)
- [💳 Payment Integration](#-payment-integration)
- [🧪 Testing](#-testing)
- [📸 Screenshots](#-screenshots)
- [📄 License](#-license)

## 🚀 Features

### For Customers
- Browse products from various farmers
- Add products to cart
- Checkout with secure payment integration (Razorpay)
- Track order status
- View order history

### For Farmers
- Dashboard to manage products and orders
- Add, edit, and delete products
- Upload product images
- Track orders and update order status
- View sales history

### For Admins
- Comprehensive dashboard with statistics
- Manage users (farmers and customers)
- Manage products across the platform
- Manage and track all orders
- Update order statuses

## 🛠 Tech Stack

**Backend:**
- Python Flask
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-WTF (Forms)
- Razorpay Python SDK (Payment Integration)
- SQLite Database

**Frontend:**
- HTML, CSS (Bootstrap 5)
- JavaScript
- Jinja2 Templates

**Payment Gateway:**
- Razorpay (with UPI, Card, NetBanking support)

## 📁 Project Structure

```
farm_fresh/
├── app/                    # Application package
│   ├── __init__.py         # Application factory
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── cart.py
│   ├── routes/             # Route handlers
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── farmer.py
│   │   ├── customer.py
│   │   ├── payment.py
│   │   └── admin.py        # Admin routes
│   ├── forms/              # Form definitions
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── product.py
│   ├── templates/          # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── contact.html
│   │   ├── auth/
│   │   ├── farmer/
│   │   ├── customer/
│   │   ├── payment/
│   │   └── admin/          # Admin templates
│   └── static/             # Static files
│       ├── css/
│       ├── js/
│       └── images/
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── create_admin.py         # Script to create admin user
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhanushm18/farm_fresh.git
   cd farm_fresh
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory with the following content:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URI=sqlite:///farmfresh.db
   RAZORPAY_KEY_ID=your_razorpay_key_id
   RAZORPAY_KEY_SECRET=your_razorpay_key_secret
   ```

   Replace `your_secret_key` with a secure random string.
   For testing Razorpay, you can use test credentials from the Razorpay dashboard.

5. **Initialize the database**
   ```bash
   python -c "from app import create_app; from app import db; app = create_app(); with app.app_context(): db.create_all()"
   ```

6. **Create an admin user**
   ```bash
   python create_admin.py admin admin@farmfresh.com admin_password
   ```
   Replace `admin_password` with a secure password.

7. **Run the application**
   ```bash
   python -m flask --app app run --debug
   ```

8. **Access the application**

   Open your browser and navigate to `http://127.0.0.1:5000`

## 👥 User Roles and Access

### Customer
- Register as a customer
- Browse and purchase products
- Track orders

### Farmer
- Register as a farmer
- Add and manage products
- Fulfill orders

### Admin
- Manage all users, products, and orders
- Access admin dashboard
- Update order statuses

## 💳 Payment Integration

The application uses Razorpay for payment processing. For testing, you can use the following credentials:

- **Test Card**: 4111 1111 1111 1111
- **Expiry**: Any future date
- **CVV**: Any 3-digit number
- **Name**: Any name
- **Test UPI**: success@razorpay

## 🧪 Testing

To test the application, follow these steps:

1. **Register as different user types**
   - Register as a farmer to add products
   - Register as a customer to purchase products
   - Use the admin account to manage the platform

2. **Test the payment system**
   - Add products to cart
   - Proceed to checkout
   - Use Razorpay test credentials for payment

3. **Test admin functionality**
   - Login as admin (created using the `create_admin.py` script)
   - Access the admin dashboard at `/admin`
   - Manage users, products, and orders

## 📸 Screenshots

### Home Page
![Home Page](app/static/images/screenshots/home.png)

### Admin Dashboard
![Admin Dashboard](app/static/images/screenshots/admin-dashboard.png)

## 📄 License

This project is licensed under the MIT License.

## Deployment

### Deploying to Render

1. Create an account on [Render](https://render.com/)
2. Click on the "New +" button and select "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file and set up your services
5. Configure the environment variables:
   - `SECRET_KEY`: Render will generate this automatically
   - `DATABASE_URI`: For production, consider using a PostgreSQL database
   - `RAZORPAY_KEY_ID`: Your Razorpay Key ID
   - `RAZORPAY_KEY_SECRET`: Your Razorpay Key Secret
6. Click "Apply" to deploy your application

### Deploying to Heroku

1. Create an account on [Heroku](https://www.heroku.com/)
2. Install the Heroku CLI and login:
   ```bash
   heroku login
   ```
3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
4. Add a PostgreSQL database:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```
5. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set RAZORPAY_KEY_ID=your_razorpay_key_id
   heroku config:set RAZORPAY_KEY_SECRET=your_razorpay_key_secret
   ```
6. Push to Heroku:
   ```bash
   git push heroku main
   ```
7. Initialize the database:
   ```bash
   heroku run python -c "from app import create_app; from app import db; app = create_app(); with app.app_context(): db.create_all()"
   ```
8. Create an admin user:
   ```bash
   heroku run python create_admin.py admin admin@farmfresh.com admin_password
   ```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## Contact

For any questions or feedback, please contact:
- GitHub: [dhanushm18](https://github.com/dhanushm18)
