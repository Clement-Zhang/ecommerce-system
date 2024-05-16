from tests.sql.sql import TestSql
from services.sql.cart import Cart
from services.sql.interactive import Interactive
import sys
import os
sys.path.append(os.getcwd())


class TestCart(TestSql):
    def test_get_cart_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        cart = Cart.get_cart(user["id"])
        self.assertEqual(cart["account_id"], user["id"])
        Interactive.wipe()

    def test_get_cart_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        cart1 = Cart.get_cart(users[0]["id"])
        cart2 = Cart.get_cart(users[1]["id"])
        self.assertEqual(cart1["account_id"], users[0]["id"])
        self.assertEqual(cart2["account_id"], users[1]["id"])
        Interactive.wipe()

    def test_get_cart_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Cart.get_cart(1))
        Interactive.wipe()

    def test_add_to_cart_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.add_to_cart(user["id"], products[0]["id"], 1)
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products[0]["quantity"], 1)
        Interactive.wipe()

    def test_add_to_cart_noisy(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.add_to_cart(user["id"], products[0]["id"], 1)
        Cart.add_to_cart(user["id"], products[1]["id"], 1)
        products = Cart.get_cart_products(user["id"])
        quantities = [product["quantity"] for product in products]
        self.assertEqual(quantities, [1, 1])
        self.assertEqual(len(products), 2)
        Interactive.wipe()

    def test_add_to_cart_no_user(self):
        Interactive.wipe()
        products = self.setup_product_single()
        self.assertIsNone(Cart.add_to_cart(1, products[0]["id"], 1))
        Interactive.wipe()

    def test_add_to_cart_no_product(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertIsNone(Cart.add_to_cart(user["id"], 1, 1))
        Interactive.wipe()

    def test_add_to_cart_no_quantity(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.add_to_cart(user["id"], products[0]["id"], 0)
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()
    
    def test_add_to_cart_negative_quantity(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.add_to_cart(user["id"], products[0]["id"], -1)
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_add_to_cart_duplicate(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.add_to_cart(user["id"], products[0]["id"], 1)
        Cart.add_to_cart(user["id"], products[0]["id"], 1)
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products[0]["quantity"], 2)
        Interactive.wipe()

    def test_get_cart_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        cart = Cart.get_cart(user["id"])
        self.assertEqual(cart["account_id"], user["id"])
        Interactive.wipe()

    def test_get_cart_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        cart1 = Cart.get_cart(users[0]["id"])
        cart2 = Cart.get_cart(users[1]["id"])
        self.assertEqual(cart1["account_id"], users[0]["id"])
        self.assertEqual(cart2["account_id"], users[1]["id"])
        Interactive.wipe()

    def test_get_cart_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Cart.get_cart(1))
        Interactive.wipe()

    def test_get_cart_products_empty(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.setup_product_single()
        cart_products = Cart.get_cart_products(user["id"])
        self.assertEqual(cart_products, [])
        Interactive.wipe()

    def test_get_cart_products_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        cart_products = Cart.get_cart_products(user["id"])
        self.assertEqual(cart_products[0]["quantity"], 1)
        Interactive.wipe()

    def test_get_cart_products_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(
            user["id"], [(products[0]["id"], 1), (products[1]["id"], 2)])
        cart_products = Cart.get_cart_products(user["id"])
        quantities = [cart_product["quantity"]
                      for cart_product in cart_products]
        self.assertIn(1, quantities)
        self.assertIn(2, quantities)
        self.assertEqual(len(cart_products), 2)
        Interactive.wipe()

    def test_get_cart_products_noisy(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        cart_products = Cart.get_cart_products(user["id"])
        self.assertEqual(cart_products[0]["quantity"], 1)
        self.assertEqual(len(cart_products), 1)
        Interactive.wipe()

    def test_get_cart_total_zero(self):
        Interactive.wipe()
        user = self.setup_user_single()
        total = Cart.get_cart_total(user["id"])
        self.assertIsNone(total)
        Interactive.wipe()

    def test_get_cart_total_positive(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        total = Cart.get_cart_total(user["id"])
        self.assertAlmostEqual(total, 1.2)
        Interactive.wipe()

    def test_get_cart_total_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        products = self.setup_product_single()
        Cart.update_cart(users[0]["id"], [(products[0]["id"], 1)])
        total1 = Cart.get_cart_total(users[0]["id"])
        self.assertAlmostEqual(total1, 1.2)
        self.assertIsNone(Cart.get_cart_total(users[1]["id"]))

    def test_get_cart_total_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Cart.get_cart_total(1))
        Interactive.wipe()

    def test_check_cart_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertTrue(Cart.check_cart(user["id"]))
        Interactive.wipe()

    def test_check_cart_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        self.assertTrue(Cart.check_cart(users[0]["id"]))
        self.assertTrue(Cart.check_cart(users[1]["id"]))
        Interactive.wipe()

    def test_check_cart_no_user(self):
        Interactive.wipe()
        self.assertFalse(Cart.check_cart(1))
        Interactive.wipe()

    def test_check_cart_product_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        self.assertTrue(Cart.check_cart_product(user["id"], products[0]["id"]))
        Interactive.wipe()

    def test_check_cart_product_noisy1(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        self.assertTrue(Cart.check_cart_product(user["id"], products[0]["id"]))
        self.assertFalse(Cart.check_cart_product(
            user["id"], products[1]["id"]))
        Interactive.wipe()

    def test_check_cart_product_noisy2(self):
        Interactive.wipe()
        users = self.setup_user_double()
        products = self.setup_product_single()
        Cart.update_cart(users[0]["id"], [(products[0]["id"], 1)])
        self.assertTrue(Cart.check_cart_product(
            users[0]["id"], products[0]["id"]))
        self.assertFalse(Cart.check_cart_product(
            users[1]["id"], products[0]["id"]))
        Interactive.wipe()

    def test_check_cart_product_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Cart.check_cart_product(1, 1))
        Interactive.wipe()

    def test_check_cart_product_no_product(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertFalse(Cart.check_cart_product(user["id"], 1))
        Interactive.wipe()

    def test_update_cart_empty(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Cart.update_cart(user["id"], [])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_update_cart_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products[0]["quantity"], 1)
        Interactive.wipe()

    def test_update_cart_additional(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(
            user["id"], [(products[0]["id"], 1), (products[1]["id"], 2)])
        products = Cart.get_cart_products(user["id"])
        quantities = [product["quantity"] for product in products]
        self.assertIn(1, quantities)
        self.assertIn(2, quantities)
        self.assertEqual(len(products), 2)
        Interactive.wipe()

    def test_update_cart_set(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(
            user["id"], [(products[0]["id"], 1), (products[0]["id"], 2)])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products[0]["quantity"], 2)
        Interactive.wipe()

    def test_update_cart_noisy1(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products[0]["quantity"], 1)
        Interactive.wipe()

    def test_update_cart_noisy2(self):
        Interactive.wipe()
        users = self.setup_user_double()
        products = self.setup_product_single()
        Cart.update_cart(users[0]["id"], [(products[0]["id"], 1)])
        products1 = Cart.get_cart_products(users[0]["id"])
        products2 = Cart.get_cart_products(users[1]["id"])
        self.assertEqual(products1[0]["quantity"], 1)
        self.assertEqual(products2, [])
        Interactive.wipe()

    def test_update_cart_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Cart.update_cart(1, [(1, 1)]))
        Interactive.wipe()

    def test_update_cart_no_product(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertIsNone(Cart.update_cart(user["id"], [(1, 1)]))
        Interactive.wipe()

    def test_update_cart_no_quantity(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(
            user["id"], [(products[0]["id"], 1), (products[0]["id"], 0)])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_remove_from_cart_empty(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Cart.remove_from_cart(user["id"], [])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_remove_from_cart_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        Cart.remove_from_cart(user["id"], [products[0]["id"]])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_remove_from_cart_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(
            user["id"], [(products[0]["id"], 1), (products[1]["id"], 2)])
        Cart.remove_from_cart(
            user["id"], [products[0]["id"], products[1]["id"]])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_remove_from_cart_all(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_multiple()
        Cart.update_cart(user["id"], [(products[0]["id"], 1),
                         (products[1]["id"], 2), (products[2]["id"], 3)])
        Cart.remove_from_cart(
            user["id"], [products[0]["id"], products[1]["id"], products[2]["id"]])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_remove_from_cart_noisy1(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(
            user["id"], [(products[0]["id"], 1), (products[1]["id"], 2)])
        Cart.remove_from_cart(user["id"], [products[0]["id"]])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products[0]["quantity"], 2)
        Interactive.wipe()

    def test_remove_from_cart_noisy2(self):
        Interactive.wipe()
        users = self.setup_user_double()
        products = self.setup_product_single()
        Cart.update_cart(users[0]["id"], [(products[0]["id"], 1)])
        Cart.remove_from_cart(users[0]["id"], [])
        products = Cart.get_cart_products(users[0]["id"])
        self.assertEqual(products[0]["quantity"], 1)
        Interactive.wipe()

    def test_remove_from_cart_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Cart.remove_from_cart(1, [1]))
        Interactive.wipe()

    def test_remove_from_cart_no_product(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Cart.remove_from_cart(user["id"], [1])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_empty_cart_empty(self):
        Interactive.wipe()
        user = self.setup_user_single()
        Cart.empty_cart(user["id"])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_empty_cart_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        Cart.update_cart(user["id"], [(products[0]["id"], 1)])
        Cart.empty_cart(user["id"])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_empty_cart_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        Cart.update_cart(
            user["id"], [(products[0]["id"], 1), (products[1]["id"], 2)])
        Cart.empty_cart(user["id"])
        products = Cart.get_cart_products(user["id"])
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_empty_cart_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        products = self.setup_product_single()
        Cart.update_cart(users[0]["id"], [(products[0]["id"], 1)])
        Cart.empty_cart(users[1]["id"])
        products1 = Cart.get_cart_products(users[0]["id"])
        products2 = Cart.get_cart_products(users[1]["id"])
        self.assertEqual(products1[0]["quantity"], 1)
        self.assertEqual(products2, [])

    def test_empty_cart_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Cart.empty_cart(1))
        Interactive.wipe()
