"""
DevOps Capstone - Python Flask Application
Food Delivery App with Ingredient Management
"""

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory data store
accounts = []
ingredients = []
zones = []

account_id_counter = 1
ingredient_id_counter = 1
zone_id_counter = 1


# ─────────────────────────────────────────────
# Health / Root
# ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Food Delivery DevOps Capstone API",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


# ─────────────────────────────────────────────
# Accounts CRUD
# ─────────────────────────────────────────────
@app.route("/accounts", methods=["GET"])
def get_accounts():
    return jsonify({"accounts": accounts, "count": len(accounts)}), 200


@app.route("/accounts", methods=["POST"])
def create_account():
    global account_id_counter
    data = request.get_json()
    if not data or "name" not in data:
        abort(400, description="Field 'name' is required")
    account = {
        "id": account_id_counter,
        "name": data["name"],
        "email": data.get("email", ""),
    }
    accounts.append(account)
    account_id_counter += 1
    return jsonify({"message": "Account created", "account": account}), 201


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = next((a for a in accounts if a["id"] == account_id), None)
    if account is None:
        abort(404, description="Account not found")
    return jsonify(account), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = next((a for a in accounts if a["id"] == account_id), None)
    if account is None:
        abort(404, description="Account not found")
    data = request.get_json()
    if "name" in data:
        account["name"] = data["name"]
    if "email" in data:
        account["email"] = data["email"]
    return jsonify({"message": "Account updated", "account": account}), 200


@app.route("/accounts", methods=["DELETE"])
def delete_all_accounts():
    global accounts
    count = len(accounts)
    accounts = []
    return jsonify({"message": f"Deleted all {count} accounts"}), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    global accounts
    account = next((a for a in accounts if a["id"] == account_id), None)
    if account is None:
        abort(404, description="Account not found")
    accounts = [a for a in accounts if a["id"] != account_id]
    return jsonify({"message": f"Account {account_id} deleted"}), 200


# ─────────────────────────────────────────────
# Ingredients CRUD  (Food Delivery Feature)
# ─────────────────────────────────────────────
@app.route("/ingredients", methods=["GET"])
def get_ingredients():
    return jsonify({"ingredients": ingredients, "count": len(ingredients)}), 200


@app.route("/ingredients", methods=["POST"])
def add_ingredient():
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
    return jsonify({"message": "Ingredient added to food delivery app", "ingredient": ingredient}), 201


@app.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id):
    ingredient = next((i for i in ingredients if i["id"] == ingredient_id), None)
    if ingredient is None:
        abort(404, description="Ingredient not found")
    return jsonify(ingredient), 200


@app.route("/ingredients/<int:ingredient_id>", methods=["PUT"])
def update_ingredient(ingredient_id):
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
    return jsonify({"message": "Ingredient updated", "ingredient": ingredient}), 200


@app.route("/ingredients/<int:ingredient_id>", methods=["DELETE"])
def delete_ingredient(ingredient_id):
    global ingredients
    ingredient = next((i for i in ingredients if i["id"] == ingredient_id), None)
    if ingredient is None:
        abort(404, description="Ingredient not found")
    ingredients = [i for i in ingredients if i["id"] != ingredient_id]
    return jsonify({"message": f"Ingredient {ingredient_id} deleted"}), 200


# ─────────────────────────────────────────────
# Zones CRUD
# ─────────────────────────────────────────────
@app.route("/zones", methods=["GET"])
def get_zones():
    return jsonify({"zones": zones, "count": len(zones)}), 200


@app.route("/zones", methods=["POST"])
def create_zone():
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
    return jsonify({"message": "Zone created", "zone": zone}), 201


@app.route("/zones/<int:zone_id>", methods=["GET"])
def get_zone(zone_id):
    zone = next((z for z in zones if z["id"] == zone_id), None)
    if zone is None:
        abort(404, description="Zone not found")
    return jsonify(zone), 200


@app.route("/zones/<int:zone_id>", methods=["DELETE"])
def delete_zone(zone_id):
    global zones
    zone = next((z for z in zones if z["id"] == zone_id), None)
    if zone is None:
        abort(404, description="Zone not found")
    zones = [z for z in zones if z["id"] != zone_id]
    return jsonify({"message": f"Zone {zone_id} deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
