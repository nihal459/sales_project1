# Sale Point

## Overview
Sale Point is a Django-based web application designed for managing sales and inventory efficiently. The system includes robust sales analytics, inventory management, and invoice management features. The application uses PostgreSQL as the database and Chart.js for visual analytics.

## Features
### Inventory Management
- Add, update, and delete products.
- Track stock levels and receive alerts for low-stock products.

### Salesman Management
- Manage sales personnel and track their performance.
- Assign sales to specific salespeople.

### Sales Analytics
Real-time sales analytics include:
- **Total Revenue** for the current month.
- **Total Number of Sales** for the current month.
- **Top-Selling Products**: Displays the top 5 products by quantity sold.
- **Sales Trends**: Line chart displaying daily/weekly revenue trends for the current month.
- **Revenue Breakdown by Salesperson**: A bar or pie chart showing revenue contribution by individual salespeople.
- **Low-Stock Products**: Lists products with stock levels below a predefined threshold (e.g., less than 5 units).

### Invoice Management
- Create invoices for sales transactions.
- Edit or delete invoices as needed.

### Secure Login
- User authentication system for secure access.

## Technologies Used
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: Bootstrap and pre-designed template
- **Charts & Analytics**: Chart.js

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- PostgreSQL
- Django

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sale-point.git](https://github.com/nihal459/sales_project1.git
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   cd env
   Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Default Login Credentials
- **Username**: `sales_admin`
- **Password**: `1234`

## License
This project is not licensed 

## Contact
For any inquiries, reach out to nihal.techworks@gmail.com

