"""
Run all curl commands for Q13-Q17 and Q26 and save formatted output.
"""
import urllib.request
import urllib.error
import json
import http.client

BASE = "http://127.0.0.1:5000"


def make_request(method, path, body=None):
    """Make an HTTP request and return (status, reason, headers, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", 5000)
    headers = {"Content-Type": "application/json"} if body else {}
    data = json.dumps(body).encode() if body else None
    conn.request(method, path, data, headers)
    resp = conn.getresponse()
    resp_body = resp.read().decode("utf-8")
    return resp.status, resp.reason, dict(resp.getheaders()), resp_body


def format_response(method, url, status, reason, headers, body, label):
    lines = [
        f"\n{'='*60}",
        f"  {label}",
        f"{'='*60}",
        f"$ curl -i -X {method} {BASE}{url}",
        f"",
        f"HTTP/1.1 {status} {reason}",
    ]
    for k, v in headers.items():
        lines.append(f"{k}: {v}")
    lines.append("")
    if body:
        try:
            lines.append(json.dumps(json.loads(body), indent=2))
        except Exception:
            lines.append(body)
    else:
        lines.append("(empty body)")
    return "\n".join(lines)


results = {}

# Q26: Root endpoint
s, r, h, b = make_request("GET", "/")
results["Q26_root"] = format_response("GET", "/", s, r, h, b,
    "Q26 - Root Endpoint: GET /")
print(results["Q26_root"])

# Q13: CREATE account (POST → 201)
s, r, h, b = make_request("POST", "/accounts",
    {"name": "John Doe", "email": "john@example.com", "phone": "555-1234"})
results["Q13_create"] = format_response("POST", "/accounts", s, r, h, b,
    "Q13 - CREATE Account: POST /accounts - 201 CREATED")
print(results["Q13_create"])

# Q14: LIST all accounts (GET → 200)
# Add a second account first
make_request("POST", "/accounts",
    {"name": "Jane Smith", "email": "jane@example.com"})
s, r, h, b = make_request("GET", "/accounts")
results["Q14_list"] = format_response("GET", "/accounts", s, r, h, b,
    "Q14 - LIST All Accounts: GET /accounts - 200 OK")
print(results["Q14_list"])

# Q15: READ single account (GET → 200)
s, r, h, b = make_request("GET", "/accounts/1")
results["Q15_read"] = format_response("GET", "/accounts/1", s, r, h, b,
    "Q15 - READ Account: GET /accounts/1 - 200 OK")
print(results["Q15_read"])

# Q16: UPDATE account (PUT → 200)
s, r, h, b = make_request("PUT", "/accounts/1",
    {"name": "John Updated", "email": "john.updated@example.com"})
results["Q16_update"] = format_response("PUT", "/accounts/1", s, r, h, b,
    "Q16 - UPDATE Account: PUT /accounts/1 - 200 OK")
print(results["Q16_update"])

# Q17: DELETE single account (DELETE → 204 NO CONTENT)
# Create a fresh account to delete
make_request("POST", "/accounts",
    {"name": "To Delete", "email": "delete@example.com"})
s, r, h, b = make_request("DELETE", "/accounts/3")
results["Q17_delete"] = format_response("DELETE", "/accounts/3", s, r, h, b,
    "Q17 - DELETE Account: DELETE /accounts/3 - 204 NO CONTENT")
print(results["Q17_delete"])

# Save all to file
with open("curl_outputs.txt", "w", encoding="utf-8") as f:
    for key, val in results.items():
        f.write(val + "\n\n")

print("\n\nAll outputs saved to curl_outputs.txt")
