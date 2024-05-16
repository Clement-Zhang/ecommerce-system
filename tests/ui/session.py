import sys
import os
from unittest.mock import patch
from tests.ui.app import TestApp
sys.path.append(os.getcwd())


class TestAppSession(TestApp):
    def test_login_frontend(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count("Login"), 2)
        self.check_logout()
    
    @patch("services.sql.account.Account.validate_user", return_value=True)
    @patch("services.sql.account.Account.get_user_by_username_password", return_value={"id": 1, "username": "username"})
    def test_login_backend_pass(self, mock_validate_user, mock_get_user_by_username_password):
        response = self.client.post("/login_backend", data={"username": "username", "password": "password"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.check_index(response)
        self.check_login()
    
    @patch("services.sql.account.Account.validate_user", return_value=False)
    @patch("services.sql.account.Account.get_user_by_username_password", return_value=None)
    def test_login_backend_fail(self, mock_validate_user, mock_get_user_by_username_password):
        response = self.client.post("/login_backend", data={"username": "username", "password": "password"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count("Invalid username or password"), 1)
        self.check_logout()
    
    def test_logout(self):
        with self.client.session_transaction() as session:
            session["id"]= 1
            session["username"]= "username"
        response = self.client.get("/logout_backend", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.check_index(response)
        self.check_logout()