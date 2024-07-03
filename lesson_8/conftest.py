# import pytest
# import requests
# from lesson_8.constants import X_client_URL

# @pytest.fixture(scope='session')
# def get_token():
#     username = "raphael"
#     password = "cool-but-crude"
#     log_pass = {"username": username, "password": password}
#     resp_token = requests.post(X_client_URL + "/auth/login", json=log_pass)
#     resp_token.raise_for_status()
#     token = resp_token.json()["userToken"]
#     return token
