"""
DevOps Capstone - Account REST API Service
Flask application with Ingredient Management (Food Delivery feature).
"""

from flask import Flask, jsonify, request, abort, make_response
from flask_talisman import Talisman
from flask_cors import CORS

app = Flask(__name__)

# ── Security Headers via Talisman ──────────────────────────────────────────
Talisman(
    app,
    force_https=False,              # disabled for local/HTTP environments
    strict_transport_security=True,
    content_security_policy=False,  # relax CSP for API service
    frame_options="DENY",
)

# ── CORS Policy ────────────────────────────────────────────────────────────
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# In-memory data store
accounts = []
ingredients = []
zones = []

account_id_counter = 1
ingredient_id_counter = 1
zone_id_counter = 1


# ─────────────────────────────────────────────
# Root / Health
# ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    """Root endpoint — returns service name and version (Q26 expected response)."""
    return jsonify({
        "name": "Account REST API Service",
        "version": "1.0",
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "OK"}), 200


# ─────────────────────────────────────────────
# Accounts CRUD
# ─────────────────────────────────────────────
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all accounts — HTTP 200 OK."""
    return jsonify(accounts), 200


@app.route("/accounts", methods=["POST"])
def create_account():
    """Create a new account — HTTP 201 CREATED."""
    global account_id_counter
    data = request.get_json()
    if not data or "name" not in data:
        abort(400, description="Field 'name' is required")
    account = {
        "id": account_id_counter,
        "name": data["name"],
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
    }
    accounts.append(account)
    account_id_counter += 1
    return jsonify(account), 201


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read a single account by ID — HTTP 200 OK."""
    account = next((a for a in accounts if a["id"] == account_id), None)
    if account is None:
        abort(404, description="Account not found")
    return jsonify(account), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an account — HTTP 200 OK."""
    account = next((a for a in accounts if a["id"] == account_id), None)
    if account is None:
        abort(404, description="Account not found")
    data = request.get_json()
    if "name" in data:
        account["name"] = data["name"]
    if "email" in data:
        account["email"] = data["email"]
    if "phone" in data:
        account["phone"] = data["phone"]
    return jsonify(account), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete a single account — HTTP 204 NO CONTENT (empty body)."""
    global accounts
    account = next((a for a in accounts if a["id"] == account_id), None)
    if account is None:
        abort(404, description="Account not found")
    accounts = [a for a in accounts if a["id"] != account_id]
    return make_response("", 204)


@app.route("/accounts", methods=["DELETE"])
def delete_all_accounts():
    """Delete ALL accounts — HTTP 204 NO CONTENT (empty body)."""
    global accounts
    accounts = []
    return make_response("", 204)


# ─────────────────────────────────────────────
# Ingredients CRUD  (Food Delivery Feature)
# User Story: "Add an ingredient to a food delivery app"
# ─────────────────────────────────────────────
@app.route("/ingredients", methods=["GET"])
def get_ingredients():
    """List all ingredients — HTTP 200 OK."""
    return jsonify(ingredients), 200


@app.route("/ingredients", methods=["POST"])
def add_ingredient():
    """Add an ingredient to a food delivery app — HTTP 201 CREATED."""
    global ingredient_id_counter
    data = request.get_json()
    if not data or "name" not in data:
        abort(400, description="Field 'name' is required")
    ingredient = {
        "id": ingredient_id_counter,
        "name": data["name"],
        "quantity": data.get("quantity", 1),
        "unit": data.get("unit", "pcs"),
    }
    ingredients.append(ingredient)
    ingredient_id_counter += 1
    return jsonify(ingredient), 201


@app.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id):
    """Get ingredient by ID — HTTP 200 OK."""
    ingredient = next((i for i in ingredients if i["id"] == ingredient_id), None)
    if ingredient is None:
        abort(404, description="Ingredient not found")
    return jsonify(ingredient), 200


@app.route("/ingredients/<int:ingredient_id>", methods=["PUT"])
def update_ingredient(ingredient_id):
    """Update an ingredient — HTTP 200 OK."""
    ingredient = next((i for i in ingredients if i["id"] == ingredient_id), None)
    if ingredient is None:
        abort(404, description="Ingredient not found")
    data = request.get_json()
    if "name" in data:
        ingredient["name"] = data["name"]
    if "quantity" in data:
        ingredient["quantity"] = data["quantity"]
    if "unit" in data:
        ingredient["unit"] = data["unit"]
    return jsonify(ingredient), 200


@app.route("/ingredients/<int:ingredient_id>", methods=["DELETE"])
def delete_ingredient(ingredient_id):
    """Delete an ingredient — HTTP 204 NO CONTENT."""
    global ingredients
    ingredient = next((i for i in ingredients if i["id"] == ingredient_id), None)
    if ingredient is None:
        abort(404, description="Ingredient not found")
    ingredients = [i for i in ingredients if i["id"] != ingredient_id]
    return make_response("", 204)


# ─────────────────────────────────────────────
# Zones CRUD
# ─────────────────────────────────────────────
@app.route("/zones", methods=["GET"])
def get_zones():
    """List all zones — HTTP 200 OK."""
    return jsonify(zones), 200


@app.route("/zones", methods=["POST"])
def create_zone():
    """Create a delivery zone — HTTP 201 CREATED."""
    global zone_id_counter
    data = request.get_json()
    if not data or "name" not in data:
        abort(400, description="Field 'name' is required")
    zone = {
        "id": zone_id_counter,
        "name": data["name"],
        "region": data.get("region", "default"),
    }
    zones.append(zone)
    zone_id_counter += 1
    return jsonify(zone), 201


@app.route("/zones/<int:zone_id>", methods=["GET"])
def get_zone(zone_id):
    """Get a single zone by ID — HTTP 200 OK."""
    zone = next((z for z in zones if z["id"] == zone_id), None)
    if zone is None:
        abort(404, description="Zone not found")
    return jsonify(zone), 200


@app.route("/zones/<int:zone_id>", methods=["DELETE"])
def delete_zone(zone_id):
    """Delete a zone — HTTP 204 NO CONTENT."""
    global zones
    zone = next((z for z in zones if z["id"] == zone_id), None)
    if zone is None:
        abort(404, description="Zone not found")
    zones = [z for z in zones if z["id"] != zone_id]
    return make_response("", 204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
