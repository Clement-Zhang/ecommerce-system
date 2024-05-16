import unittest
import sys
import os
sys.path.append(os.getcwd())
from tests.sql.account import TestAccount
from tests.sql.cart import TestCart
from tests.sql.order import TestOrder
from tests.sql.product import TestProduct
from tests.ui.account import TestAppAccount
from tests.ui.display import TestAppDisplay
from tests.ui.session import TestAppSession
from tests.ui.transaction import TestAppTransaction

if __name__ == "__main__":
    sql_tests = [TestAccount, TestCart, TestOrder, TestProduct]
    ui_tests = [TestAppAccount, TestAppDisplay, TestAppSession, TestAppTransaction]
    suites = [unittest.TestLoader().loadTestsFromTestCase(c) for c in sql_tests + ui_tests]
    all_tests = unittest.TestSuite(suites)
    unittest.TextTestRunner().run(all_tests)