import unittest
import sys
import os
sys.path.append(os.getcwd())
from services.sql.account import Account
from services.sql.product import Product
from services.crypto import Crypto

class TestSql(unittest.TestCase):

    def setup_user_single(self):
        Account.add_customer("blah", Crypto.hash_password("123"), "John", "Smith", "js@yahoo.ca", "1234567890")
        return Account.get_user_by_username_email("blah", "js@yahoo.ca")

    def setup_user_double(self):
        Account.add_customer("blah", Crypto.hash_password("123"), "John", "Smith", "js@yahoo.ca", "1234567890")
        Account.add_customer("bl", Crypto.hash_password("123"), "Jane", "Doe", "jd@yahoo.ca", "0987654321")
        return [Account.get_user_by_username_email("blah", "js@yahoo.ca"), Account.get_user_by_username_email("bl", "jd@yahoo.ca")]
    
    def setup_product_single(self):
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 5)
        return Product.get_products()
    
    def setup_product_double(self):
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 5)
        Product.add_product("p2", 1.2, "p2desc", "error.jpg", 5)
        return Product.get_products()
    
    def setup_product_multiple(self):
        Product.add_product("p1", 1.2, "p1desc", "error.jpg", 5)
        Product.add_product("p2", 1.2, "p2desc", "error.jpg", 5)
        Product.add_product("p3", 1.2, "p3desc", "error.jpg", 5)
        return Product.get_products()