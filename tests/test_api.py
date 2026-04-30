def test_get_activities(client):
    """Test GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check structure of one activity
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_root_redirect(client):
    """Test GET / redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_signup_success(client):
    """Test successful signup adds participant."""
    email = "test@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity}" in data["message"]

    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity]["participants"]


def test_signup_activity_not_found(client):
    """Test signup with invalid activity returns 404."""
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up(client):
    """Test signup when already signed up returns 400."""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_unregister_success(client):
    """Test successful unregister removes participant."""
    email = "daniel@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity}" in data["message"]

    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister with invalid activity returns 404."""
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_not_signed_up(client):
    """Test unregister when not signed up returns 400."""
    email = "notsignedup@mergington.edu"
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up for this activity" in data["detail"]