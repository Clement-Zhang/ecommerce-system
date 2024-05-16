import sys
import os
from unittest.mock import patch
from tests.ui.app import TestApp
sys.path.append(os.getcwd())


class TestAppDisplay(TestApp):
    def test_index_logged_out(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.check_index(response)
        self.assertEqual(data.count("Login"), 1)
        self.assertEqual(data.count("Register"), 1)
        self.assertEqual(data.count("Logout"), 0)
        self.assertEqual(data.count("Account"), 0)
        self.assertEqual(data.count("Cart"), 0)
        self.assertEqual(data.count("Orders"), 0)

    def test_index_logged_in(self):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.check_index(response)
        self.assertEqual(data.count("Login"), 0)
        self.assertEqual(data.count("Register"), 0)
        self.assertEqual(data.count("Logout"), 1)
        self.assertEqual(data.count("Account"), 1)
        self.assertEqual(data.count("Cart"), 1)
        self.assertEqual(data.count("Orders"), 1)

    @patch("services.sql.product.Product.get_products", return_value=[])
    def test_products_empty(self, mock_get_products):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn("No products", response.get_data(as_text=True))

    @patch("services.sql.product.Product.get_products", return_value=[{"id": 1, "name": "product", "price": 1.0, "description": "description", "img_path": "error.jpg", "quantity": 5}])
    def test_products_single(self, mock_get_products):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count("card "), 1)

    @patch("services.sql.product.Product.get_products", return_value=[{"id": 1, "name": "product", "price": 1.0, "description": "description", "img_path": "error.jpg", "quantity": 5}, {"id": 2, "name": "product", "price": 1.0, "description": "description", "img_path": "error.jpg", "quantity": 5}])
    def test_products_double(self, mock_get_products):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count("card "), 2)
    
    @patch("services.sql.product.Product.get_products", return_value=[{"id": 1, "name": "product", "price": 1.0, "description": "description", "img_path": "error.jpg", "quantity": 0}])
    def test_products_zero_quantity(self, mock_get_products):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count("card "), 1)

    @patch("services.sql.product.Product.get_products", return_value=[{"id": 1, "name": "product", "price": 1.0, "description": "description", "img_path": "error.jpg", "quantity": 5}])
    @patch("services.sql.cart.Cart.get_cart_products", return_value=[])
    def test_products_empty_cart(self, mock_get_cart_products, mock_get_product_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/products")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Add to Cart"), 1)
        self.assertEqual(data.count("max=\"5\""), 1)
        self.assertEqual(data.count("min=\"0\""), 1)
        self.assertEqual(data.count("value=\"0\""), 1)
    
    @patch("services.sql.product.Product.get_products", return_value=[{"id": 1, "name": "product", "price": 1.0, "description": "description", "img_path": "error.jpg", "quantity": 5}])
    @patch("services.sql.cart.Cart.get_cart_products", return_value=[{"id": 1, "quantity": 2}])
    def test_products_nonempty_cart(self, mock_get_cart_products, mock_get_product_by_id):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/products")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Update Cart"), 1)
        self.assertEqual(data.count("max=\"5\""), 1)
        self.assertEqual(data.count("min=\"0\""), 1)
        self.assertEqual(data.count("value=\"2\""), 1)

    @patch("services.sql.order.Order.get_order", return_value={"id": 1, "total_price": 1.0})
    @patch("services.sql.order.Order.get_order_products", return_value=[{"id": 1, "name":"p1", "price": 1.0, "quantity": 1}])
    def test_order(self, mock_get_order_products, mock_get_order):
        with self.client.session_transaction() as session:
            session["id"] = 1
            session["username"] = "username"
        response = self.client.get("/orders/1")
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.count("Details for Order 1"), 1)
        self.assertEqual(data.count("p1"), 1)