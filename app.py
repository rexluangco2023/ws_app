from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Sample customer data
customers = {
  "customers": {
    "1001": {
      "personal_info": {
        "name": "John Doe",
        "date_of_birth": "1980-01-01",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA"
      },
      "account_details": {
        "status": "active",
        "membership_level": "Gold",
        "loyalty_points": 1500,
        "last_purchase_date": "2023-08-15",
        "preferred_contact_method": "email"
      },
      "professional_info": {
        "department": "Sales",
        "account_manager": "Sarah Lee"
      }
    }
  }
}

@app.route('/')
def hello_world():
    return jsonify(message="Genesys Cloud Web Service Data Action Example")

@app.route('/api/customer', methods=['POST'])
def create_customer():
    data = request.json
    customer_id = data.get('customerId')
    
    if customer_id in customers["customers"]:
        return jsonify({"error": "Customer ID already exists"}), 400
    else:
        customers["customers"][customer_id] = {
          "personal_info": {
            "name": data.get("name"),
            "date_of_birth": data.get("date_of_birth"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "address": data.get("address")
          },
          "account_details": {
            "status": data.get("status"),
            "membership_level": data.get("membership_level"),
            "loyalty_points": data.get("loyalty_points"),
            "last_purchase_date": data.get("last_purchase_date"),
            "preferred_contact_method": data.get("preferred_contact_method")
          },
          "professional_info": {
            "department": data.get("department"),
            "account_manager": data.get("account_manager")
          }
        }
        return jsonify(customers["customers"][customer_id]), 201

@app.route('/api/customers', methods=['GET'])
def get_all_customers():
    return jsonify(customers), 200

@app.route('/api/customers/grouped', methods=['GET'])
def get_grouped_customers():
    grouped_customers = {}
    for customer_id, customer_data in customers["customers"].items():
        group_key = customer_id[0]  # Group by the first digit of the customer ID
        if group_key not in grouped_customers:
            grouped_customers[group_key] = []
        grouped_customers[group_key].append({customer_id: customer_data})
    return jsonify(grouped_customers), 200

@app.route('/api/customer/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    if customer_id in customers["customers"]:
        return jsonify(customers["customers"][customer_id]), 200
    else:
        return jsonify({"error": "Customer not found"}), 404

@app.route('/api/customer/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    if customer_id in customers["customers"]:
        data = request.json
        customers["customers"][customer_id].update({
          "personal_info": {
            "name": data.get("name"),
            "date_of_birth": data.get("date_of_birth"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "address": data.get("address")
          },
          "account_details": {
            "status": data.get("status"),
            "membership_level": data.get("membership_level"),
            "loyalty_points": data.get("loyalty_points"),
            "last_purchase_date": data.get("last_purchase_date"),
            "preferred_contact_method": data.get("preferred_contact_method")
          },
          "professional_info": {
            "department": data.get("department"),
            "account_manager": data.get("account_manager")
          }
        })
        return jsonify(customers["customers"][customer_id]), 200
    else:
        return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
