"""
Tests for the DevOps Capstone Food Delivery API
Story: "Add an ingredient to a food delivery app"
"""

import json
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ─────────────────────────────────────────────
# Health Check Tests
# ─────────────────────────────────────────────
class TestHealth:
    def test_home_endpoint(self, client):
        """Test the root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "Welcome to the Food Delivery DevOps Capstone API" in data["message"]
        assert data["status"] == "running"

    def test_health_endpoint(self, client):
        """Test the /health endpoint returns healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"


# ─────────────────────────────────────────────
# Ingredient Tests
# Story: "Add an ingredient to a food delivery app"
# ─────────────────────────────────────────────
class TestIngredients:
    def test_add_ingredient_to_food_delivery_app(self, client):
        """
        USER STORY: Add an ingredient to a food delivery app.
        Verifies that a new ingredient can be successfully added.
        """
        payload = {
            "name": "Tomato",
            "quantity": 5,
            "unit": "kg"
        }
        response = client.post(
            "/ingredients",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "Ingredient added to food delivery app"
        assert data["ingredient"]["name"] == "Tomato"
        assert data["ingredient"]["quantity"] == 5
        assert data["ingredient"]["unit"] == "kg"
        assert "id" in data["ingredient"]

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
                content_type="application/json"
            )
            assert response.status_code == 201

    def test_get_all_ingredients(self, client):
        """Test retrieving all ingredients."""
        # First add one
        client.post(
            "/ingredients",
            data=json.dumps({"name": "Pepper", "quantity": 3, "unit": "pcs"}),
            content_type="application/json"
        )
        response = client.get("/ingredients")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "ingredients" in data
        assert isinstance(data["ingredients"], list)
        assert data["count"] >= 0

    def test_add_ingredient_missing_name_returns_400(self, client):
        """Test that missing required 'name' field returns 400."""
        payload = {"quantity": 5}
        response = client.post(
            "/ingredients",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 400

    def test_get_single_ingredient(self, client):
        """Test retrieving a single ingredient by ID."""
        # Add first
        add_response = client.post(
            "/ingredients",
            data=json.dumps({"name": "Garlic", "quantity": 4, "unit": "cloves"}),
            content_type="application/json"
        )
        ingredient_id = json.loads(add_response.data)["ingredient"]["id"]

        # Get it
        response = client.get(f"/ingredients/{ingredient_id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == "Garlic"

    def test_update_ingredient(self, client):
        """Test updating an ingredient."""
        add_response = client.post(
            "/ingredients",
            data=json.dumps({"name": "Salt", "quantity": 1, "unit": "kg"}),
            content_type="application/json"
        )
        ingredient_id = json.loads(add_response.data)["ingredient"]["id"]

        update_response = client.put(
            f"/ingredients/{ingredient_id}",
            data=json.dumps({"quantity": 2}),
            content_type="application/json"
        )
        assert update_response.status_code == 200
        data = json.loads(update_response.data)
        assert data["ingredient"]["quantity"] == 2

    def test_delete_ingredient(self, client):
        """Test deleting an ingredient."""
        add_response = client.post(
            "/ingredients",
            data=json.dumps({"name": "Sugar", "quantity": 500, "unit": "g"}),
            content_type="application/json"
        )
        ingredient_id = json.loads(add_response.data)["ingredient"]["id"]

        del_response = client.delete(f"/ingredients/{ingredient_id}")
        assert del_response.status_code == 200

    def test_get_nonexistent_ingredient_returns_404(self, client):
        """Test that fetching a non-existent ingredient returns 404."""
        response = client.get("/ingredients/999999")
        assert response.status_code == 404


# ─────────────────────────────────────────────
# Account Tests
# Story: "Delete all accounts from the Docs column"
# ─────────────────────────────────────────────
class TestAccounts:
    def test_create_account(self, client):
        """Test creating a new account."""
        payload = {"name": "Ahmed Fawzy", "email": "ahmed@example.com"}
        response = client.post(
            "/accounts",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["account"]["name"] == "Ahmed Fawzy"

    def test_get_all_accounts(self, client):
        """Test getting all accounts."""
        response = client.get("/accounts")
        assert response.status_code == 200

    def test_delete_all_accounts(self, client):
        """
        USER STORY: Delete all accounts from the Docs column.
        Verifies bulk deletion of all accounts.
        """
        # Create some accounts first
        for name in ["User1", "User2", "User3"]:
            client.post(
                "/accounts",
                data=json.dumps({"name": name, "email": f"{name}@test.com"}),
                content_type="application/json"
            )

        # Delete all
        response = client.delete("/accounts")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "Deleted all" in data["message"]

        # Confirm empty
        get_response = client.get("/accounts")
        remaining = json.loads(get_response.data)
        assert remaining["count"] == 0

    def test_update_account(self, client):
        """Test updating an account (update goals)."""
        add_response = client.post(
            "/accounts",
            data=json.dumps({"name": "Test User", "email": "test@test.com"}),
            content_type="application/json"
        )
        account_id = json.loads(add_response.data)["account"]["id"]

        update_response = client.put(
            f"/accounts/{account_id}",
            data=json.dumps({"email": "updated@test.com"}),
            content_type="application/json"
        )
        assert update_response.status_code == 200


# ─────────────────────────────────────────────
# Zone Tests
# ─────────────────────────────────────────────
class TestZones:
    def test_create_zone(self, client):
        """Test creating a delivery zone."""
        payload = {"name": "Zone-A", "region": "North"}
        response = client.post(
            "/zones",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["zone"]["name"] == "Zone-A"
        assert data["message"] == "Zone created"

    def test_get_zones(self, client):
        """Test getting all zones."""
        response = client.get("/zones")
        assert response.status_code == 200

    def test_delete_zone(self, client):
        """Test deleting a zone."""
        add_response = client.post(
            "/zones",
            data=json.dumps({"name": "Zone-B"}),
            content_type="application/json"
        )
        zone_id = json.loads(add_response.data)["zone"]["id"]
        del_response = client.delete(f"/zones/{zone_id}")
        assert del_response.status_code == 200
