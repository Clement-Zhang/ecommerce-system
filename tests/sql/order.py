from tests.sql.sql import TestSql
from services.sql.order import Order
from services.sql.interactive import Interactive
import sys
import os
sys.path.append(os.getcwd())


class TestOrder(TestSql):
    def test_create_order_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 1)
        order = Order.get_order(oid)
        self.assertEqual(order["total_price"], 1)
        Interactive.wipe()

    def test_create_order_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        oid = Order.create_order(users[0]["id"], 1)
        orders1 = Order.get_orders(users[0]["id"])
        orders2 = Order.get_orders(users[1]["id"])
        self.assertEqual(orders1[0]["total_price"], 1)
        self.assertEqual(orders2, [])

    def test_create_order_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Order.create_order(1, 1))
        Interactive.wipe()

    def test_get_order_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 1)
        order = Order.get_order(oid)
        self.assertEqual(order["total_price"], 1)
        Interactive.wipe()

    def test_get_order_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid1 = Order.create_order(user["id"], 1)
        Order.create_order(user["id"], 2)
        orders = Order.get_orders(user["id"])
        prices = [order["total_price"] for order in orders]
        self.assertIn(1, prices)
        self.assertIn(2, prices)
        self.assertEqual(len(orders), 2)
        Interactive.wipe()

    def test_get_order_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        oid1 = Order.create_order(users[0]["id"], 1)
        order = Order.get_order(oid1)
        self.assertEqual(order["total_price"], 1)
        self.assertIsNone(Order.get_order(oid1 + 1))
        Interactive.wipe()

    def test_get_order_no_order(self):
        Interactive.wipe()
        self.assertIsNone(Order.get_order(1))
        Interactive.wipe()

    def test_get_order_products_empty(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 0)
        self.assertEqual(Order.get_order_products(oid), [])
        Interactive.wipe()

    def test_get_order_products_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        oid = Order.create_order(user["id"], 1.2)
        Order.add_order_product(
            oid, products[0]["id"], products[0]["price"], 1)
        order_products = Order.get_order_products(oid)
        self.assertEqual(order_products[0]["quantity"], 1)
        Interactive.wipe()

    def test_get_order_products_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        oid = Order.create_order(user["id"], 2.4)
        Order.add_order_product(
            oid, products[0]["id"], products[0]["price"], 1)
        Order.add_order_product(
            oid, products[1]["id"], products[1]["price"], 1)
        order_products = Order.get_order_products(oid)
        quantities = [order_products["quantity"]
                      for order_products in order_products]
        self.assertEqual(quantities, [1, 1])
        Interactive.wipe()

    def test_get_order_products_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        product = self.setup_product_single()
        oid1 = Order.create_order(users[0]["id"], 1)
        oid2 = Order.create_order(users[1]["id"], 2)
        Order.add_order_product(oid1, product[0]["id"], product[0]["price"], 1)
        order_products1 = Order.get_order_products(oid1)
        order_products2 = Order.get_order_products(oid2)
        self.assertEqual(order_products1[0]["quantity"], 1)
        self.assertEqual(order_products2, [])
        Interactive.wipe()

    def test_get_order_products_no_order(self):
        Interactive.wipe()
        self.assertIsNone(Order.get_order_products(1), [])
        Interactive.wipe()

    def test_get_order_total_zero(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 0)
        self.assertEqual(Order.get_order_total(oid), 0)
        Interactive.wipe()

    def test_get_order_total_positive(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 1.2)
        self.assertEqual(Order.get_order_total(oid), 1.2)
        Interactive.wipe()

    def test_get_order_total_noisy(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid1 = Order.create_order(user["id"], 1.2)
        oid2 = Order.create_order(user["id"], 2.4)
        self.assertEqual(Order.get_order_total(oid1), 1.2)
        self.assertEqual(Order.get_order_total(oid2), 2.4)
        Interactive.wipe()

    def test_get_order_total_no_order(self):
        Interactive.wipe()
        self.assertIsNone(Order.get_order_total(1))
        Interactive.wipe()

    def test_get_orders_empty(self):
        Interactive.wipe()
        user = self.setup_user_single()
        self.assertEqual(Order.get_orders(user["id"]), [])
        Interactive.wipe()

    def test_get_orders_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 1)
        orders = Order.get_orders(user["id"])
        self.assertEqual(orders[0]["id"], oid)
        Interactive.wipe()

    def test_get_orders_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid1 = Order.create_order(user["id"], 1)
        oid2 = Order.create_order(user["id"], 2)
        orders = Order.get_orders(user["id"])
        ids = [order["id"] for order in orders]
        self.assertIn(oid1, ids)
        self.assertIn(oid2, ids)
        Interactive.wipe()

    def test_get_orders_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        oid1 = Order.create_order(users[0]["id"], 1)
        orders1 = Order.get_orders(users[0]["id"])
        orders2 = Order.get_orders(users[1]["id"])
        self.assertEqual(orders1[0]["id"], oid1)
        self.assertEqual(orders2, [])
        Interactive.wipe()

    def test_get_orders_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Order.get_orders(1))
        Interactive.wipe()

    def test_check_order_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 1)
        self.assertTrue(Order.check_order(oid))
        Interactive.wipe()

    def test_check_order_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid1 = Order.create_order(user["id"], 1)
        oid2 = Order.create_order(user["id"], 2)
        self.assertTrue(Order.check_order(oid1))
        self.assertTrue(Order.check_order(oid2))
        Interactive.wipe()

    def test_check_order_no_order(self):
        Interactive.wipe()
        self.assertFalse(Order.check_order(1))
        Interactive.wipe()

    def test_add_order_product_pass(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        oid = Order.create_order(user["id"], 1.2)
        Order.add_order_product(
            oid, products[0]["id"], products[0]["price"], 1)
        order_products = Order.get_order_products(oid)
        self.assertEqual(order_products[0]["quantity"], 1)
        Interactive.wipe()

    def test_add_order_product_noisy1(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_double()
        oid = Order.create_order(user["id"], 1.2)
        Order.add_order_product(
            oid, products[0]["id"], products[0]["price"], 1)
        order_products = Order.get_order_products(oid)
        self.assertEqual(order_products[0]["quantity"], 1)
        Interactive.wipe()

    def test_add_order_product_noisy2(self):
        Interactive.wipe()
        users = self.setup_user_double()
        products = self.setup_product_single()
        oid = Order.create_order(users[0]["id"], 1.2)
        Order.add_order_product(
            oid, products[0]["id"], products[0]["price"], 1)
        order_products1 = Order.get_order_products(oid)
        self.assertEqual(order_products1[0]["quantity"], 1)
        self.assertIsNone(Order.get_order_products(oid + 1))

    def test_add_order_product_no_user(self):
        Interactive.wipe()
        self.assertIsNone(Order.add_order_product(1, 1, 1, 1))
        Interactive.wipe()

    def test_add_order_product_no_order(self):
        Interactive.wipe()
        self.setup_user_single()
        products = self.setup_product_single()
        self.assertIsNone(Order.add_order_product(
            1, products[0]["id"], products[0]["price"], 1))
        Interactive.wipe()

    def test_add_order_product_no_product(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 1.2)
        Order.add_order_product(oid, 1, 1.2, 1)
        self.assertEqual(Order.get_order_products(oid), [])
        Interactive.wipe()

    def test_add_order_product_no_quantity(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        oid = Order.create_order(user["id"], 1.2)
        Order.add_order_product(
            oid, products[0]["id"], products[0]["price"], 0)
        self.assertEqual(Order.get_order_products(oid), [])
        Interactive.wipe()
    
    def test_add_order_product_negative_quantity(self):
        Interactive.wipe()
        user = self.setup_user_single()
        products = self.setup_product_single()
        oid = Order.create_order(user["id"], 1.2)
        Order.add_order_product(
            oid, products[0]["id"], products[0]["price"], -1)
        self.assertEqual(Order.get_order_products(oid), [])
        Interactive.wipe()

    def test_cancel_orders_empty(self):
        Interactive.wipe()
        self.assertTrue(Order.cancel_orders([]))
        Interactive.wipe()

    def test_cancel_orders_single(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid = Order.create_order(user["id"], 1)
        Order.cancel_orders([oid])
        orders = Order.get_orders(user["id"])
        statuses = [order["status"] for order in orders]
        self.assertEqual(statuses.count("cancel"), 1)
        Interactive.wipe()

    def test_cancel_orders_double(self):
        Interactive.wipe()
        user = self.setup_user_single()
        oid1 = Order.create_order(user["id"], 1)
        oid2 = Order.create_order(user["id"], 2)
        Order.cancel_orders([oid1, oid2])
        orders = Order.get_orders(user["id"])
        statuses = [order["status"] for order in orders]
        self.assertEqual(statuses.count("cancel"), 2)
        Interactive.wipe()

    def test_cancel_orders_noisy(self):
        Interactive.wipe()
        users = self.setup_user_double()
        oid1 = Order.create_order(users[0]["id"], 1)
        Order.create_order(users[1]["id"], 2)
        Order.cancel_orders([oid1])
        orders1 = Order.get_orders(users[0]["id"])
        orders2 = Order.get_orders(users[1]["id"])
        status1 = [order["status"] for order in orders1]
        status2 = [order["status"] for order in orders2]
        self.assertEqual(status1, ["cancel"])
        self.assertEqual(status2, ["package"])
        Interactive.wipe()

    def test_cancel_orders_no_order(self):
        Interactive.wipe()
        self.assertTrue(Order.cancel_orders([1]))
        Interactive.wipe()
