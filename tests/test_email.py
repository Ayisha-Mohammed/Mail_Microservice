
def test_unauthorized_access(client_unauthorized):
    response = client_unauthorized.post(
        "/email/send-email",
        json={
            "to_email": "someone@example.com",
            "subject": "Test Unauthorized",
            "body": "Hello from unauthorized test"
        }
    )
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"

def test_send_email_valid(client_logged_in):
    payload = {
        "to_email": "test@example.com",
        "subject": "Test Email",
        "body": "Hello from test suite!"
    }
    response = client_logged_in.post("/email/send-email", json=payload)
    assert response.status_code in (200, 201), f"Expected 200/201, got {response.status_code}"

def test_rate_limit_trigger(client_logged_in):
    payload = {
        "to_email": "limit@example.com",
        "subject": "Rate Limit Test",
        "body": "Testing rate limiter"
    }

    last_response = None
    for i in range(6): 
        last_response = client_logged_in.post("/email/send-email", json=payload)

    assert last_response.status_code == 429, (
        f"Expected 429 after exceeding limit, got {last_response.status_code}"
    )
