from tests.sql.sql import TestSql
from services.crypto import Crypto
from services.sql.account import Account
from services.sql.interactive import Interactive
import sys
import os
sys.path.append(os.getcwd())


class TestAccount(TestSql):
    def test_add_user_pass(self):
        Interactive.wipe()
        Account.add_customer("blah", Crypto.hash_password("123"),
                         "John", "Smith", "js@yahoo.ca", "1234567890")
        user = Account.get_user_by_username_email("blah", "js@yahoo.ca")
        self.assertEqual(user["username"], "blah")
        Interactive.wipe()

    def test_add_user_duplicate_username(self):
        Interactive.wipe()
        self.setup_user_single()
        self.assertIsNone(Account.add_customer("blah", Crypto.hash_password(
            "321"), "Jane", "Doe", "jd@yahoo.ca", "0987654321"))
        Interactive.wipe()

    def test_add_user_duplicate_email(self):
        Interactive.wipe()
        self.setup_user_single()
        self.assertIsNone(Account.add_customer("bl", Crypto.hash_password(
            "321"), "Jane", "Doe", "js@yahoo.ca", "0987654321"))
        Interactive.wipe()

    def test_add_user_allowed_duplicates(self):
        Interactive.wipe()
        user1 = self.setup_user_single()
        Account.add_customer("bl", Crypto.hash_password("123"),
                         "John", "Smith", "jd@yahoo.ca", "1234567890")
        user2 = Account.get_user_by_username_email("bl", "jd@yahoo.ca")
        self.assertEqual(user1["username"], "blah")
        self.assertEqual(user2["username"], "bl")
        Interactive.wipe()
    
    def test_get_user_by_id_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertEqual(Account.get_user_by_id(user["id"])["username"], "blah")
        Interactive.wipe()
    
    def test_get_user_by_id_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        self.assertEqual(Account.get_user_by_id(users[0]["id"])["username"], "blah")
        self.assertEqual(Account.get_user_by_id(users[1]["id"])["username"], "bl")
        Interactive.wipe()
    
    def test_get_user_by_id_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.get_user_by_id(1))
        Interactive.wipe()
    
    def test_get_user_by_username_email_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertEqual(Account.get_user_by_username_email("blah", "js@yahoo.ca")["id"], user["id"])
        Interactive.wipe()
    
    def test_get_user_by_username_email_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        self.assertEqual(Account.get_user_by_username_email("blah", "js@yahoo.ca")["id"], users[0]["id"])
        self.assertEqual(Account.get_user_by_username_email("bl", "jd@yahoo.ca")["id"], users[1]["id"])
        Interactive.wipe()
    
    def test_get_user_by_username_email_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.get_user_by_username_email("blah", "js@yahoo.ca"))
        Interactive.wipe()
    
    def test_get_user_by_username_email_wrong_username(self):
        Interactive.wipe()
        self.setup_user_single()
        self.assertIsNone(Account.get_user_by_username_email("bl", "js@yahoo.ca"))
        Interactive.wipe()
    
    def test_get_user_by_username_email_wrong_email(self):
        Interactive.wipe()
        self.setup_user_single()
        self.assertIsNone(Account.get_user_by_username_email("blah", "jd@yahoo.ca"))
        Interactive.wipe()
    
    def test_get_user_by_username_password_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertEqual(Account.get_user_by_username_password("blah", Crypto.hash_password("123"))["id"], user["id"])
        Interactive.wipe()
    
    def test_get_user_by_username_password_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        self.assertEqual(Account.get_user_by_username_password("blah", Crypto.hash_password("123"))["id"], users[0]["id"])
        self.assertEqual(Account.get_user_by_username_password("bl", Crypto.hash_password("123"))["id"], users[1]["id"])
        Interactive.wipe()
    
    def test_get_user_by_username_password_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.get_user_by_username_password("blah", Crypto.hash_password("123")))
        Interactive.wipe()
    
    def test_get_user_by_username_password_wrong_username(self):
        Interactive.wipe()
        self.setup_user_single()
        self.assertIsNone(Account.get_user_by_username_password("bl", Crypto.hash_password("123")))
        Interactive.wipe()
    
    def test_get_user_by_username_password_wrong_password(self):
        Interactive.wipe()
        self.setup_user_single()
        self.assertIsNone(Account.get_user_by_username_password("blah", Crypto.hash_password("12")))
        Interactive.wipe()

    def test_validate_user_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertTrue(Account.validate_user(
            user["username"], user["password"]))
        Interactive.wipe()

    def test_validate_user_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        self.assertTrue(Account.validate_user(
            users[0]["username"], users[0]["password"]))
        self.assertTrue(Account.validate_user(
            users[1]["username"], users[1]["password"]))
        Interactive.wipe()

    def test_validate_user_wrong_username(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertFalse(Account.validate_user("bl", user["password"]))
        Interactive.wipe()

    def test_validate_user_wrong_password(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertFalse(Account.validate_user(
            user["username"], Crypto.hash_password("12")))
        Interactive.wipe()

    def test_existing_user_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertTrue(Account.existing_user(user["username"], user["email"]))
        Interactive.wipe()

    def test_existing_user_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        self.assertTrue(Account.existing_user(
            users[0]["username"], users[0]["email"]))
        self.assertTrue(Account.existing_user(
            users[1]["username"], users[1]["email"]))
        Interactive.wipe()

    def test_existing_user_no_user(self):
        Interactive.wipe()
        self.assertFalse(Account.existing_user("blah", "js@yahoo.ca"))
        Interactive.wipe()

    def test_check_user_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertTrue(Account.check_user(user["id"]))
        Interactive.wipe()

    def test_check_user_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        self.assertTrue(Account.check_user(users[0]["id"]))
        self.assertTrue(Account.check_user(users[1]["id"]))
        Interactive.wipe()

    def test_check_user_no_user(self):
        Interactive.wipe()
        self.assertFalse(Account.check_user(1))
        Interactive.wipe()

    def test_change_password_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Account.change_password(user["id"], Crypto.hash_password("321"))
        self.assertEqual(Account.get_user_by_id(user["id"])[
                         "password"], Crypto.hash_password("321"))
        Interactive.wipe()

    def test_change_password_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        Account.change_password(users[0]["id"], Crypto.hash_password("321"))
        Account.change_password(users[1]["id"], Crypto.hash_password("456"))
        self.assertEqual(Account.get_user_by_id(users[0]["id"])[
                         "password"], Crypto.hash_password("321"))
        self.assertEqual(Account.get_user_by_id(users[1]["id"])[
                         "password"], Crypto.hash_password("456"))
        Interactive.wipe()

    def test_change_password_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.change_password(
            1, Crypto.hash_password("321")))
        Interactive.wipe()

    def test_update_fname_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Account.update_fname(user["id"], "Jane")
        user = Account.get_user_by_id(user["id"])
        self.assertEqual(user["fname"], "Jane")
        Interactive.wipe()

    def test_update_fname_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        Account.update_fname(users[0]["id"], "Jane")
        Account.update_fname(users[1]["id"], "John")
        user1 = Account.get_user_by_id(users[0]["id"])
        user2 = Account.get_user_by_id(users[1]["id"])
        self.assertEqual(user1["fname"], "Jane")
        self.assertEqual(user2["fname"], "John")

    def test_update_fname_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.update_fname(1, "Jane"))
        Interactive.wipe()

    def test_update_lname_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Account.update_lname(user["id"], "Doe")
        user = Account.get_user_by_username_email("blah", "js@yahoo.ca")
        self.assertEqual(user["lname"], "Doe")
        Interactive.wipe()

    def test_update_lname_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        Account.update_lname(users[0]["id"], "Doe")
        Account.update_lname(users[1]["id"], "Smith")
        user1 = Account.get_user_by_id(users[0]["id"])
        user2 = Account.get_user_by_id(users[1]["id"])
        self.assertEqual(user1["lname"], "Doe")
        self.assertEqual(user2["lname"], "Smith")
        Interactive.wipe()

    def test_update_lname_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.update_lname(1, "Doe"))
        Interactive.wipe()

    def test_update_email_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Account.update_email(user["id"], "js@gmail.com")
        user = Account.get_user_by_username_email("blah", "js@gmail.com")
        self.assertEqual(user["email"], "js@gmail.com")
        Interactive.wipe()

    def test_update_email_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        Account.update_email(users[0]["id"], "js@gmail.com")
        Account.update_email(users[1]["id"], "jd@gmail.com")
        user1 = Account.get_user_by_id(users[0]["id"])
        user2 = Account.get_user_by_id(users[1]["id"])
        self.assertEqual(user1["email"], "js@gmail.com")
        self.assertEqual(user2["email"], "jd@gmail.com")
        Interactive.wipe()

    def test_update_email_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.update_email(1, "js@yahoo.ca"))
        Interactive.wipe()

    def test_update_email_duplicate(self):
        Interactive.wipe()
        self.setup_user_single()
        self.assertIsNone(Account.add_customer("bl", Crypto.hash_password(
            "123"), "John", "Smith", "js@yahoo.ca", "1234567890"))
        Interactive.wipe()

    def test_update_phone_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Account.update_phone(user["id"], "0987654321")
        user = Account.get_user_by_username_email("blah", "js@yahoo.ca")
        self.assertEqual(user["phone"], "0987654321")
        Interactive.wipe()

    def test_update_phone_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        Account.update_phone(users[0]["id"], "0987654321")
        Account.update_phone(users[1]["id"], "1234567890")
        user1 = Account.get_user_by_id(users[0]["id"])
        user2 = Account.get_user_by_id(users[1]["id"])
        self.assertEqual(user1["phone"], "0987654321")
        self.assertEqual(user2["phone"], "1234567890")
        Interactive.wipe()

    def test_update_phone_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Account.update_phone(1, "0987654321"))
        Interactive.wipe()
