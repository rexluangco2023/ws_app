from flask import Flask, jsonify, request
import os
import secrets
import time

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory token store  { token_string: expiry_epoch }
# ---------------------------------------------------------------------------
active_tokens = {}
TOKEN_TTL_SECONDS = 3600  # tokens expire after 1 hour

# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def generate_token():
    """Create a cryptographically secure random token."""
    return secrets.token_hex(32)


def require_token(f):
    """Decorator – validates Bearer token on every protected route."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ", 1)[1]

        # Check token exists and hasn't expired
        expiry = active_tokens.get(token)
        if expiry is None or time.time() > expiry:
            active_tokens.pop(token, None)          # clean up expired token
            return jsonify({"error": "Token invalid or expired"}), 401

        return f(*args, **kwargs)

    return decorated


# ---------------------------------------------------------------------------
# AUTH ENDPOINT  –  POST /auth/token
# ---------------------------------------------------------------------------
# Genesys Cloud (or any client) calls this first with:
#   Body: { "client_id": "...", "client_secret": "..." }
# and receives a Bearer token to use on subsequent requests.
# ---------------------------------------------------------------------------

@app.route('/auth/token', methods=['POST'])
def get_token():
    """
    Login / token endpoint.
    Expects JSON body:
        { "client_id": "<CLIENT_ID>", "client_secret": "<CLIENT_SECRET>" }
    Returns:
        { "access_token": "...", "token_type": "Bearer", "expires_in": 3600 }
    """
    data = request.get_json(silent=True) or {}

    client_id     = data.get("client_id", "").strip()
    client_secret = data.get("client_secret", "").strip()

    # Validate against environment variables (set these in Render dashboard)
    expected_id     = os.environ.get("CLIENT_ID", "")
    expected_secret = os.environ.get("CLIENT_SECRET", "")

    if not client_id or not client_secret:
        return jsonify({"error": "client_id and client_secret are required"}), 400

    if client_id != expected_id or client_secret != expected_secret:
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate and store token
    token  = generate_token()
    expiry = time.time() + TOKEN_TTL_SECONDS
    active_tokens[token] = expiry

    return jsonify({
        "access_token": token,
        "token_type":   "Bearer",
        "expires_in":   TOKEN_TTL_SECONDS
    }), 200


# ---------------------------------------------------------------------------
# Optional: revoke a token  –  POST /auth/revoke
# ---------------------------------------------------------------------------

@app.route('/auth/revoke', methods=['POST'])
@require_token
def revoke_token():
    """Invalidate the current Bearer token immediately."""
    token = request.headers["Authorization"].split(" ", 1)[1]
    active_tokens.pop(token, None)
    return jsonify({"message": "Token revoked"}), 200


# ---------------------------------------------------------------------------
# Sample customer data
# ---------------------------------------------------------------------------

customers = {
    "customers": {
        "1001": {
            "personal_info": {
                "name": "John Doe",
                "date_of_birth": "1980-01-01",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "address": "123 Main St, Anytown, USA",
                "work_details": {
                    "position": "Sales Manager",
                    "salary": "75000",
                    "hire_date": "2015-06-01"
                }
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
                "account_manager": "Sarah Lee",
                "work_details": {
                    "position": "Sales Manager",
                    "salary": "75000",
                    "hire_date": "2015-06-01"
                }
            }
        }
    }
}


# ---------------------------------------------------------------------------
# Existing routes  –  all protected with @require_token
# ---------------------------------------------------------------------------

@app.route('/')
def hello_world():
    return jsonify(message="Genesys Cloud Web Service Data Action Example")


@app.route('/api/customer', methods=['POST'])
@require_token
def create_customer():
    data = request.json
    customer_id = data.get('customerId')

    if customer_id in customers["customers"]:
        return jsonify({"error": "Customer ID already exists"}), 400

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
            "account_manager": data.get("account_manager"),
            "work_details": {
                "position": data.get("position"),
                "salary": data.get("salary"),
                "hire_date": data.get("hire_date")
            }
        }
    }
    return jsonify(customers["customers"][customer_id]), 201


@app.route('/api/customers', methods=['GET'])
@require_token
def get_all_customers():
    return jsonify(customers), 200


@app.route('/api/customers/grouped', methods=['GET'])
@require_token
def get_grouped_customers():
    grouped_customers = {}
    for customer_id, customer_data in customers["customers"].items():
        group_key = customer_id[0]
        if group_key not in grouped_customers:
            grouped_customers[group_key] = []
        grouped_customers[group_key].append({customer_id: customer_data})
    return jsonify(grouped_customers), 200


@app.route('/api/customer/<customer_id>', methods=['GET'])
@require_token
def get_customer_by_id(customer_id):
    if customer_id in customers["customers"]:
        return jsonify(customers["customers"][customer_id]), 200
    return jsonify({"error": "Customer not found"}), 404


@app.route('/api/customer/<customer_id>/personal', methods=['GET'])
@require_token
def get_customer_personal_details(customer_id):
    if customer_id in customers["customers"]:
        return jsonify(customers["customers"][customer_id]["personal_info"]), 200
    return jsonify({"error": "Customer not found"}), 404


@app.route('/api/customer/<customer_id>', methods=['PUT'])
@require_token
def update_customer(customer_id):
    if customer_id not in customers["customers"]:
        return jsonify({"error": "Customer not found"}), 404

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
            "account_manager": data.get("account_manager"),
            "work_details": {
                "position": data.get("position"),
                "salary": data.get("salary"),
                "hire_date": data.get("hire_date")
            }
        }
    })
    return jsonify(customers["customers"][customer_id]), 200


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
