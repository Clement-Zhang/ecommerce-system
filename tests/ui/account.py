import sys
import os
from unittest.mock import patch
from tests.ui.app import TestApp
sys.path.append(os.getcwd())


class TestAppAccount(TestApp):
    def test_register_frontend(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count("Register"), 2)

    @patch("services.sql.account.Account.add_user", return_value=True)
    @patch("services.sql.account.Account.get_user_by_username_password", return_value={"id": 1, "username": "username"})
    def test_register_backend_pass(self, mock_add_user, mock_get_user_by_username_password):
        response = self.client.post("/register", data={"username": "username", "password": "password",
                                    "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.check_index(response)

    @patch("services.sql.account.Account.add_user", return_value=False)
    def test_register_backend_fail(self, mock_add_user):
        response = self.client.post("/register", data={"id": 1, "username": "username", "password": "password",
                                    "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(
            as_text=True).count("Account already exists"), 1)

    @patch("services.sql.account.Account.get_user_by_id", return_value={"id": 1, "username": "username", "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"})
    def test_account(self, mock_get_user_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/account")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count(
            "View and edit your account details"), 1)

    @patch("services.sql.account.Account.change_password", return_value=True)
    @patch("services.sql.account.Account.get_user_by_id", return_value={"id": 1, "username": "username", "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"})
    def test_change_password(self, mock_change_password, mock_get_user_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post(
            "/change_password", data={"password": "password"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count(
            "View and edit your account details"), 1)

    @patch("services.sql.account.Account.existing_user", return_value=True)
    @patch("services.sql.account.Account.get_user_by_username_email", return_value={"id": 1})
    @patch("services.sql.account.Account.change_password", return_value=True)
    @patch("services.sql.account.Account.get_user_by_username_password", return_value={"id": 1, "username": "username"})
    def test_reset_password_pass(self, mock_existing_user, mock_get_user_by_username_email, mock_change_password, mock_get_user_by_username_password):
        response = self.client.post(
            "/reset_password", data={"username": "username", "email": "js@yahoo.ca", "password": "password"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.check_index(response)

    @patch("services.sql.account.Account.existing_user", return_value=False)
    def test_reset_password_fail(self, mock_existing_user):
        response = self.client.post(
            "/reset_password", data={"username": "username", "email": "js@yahoo.ca", "password": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count(
            "Username or password is incorrect. Please give the correct credentials or make a new account"), 1)
        self.check_logout()

    @patch("services.sql.account.Account.update_fname", return_value=True)
    @patch("services.sql.account.Account.get_user_by_id", return_value={"id": 1, "username": "username", "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"})
    def test_change_fname(self, mock_update_fname, mock_get_user_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post(
            "/change_fname", data={"fname": "John"}, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("View and edit your account details"), 1)
        self.assertEqual(data.count("First Name: John"), 1)

    @patch("services.sql.account.Account.update_lname", return_value=True)
    @patch("services.sql.account.Account.get_user_by_id", return_value={"id": 1, "username": "username", "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"})
    def test_change_lname(self, mock_update_lname, mock_get_user_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post(
            "/change_lname", data={"lname": "Smith"}, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("View and edit your account details"), 1)
        self.assertEqual(data.count("Last Name: Smith"), 1)

    @patch("services.sql.account.Account.update_email", return_value=True)
    @patch("services.sql.account.Account.get_user_by_id", return_value={"id": 1, "username": "username", "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"})
    def test_change_email(self, mock_update_email, mock_get_user_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post(
            "/change_email", data={"email": "js@yahoo.ca"}, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("View and edit your account details"), 1)
        self.assertEqual(data.count("Email: js@yahoo.ca"), 1)

    @patch("services.sql.account.Account.update_phone", return_value=True)
    @patch("services.sql.account.Account.get_user_by_id", return_value={"id": 1, "username": "username", "fname": "John", "lname": "Smith", "email": "js@yahoo.ca", "phone": "1234567890"})
    def test_change_phone(self, mock_update_phone, mock_get_user_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post(
            "/change_phone", data={"phone": "1234567890"}, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("View and edit your account details"), 1)
        self.assertEqual(data.count("Phone: 1234567890"), 1)
