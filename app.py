from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Sample customer data
customers = {
    "1001": {"name": "John Doe", "email": "john.doe@example.com", "status": "active"},
    "1002": {"name": "Jane Smith", "email": "jane.smith@example.com", "status": "inactive"},
    "1003": {"name": "Bob Johnson", "email": "bob.johnson@example.com", "status": "active"}
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
