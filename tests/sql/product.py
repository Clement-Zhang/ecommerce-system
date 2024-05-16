from tests.sql.sql import TestSql
from services.sql.product import Product
from services.sql.interactive import Interactive
import sys
import os
sys.path.append(os.getcwd())


class TestProduct(TestSql):
    def test_add_product_pass(self):
        Interactive.wipe()
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 5)
        products = Product.get_products()
        self.assertEqual(products[0]["quantity"], 5)
        Interactive.wipe()
    
    def test_add_product_zero(self):
        Interactive.wipe()
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 0)
        products = Product.get_products()
        self.assertEqual(products, [])
        Interactive.wipe()
    
    def test_add_product_negative(self):
        Interactive.wipe()
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", -1)
        products = Product.get_products()
        self.assertEqual(products, [])
        Interactive.wipe()

    def test_add_product_duplicate(self):
        Interactive.wipe()
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 5)
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 5)
        products = Product.get_products()
        quantities = [product["quantity"] for product in products]
        self.assertEqual(quantities, [5, 5])
        Interactive.wipe()

    def test_get_products_empty(self):
        Interactive.wipe()
        self.assertEqual(Product.get_products(), [])
        Interactive.wipe()

    def test_get_products_single(self):
        Interactive.wipe()
        self.setup_product_single()
        self.assertEqual(Product.get_products()[0]["quantity"], 5)
        Interactive.wipe()

    def test_get_products_double(self):
        Interactive.wipe()
        self.setup_product_double()
        products = Product.get_products()
        quantities = [product["quantity"] for product in products]
        self.assertEqual(quantities, [5, 5])
        Interactive.wipe()

    def test_get_products_by_ids_empty(self):
        Interactive.wipe()
        self.assertEqual(Product.get_products_by_ids([]), [])
        Interactive.wipe()

    def test_get_product_by_ids_single(self):
        Interactive.wipe()
        products = self.setup_product_single()
        products = Product.get_products_by_ids(products[0]["id"])
        self.assertEqual(products[0]["quantity"], 5)
        Interactive.wipe()
    
    def test_get_products_by_ids_double(self):
        Interactive.wipe()
        products = self.setup_product_double()
        products = Product.get_products_by_ids([products[0]["id"], products[1]["id"]])
        quantities = [product["quantity"] for product in products]
        self.assertEqual(quantities, [5, 5])
        Interactive.wipe()
    
    def test_get_products_by_ids_all(self):
        Interactive.wipe()
        products = self.setup_product_multiple()
        products = Product.get_products_by_ids([products[0]["id"], products[1]["id"], products[2]["id"]])
        quantities = [product["quantity"] for product in products]
        self.assertEqual(quantities, [5, 5, 5])
        Interactive.wipe()

    def test_get_products_by_ids_noisy(self):
        Interactive.wipe()
        products = self.setup_product_double()
        noisy_products1 = Product.get_products_by_ids([products[0]["id"]])
        noisy_products2 = Product.get_products_by_ids([products[1]["id"]])
        self.assertEqual(noisy_products1[0]["quantity"], 5)
        self.assertEqual(noisy_products2[0]["quantity"], 5)
        Interactive.wipe()

    def test_get_products_by_ids_no_product(self):
        Interactive.wipe()
        self.assertEqual(Product.get_products_by_ids(1), [])
        Interactive.wipe()

    def test_check_product_pass(self):
        Interactive.wipe()
        products = self.setup_product_single()
        self.assertTrue(Product.check_product(products[0]["id"]))
        Interactive.wipe()
    
    def test_check_product_noisy(self):
        Interactive.wipe()
        products = self.setup_product_double()
        self.assertTrue(Product.check_product(products[0]["id"]))
        self.assertTrue(Product.check_product(products[1]["id"]))
        Interactive.wipe()
    
    def test_check_product_fail(self):
        Interactive.wipe()
        self.assertFalse(Product.check_product(1))
        Interactive.wipe()
    
    def restock_product_zero(self):
        Interactive.wipe()
        products = self.setup_product_single()
        self.assertIsNone(Product.restock_product(products[0]["id"], 0))
        self.assertEqual(Product.get_products()[0]["quantity"], 5)
        Interactive.wipe()
    
    def restock_product_positive(self):
        Interactive.wipe()
        products = self.setup_product_single()
        Product.restock_product(products[0]["id"], 1)
        self.assertEqual(Product.get_products()[0]["quantity"], 6)
        Interactive.wipe()
    
    def restock_product_noisy(self):
        Interactive.wipe()
        products = self.setup_product_double()
        Product.restock_product(products[0]["id"], 1)
        Product.restock_product(products[1]["id"], 2)
        self.assertEqual(Product.get_products()[0]["quantity"], 6)
        self.assertEqual(Product.get_products()[1]["quantity"], 7)
        Interactive.wipe()
    
    def restock_product_no_product(self):
        Interactive.wipe()
        self.assertIsNone(Product.restock_product(1, 1))
        self.assertEqual(Product.get_products(), [])
        Interactive.wipe()
    
    def test_restock_product_negative(self):
        Interactive.wipe()
        products = self.setup_product_single()
        self.assertIsNone(Product.restock_product(products[0]["id"], -1))
        self.assertEqual(Product.get_products()[0]["quantity"], 5)
        Interactive.wipe()