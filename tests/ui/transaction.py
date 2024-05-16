import sys
import os
from unittest.mock import patch
from tests.ui.app import TestApp
sys.path.append(os.getcwd())


class TestAppTransaction(TestApp):
    @patch("services.sql.cart.Cart.update_cart", return_value=True)
    @patch("services.sql.cart.Cart.get_cart_products", return_value=[])
    @patch("services.sql.cart.Cart.get_cart_total", return_value=None)
    def test_cart_add_to_cart(self, mock_update_cart, mock_get_cart_products, mock_get_cart_total):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post(
            "/add_to_cart", data={}, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Cart"), 2)
        self.assertEqual(data.count("Checkout"), 0)

    @patch("services.sql.cart.Cart.get_cart_products", return_value=[])
    @patch("services.sql.cart.Cart.get_cart_total", return_value=None)
    def test_cart_empty(self, mock_get_cart_products, mock_get_cart_total):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/cart")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Cart"), 2)
        self.assertEqual(data.count("Checkout"), 0)

    @patch("services.sql.cart.Cart.get_cart_products", return_value=[{"id": 1, "name": "p1", "price": 1.0, "quantity": 1}])
    @patch("services.sql.cart.Cart.get_cart_total", return_value=1.0)
    def test_cart_single(self, mock_get_cart_products, mock_get_cart_total):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/cart")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("p1"), 1)
        self.assertEqual(data.count("Checkout"), 1)

    @patch("services.sql.cart.Cart.get_cart_products", return_value=[{"id": 1, "name": "p1", "price": 1.0, "quantity": 1}, {"id": 2, "name": "p2", "price": 1.0, "quantity": 1}])
    @patch("services.sql.cart.Cart.get_cart_total", return_value=2.0)
    def test_cart_double(self, mock_get_cart_products, mock_get_cart_total):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/cart")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("p1"), 1)
        self.assertEqual(data.count("p2"), 1)
        self.assertEqual(data.count("Checkout"), 1)

    @patch("services.sql.cart.Cart.remove_from_cart", return_value=True)
    @patch("services.sql.cart.Cart.get_cart_products", return_value=[{"id": 1, "name": "p1", "price": 1.0, "quantity": 1}])
    @patch("services.sql.cart.Cart.get_cart_total", return_value=1.0)
    def test_cart_remove(self, mock_remove_from_cart, mock_get_cart_products, mock_get_cart_total):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post("/cart", data={}, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Cart"), 2)
        self.assertEqual(data.count("p1"), 1)

    @patch("services.sql.interactive.Interactive.checkout", return_value=True)
    @patch("services.sql.order.Order.get_orders", return_value=[])
    def test_checkout(self, mock_checkout, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/checkout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count("Order History"), 1)
    
    @patch("services.sql.order.Order.get_orders", return_value=[])
    def test_orders_empty(self, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/orders")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Order History"), 1)
        self.assertEqual(data.count("Cancel Selected Orders"), 0)
    
    @patch("services.sql.order.Order.get_orders", return_value=[{"id": 1, "total_price": 1.0, "status": "package", "created_at": "2021-01-01", "last_modified": "2021-01-01"}])
    def test_orders_single(self, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/orders")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Order History"), 1)
        self.assertEqual(data.count("We are getting your ordered items ready"), 1)
        self.assertEqual(data.count("Cancel Selected Orders"), 1)
    
    @patch("services.sql.order.Order.get_orders", return_value=[{"id": 1, "total_price": 1.0, "status": "package", "created_at": "2021-01-01", "last_modified": "2021-01-01"}, {"id": 2, "total_price": 1.0, "status": "package", "created_at": "2021-01-01", "last_modified": "2021-01-01"}])
    def test_orders_double(self, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/orders")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Order History"), 1)
        self.assertEqual(data.count("We are getting your ordered items ready"), 2)
        self.assertEqual(data.count("Cancel Selected Orders"), 1)
    
    @patch("services.sql.order.Order.get_orders", return_value=[{"id": 1, "total_price": 1.0, "status": "ship", "created_at": "2021-01-01", "last_modified": "2021-01-01"}])
    def test_orders_ship(self, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/orders")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Order History"), 1)
        self.assertEqual(data.count("checkbox"), 1)
        self.assertEqual(data.count("We are sending your ordered items to you"), 1)
    
    @patch("services.sql.order.Order.get_orders", return_value=[{"id": 1, "total_price": 1.0, "status": "arrive", "created_at": "2021-01-01", "last_modified": "2021-01-01"}])
    def test_orders_ship(self, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/orders")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Order History"), 1)
        self.assertEqual(data.count("checkbox"), 1)
        self.assertEqual(data.count("Your ordered items have been delivered"), 1)
    
    @patch("services.sql.order.Order.get_orders", return_value=[{"id": 1, "total_price": 1.0, "status": "cancel", "created_at": "2021-01-01", "last_modified": "2021-01-01"}])
    def test_orders_cancelled(self, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/orders")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Order History"), 1)
        self.assertEqual(data.count("checkbox"), 0)
        self.assertEqual(data.count("Your order has been cancelled"), 1)

    @patch("services.sql.order.Order.cancel_orders", return_value=True)
    @patch("services.sql.order.Order.get_orders", return_value=[{"id": 1, "total_price": 1.0, "status": "package", "created_at": "2021-01-01", "last_modified": "2021-01-01"}])
    def test_orders_cancel(self, mock_cancel_orders, mock_get_orders):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.post("/orders", data={}, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Order History"), 1)
        self.assertEqual(data.count("We are getting your ordered items ready"), 1)