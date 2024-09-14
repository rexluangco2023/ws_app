from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Sample customer data
customers = {
    "1001": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "status": "active",
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA",
        "date_of_birth": "1980-01-01",
        "membership_level": "Gold",
        "last_purchase_date": "2023-08-15",
        "preferred_contact_method": "email",
        "department": "Sales",
        "loyalty_points": 1500,
        "account_manager": "Sarah Lee"
    },
    "1002": {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "status": "inactive",
        "phone": "234-567-8901",
        "address": "456 Elm St, Othertown, USA",
        "date_of_birth": "1985-02-02",
        "membership_level": "Silver",
        "last_purchase_date": "2022-12-20",
        "preferred_contact_method": "phone",
        "department": "Marketing",
        "loyalty_points": 800,
        "account_manager": "Michael Brown"
    },
    "1003": {
        "name": "Bob Johnson",
        "email": "bob.johnson@example.com",
        "status": "active",
        "phone": "345-678-9012",
        "address": "789 Oak St, Sometown, USA",
        "date_of_birth": "1990-03-03",
        "membership_level": "Platinum",
        "last_purchase_date": "2023-09-01",
        "preferred_contact_method": "email",
        "department": "Engineering",
        "loyalty_points": 2000,
        "account_manager": "Emily Davis"
    },
    "1004": {
        "name": "Alice Brown",
        "email": "alice.brown@example.com",
        "status": "active",
        "phone": "456-789-0123",
        "address": "101 Pine St, Anycity, USA",
        "date_of_birth": "1995-04-04",
        "membership_level": "Gold",
        "last_purchase_date": "2023-07-22",
        "preferred_contact_method": "phone",
        "department": "Human Resources",
        "loyalty_points": 1200,
        "account_manager": "David Wilson"
    },
    "1005": {
        "name": "Charlie Davis",
        "email": "charlie.davis@example.com",
        "status": "inactive",
        "phone": "567-890-1234",
        "address": "202 Maple St, Othercity, USA",
        "date_of_birth": "2000-05-05",
        "membership_level": "Bronze",
        "last_purchase_date": "2021-11-30",
        "preferred_contact_method": "email",
        "department": "Finance",
        "loyalty_points": 500,
        "account_manager": "Laura Martinez"
    },
    "1006": {
        "name": "Diana Evans",
        "email": "diana.evans@example.com",
        "status": "active",
        "phone": "678-901-2345",
        "address": "303 Birch St, Newtown, USA",
        "date_of_birth": "1988-06-06",
        "membership_level": "Silver",
        "last_purchase_date": "2023-06-15",
        "preferred_contact_method": "phone",
        "department": "Customer Support",
        "loyalty_points": 900,
        "account_manager": "James Anderson"
    },
    "1007": {
        "name": "Edward Foster",
        "email": "edward.foster@example.com",
        "status": "inactive",
        "phone": "789-012-3456",
        "address": "404 Cedar St, Oldtown, USA",
        "date_of_birth": "1992-07-07",
        "membership_level": "Gold",
        "last_purchase_date": "2022-10-10",
        "preferred_contact_method": "email",
        "department": "Legal",
        "loyalty_points": 1100,
        "account_manager": "Patricia Thomas"
    },
    "1008": {
        "name": "Fiona Green",
        "email": "fiona.green@example.com",
        "status": "active",
        "phone": "890-123-4567",
        "address": "505 Spruce St, Smalltown, USA",
        "date_of_birth": "1996-08-08",
        "membership_level": "Platinum",
        "last_purchase_date": "2023-08-05",
        "preferred_contact_method": "phone",
        "department": "IT",
        "loyalty_points": 2500,
        "account_manager": "Robert Jackson"
    },
    "1009": {
        "name": "George Harris",
        "email": "george.harris@example.com",
        "status": "inactive",
        "phone": "901-234-5678",
        "address": "606 Willow St, Bigcity, USA",
        "date_of_birth": "2001-09-09",
        "membership_level": "Bronze",
        "last_purchase_date": "2021-12-25",
        "preferred_contact_method": "email",
        "department": "Operations",
        "loyalty_points": 600,
        "account_manager": "Barbara White"
    },
    "1010": {
        "name": "Hannah Irving",
        "email": "hannah.irving@example.com",
        "status": "active",
        "phone": "012-345-6789",
        "address": "707 Maple St, Midcity, USA",
        "date_of_birth": "2003-10-10",
        "membership_level": "Silver",
        "last_purchase_date": "2023-09-10",
        "preferred_contact_method": "phone",
        "department": "Sales",
        "loyalty_points": 1300,
        "account_manager": "William Harris"
    },
    "1011": {
        "name": "Ian Jackson",
        "email": "ian.jackson@example.com",
        "status": "active",
        "phone": "123-456-7891",
        "address": "808 Birch St, Newcity, USA",
        "date_of_birth": "1981-11-11",
        "membership_level": "Gold",
        "last_purchase_date": "2023-07-01",
        "preferred_contact_method": "email",
        "department": "Marketing",
        "loyalty_points": 1400,
        "account_manager": "Linda Clark"
    },
    "1012": {
        "name": "Julia King",
        "email": "julia.king@example.com",
        "status": "inactive",
        "phone": "234-567-8902",
        "address": "909 Cedar St, Oldcity, USA",
        "date_of_birth": "1986-12-12",
        "membership_level": "Bronze",
        "last_purchase_date": "2022-01-15",
        "preferred_contact_method": "phone",
        "department": "Finance",
        "loyalty_points": 700,
        "account_manager": "Christopher Lewis"
    }
}

@app.route('/')
def hello_world():
    return jsonify(message="Genesys Cloud Web Service Data Action Example")

@app.route('/api/customer', methods=['POST'])
def get_customer_data():
    # Get the customer ID from the request JSON
    data = request.json
    customer_id = data.get('customerId')
    
    if customer_id in customers:
        return jsonify(customers[customer_id]), 200
    else:
        return jsonify({"error": "Customer not found"}), 404

@app.route('/api/customer/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    if customer_id in customers:
        return jsonify(customers[customer_id]), 200
    else:
        return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
