import sys
import os
import unittest
from main import App
sys.path.append(os.getcwd())

class TestApp(unittest.TestCase):
    def setUp(self):
        app = App().app
        app.testing = True
        self.client = app.test_client()

    def check_index(self, response):
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertEqual(data.count("<nav"), 1)
        self.assertEqual(data.count("<img"), 0)
    
    def check_login(self):
        with self.client.session_transaction() as session:
            self.assertIn("id", session)
            self.assertIn("username", session)
        
    def check_logout(self):
        with self.client.session_transaction() as session:
            self.assertNotIn("id", session)
            self.assertNotIn("username", session)