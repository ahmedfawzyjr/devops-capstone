# User Story — Add an Ingredient to a Food Delivery App

## Story

**As a** food delivery app manager,
**I want to** add ingredients to the system,
**So that** I can track what ingredients are available for preparing food orders.

## Acceptance Criteria

- **Given** I am an authorized user of the Food Delivery API
- **When** I send a `POST` request to `/ingredients` with a valid JSON body containing at least a `name` field
- **Then** the system should create the ingredient and return a `201 CREATED` response with the new ingredient's details

## Details

| Field         | Value                              |
|---------------|------------------------------------|
| **Story ID**  | US-001                             |
| **Epic**      | Ingredient Management              |
| **Priority**  | High                               |
| **Points**    | 3                                  |
| **Assignee**  | Ahmed Fawzy                        |
| **Sprint**    | Sprint 1                           |

## Endpoints Implemented

| Method   | Endpoint                  | Description                        | Status Code     |
|----------|---------------------------|------------------------------------|-----------------|
| `POST`   | `/ingredients`            | Add an ingredient                  | `201 CREATED`   |
| `GET`    | `/ingredients`            | List all ingredients               | `200 OK`        |
| `GET`    | `/ingredients/<id>`       | Get a single ingredient            | `200 OK`        |
| `PUT`    | `/ingredients/<id>`       | Update an ingredient               | `200 OK`        |
| `DELETE` | `/ingredients/<id>`       | Delete an ingredient               | `204 NO CONTENT`|

## Example Request

```bash
curl -i -X POST http://localhost:5000/ingredients \
  -H "Content-Type: application/json" \
  -d '{"name": "Tomato", "quantity": 5, "unit": "kg"}'
```

## Example Response

```
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "id": 1,
  "name": "Tomato",
  "quantity": 5,
  "unit": "kg"
}
```

## Test

This story is covered by the automated test:
`test_add_ingredient_to_food_delivery_app` in `app/tests/test_main.py`
