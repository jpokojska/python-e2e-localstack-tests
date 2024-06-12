import pytest
import os

from api.data.register import RegisterRequestDto
from api.post_sign_up import SignUp
from dotenv import load_dotenv
import requests
from generators.user_generator import get_random_user

load_dotenv()

@pytest.fixture
def sign_up_api():
    return SignUp()

def test_successful_api_signup(sign_up_api: SignUp):
    user = get_random_user()
    response = sign_up_api.api_call(user)
    try:
        response.raise_for_status()
        assert response.status_code == 201, "Expected status code 201 for successful signup"
        assert response.json()['token'] is not None, "Token should not be None in the response"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")

def test_should_return_400_if_username_or_password_too_short(sign_up_api: SignUp):
    try:
        user = get_random_user()
        user.username = "one"  # Set username to be too short
        response = sign_up_api.api_call(user)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400 for short username"
        assert "username length" in e.response.json()["username"], "Username error should mention length"

def test_should_return_400_on_invalid_data(sign_up_api: SignUp):
    try:
        # Create a user with invalid data that should result in a 400 response
        user = RegisterRequestDto(username="", email="invalid_email", password="short", roles=["ROLE_ADMIN"], firstName="John", lastName="Doe")
        response = sign_up_api.api_call(user)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400 for invalid data"

def test_should_return_422_on_not_existing_user(sign_up_api: SignUp):
    try:
        # Simulate a scenario where the username/password doesn't exist
        user = get_random_user()
        user.username = "nonexistent_user"
        response = sign_up_api.api_call(user)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 422, "Expected status code 422 for nonexisting user"
