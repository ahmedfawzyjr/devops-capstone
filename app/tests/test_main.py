"""
Tests for the DevOps Capstone — Account REST API Service
Story: "Add an ingredient to a food delivery app"
"""

import json
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory store before every test."""
    import app.main as m
    m.accounts = []
    m.ingredients = []
    m.zones = []
    m.account_id_counter = 1
    m.ingredient_id_counter = 1
    m.zone_id_counter = 1
    yield


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


# ─────────────────────────────────────────────
# Health / Root Tests
# ─────────────────────────────────────────────
class TestHealth:
    def test_home_endpoint(self, client):
        """Root endpoint returns the expected service name and version."""
        response = client.get("/")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == "Account REST API Service"
        assert data["version"] == "1.0"

    def test_health_endpoint(self, client):
        """Health endpoint returns OK."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "OK"


# ─────────────────────────────────────────────
# Ingredient Tests
# Story: "Add an ingredient to a food delivery app"
# ─────────────────────────────────────────────
class TestIngredients:
    def test_add_ingredient_to_food_delivery_app(self, client):
        """
        USER STORY: Add an ingredient to a food delivery app.
        Verifies that a new ingredient can be successfully added (HTTP 201).
        """
        payload = {"name": "Tomato", "quantity": 5, "unit": "kg"}
        response = client.post(
            "/ingredients",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["name"] == "Tomato"
        assert data["quantity"] == 5
        assert data["unit"] == "kg"
        assert "id" in data

    def test_add_multiple_ingredients(self, client):
        """Test adding multiple ingredients to the food delivery app."""
        ingredients_to_add = [
            {"name": "Cheese", "quantity": 2, "unit": "kg"},
            {"name": "Basil", "quantity": 10, "unit": "leaves"},
            {"name": "Olive Oil", "quantity": 1, "unit": "liter"},
        ]
        for ingredient in ingredients_to_add:
            response = client.post(
                "/ingredients",
                data=json.dumps(ingredient),
                content_type="application/json",
            )
            assert response.status_code == 201

    def test_get_all_ingredients(self, client):
        """Test retrieving all ingredients (HTTP 200)."""
        client.post(
            "/ingredients",
            data=json.dumps({"name": "Pepper", "quantity": 3, "unit": "pcs"}),
            content_type="application/json",
        )
        response = client.get("/ingredients")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_add_ingredient_missing_name_returns_400(self, client):
        """Missing required 'name' field returns 400."""
        payload = {"quantity": 5}
        response = client.post(
            "/ingredients",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_get_single_ingredient(self, client):
        """Test retrieving a single ingredient by ID (HTTP 200)."""
        add_response = client.post(
            "/ingredients",
            data=json.dumps({"name": "Garlic", "quantity": 4, "unit": "cloves"}),
            content_type="application/json",
        )
        ingredient_id = json.loads(add_response.data)["id"]
        response = client.get(f"/ingredients/{ingredient_id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == "Garlic"

    def test_update_ingredient(self, client):
        """Test updating an ingredient (HTTP 200)."""
        add_response = client.post(
            "/ingredients",
            data=json.dumps({"name": "Salt", "quantity": 1, "unit": "kg"}),
            content_type="application/json",
        )
        ingredient_id = json.loads(add_response.data)["id"]
        update_response = client.put(
            f"/ingredients/{ingredient_id}",
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
        )
        assert update_response.status_code == 200
        data = json.loads(update_response.data)
        assert data["quantity"] == 2

    def test_delete_ingredient(self, client):
        """Test deleting an ingredient returns 204 NO CONTENT."""
        add_response = client.post(
            "/ingredients",
            data=json.dumps({"name": "Sugar", "quantity": 500, "unit": "g"}),
            content_type="application/json",
        )
        ingredient_id = json.loads(add_response.data)["id"]
        del_response = client.delete(f"/ingredients/{ingredient_id}")
        assert del_response.status_code == 204

    def test_get_nonexistent_ingredient_returns_404(self, client):
        """Fetching a non-existent ingredient returns 404."""
        response = client.get("/ingredients/999999")
        assert response.status_code == 404


# ─────────────────────────────────────────────
# Account Tests
# Stories: Create, Read, Update, Delete, List all accounts
# ─────────────────────────────────────────────
class TestAccounts:
    def test_create_account(self, client):
        """Create a new account — HTTP 201 CREATED."""
        payload = {"name": "Ahmed Fawzy", "email": "ahmed@example.com"}
        response = client.post(
            "/accounts",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["name"] == "Ahmed Fawzy"
        assert "id" in data

    def test_list_all_accounts(self, client):
        """List all accounts — HTTP 200 OK."""
        # Add two accounts first
        for name in ["Alice", "Bob"]:
            client.post(
                "/accounts",
                data=json.dumps({"name": name, "email": f"{name.lower()}@test.com"}),
                content_type="application/json",
            )
        response = client.get("/accounts")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2

    def test_read_account(self, client):
        """Read a single account by ID — HTTP 200 OK."""
        add_response = client.post(
            "/accounts",
            data=json.dumps({"name": "Test User", "email": "test@test.com"}),
            content_type="application/json",
        )
        account_id = json.loads(add_response.data)["id"]
        response = client.get(f"/accounts/{account_id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == "Test User"

    def test_update_account(self, client):
        """Update an account — HTTP 200 OK."""
        add_response = client.post(
            "/accounts",
            data=json.dumps({"name": "Test User", "email": "test@test.com"}),
            content_type="application/json",
        )
        account_id = json.loads(add_response.data)["id"]
        update_response = client.put(
            f"/accounts/{account_id}",
            data=json.dumps({"email": "updated@test.com"}),
            content_type="application/json",
        )
        assert update_response.status_code == 200
        data = json.loads(update_response.data)
        assert data["email"] == "updated@test.com"

    def test_delete_account(self, client):
        """Delete a single account — HTTP 204 NO CONTENT."""
        add_response = client.post(
            "/accounts",
            data=json.dumps({"name": "To Delete", "email": "del@test.com"}),
            content_type="application/json",
        )
        account_id = json.loads(add_response.data)["id"]
        del_response = client.delete(f"/accounts/{account_id}")
        assert del_response.status_code == 204

    def test_delete_all_accounts(self, client):
        """
        USER STORY: Delete all accounts from the Docs column.
        Returns HTTP 204 NO CONTENT with empty body.
        """
        # Create some accounts first
        for name in ["User1", "User2", "User3"]:
            client.post(
                "/accounts",
                data=json.dumps({"name": name, "email": f"{name}@test.com"}),
                content_type="application/json",
            )

        # Delete all — should return 204 with empty body
        response = client.delete("/accounts")
        assert response.status_code == 204
        assert response.data == b""

        # Confirm empty
        get_response = client.get("/accounts")
        remaining = json.loads(get_response.data)
        assert remaining == []


# ─────────────────────────────────────────────
# Zone Tests
# ─────────────────────────────────────────────
class TestZones:
    def test_create_zone(self, client):
        """Create a delivery zone — HTTP 201 CREATED."""
        payload = {"name": "Zone-A", "region": "North"}
        response = client.post(
            "/zones",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["name"] == "Zone-A"

    def test_get_zones(self, client):
        """Get all zones — HTTP 200 OK."""
        response = client.get("/zones")
        assert response.status_code == 200

    def test_delete_zone(self, client):
        """Delete a zone — HTTP 204 NO CONTENT."""
        add_response = client.post(
            "/zones",
            data=json.dumps({"name": "Zone-B"}),
            content_type="application/json",
        )
        zone_id = json.loads(add_response.data)["id"]
        del_response = client.delete(f"/zones/{zone_id}")
        assert del_response.status_code == 204
