import unittest
import requests

local_url = "http://127.0.0.1:9091"

register_existing_user = {
    "username": "krenil2",
    "password": "pass@123"
}

response_existing_user = {
    "message": "Username already exists"
}

register_invalid_username = {
    "username": "kre",
    "password": "pass@123"
}

response_invalid_username = {
    "message": "Enter a valid username"
}

register_invalid_password = {
    "username": "krenil2",
    "password": "pass"
}

response_invalid_password = {
    "message": "Enter a valid password"
}

register_new_user = {
    "username": "krenil99",
    "password": "pass@99"
}

response_new_user = {
    "message": "Successfully registered."
}


class TestAuthentication(unittest.TestCase):
    def test_register(self):
        # already_exist
        res = requests.get(local_url + "/api/register", json=register_existing_user)
        self.assertEqual(res.json(), response_existing_user)
        self.assertEqual(res.status_code, 400)
        # invalid_username
        res = requests.get(local_url + "/api/register", json=register_invalid_username)
        self.assertEqual(res.json(), response_invalid_username)
        self.assertEqual(res.status_code, 400)
        # invalid_password
        res = requests.get(local_url + "/api/register", json=register_invalid_password)
        self.assertEqual(res.json(), response_invalid_password)
        self.assertEqual(res.status_code, 400)

    def test_login(self):
        pass


if __name__ == "__main__":
    unittest.main()