import src.app as app_module


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Programming Class"
    email = "not-signed-up@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_signup_unregister_and_signup_again_workflow(client):
    # Arrange
    activity_name = "Debate Team"
    email = "workflow.student@mergington.edu"

    # Act
    first_signup = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    unregister = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    second_signup = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert first_signup.status_code == 200
    assert unregister.status_code == 200
    assert second_signup.status_code == 200
    participants = app_module.activities[activity_name]["participants"]
    assert participants.count(email) == 1


def test_state_isolation_uses_seed_data_each_test(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    participants = response.json()[activity_name]["participants"]
    assert participants == ["michael@mergington.edu", "daniel@mergington.edu"]
