from services.sql.sql import Sql
from services.sql.cart import Cart
from services.sql.order import Order

class Interactive(Sql):
    def checkout(uid: int):
        """
        Converts the user's cart into an order.

        Args:
            uid (int): The user's id.

        Returns:
            True if the checkout was successful, None otherwise.
        """
        if Cart.check_cart(uid):
            # cart = Sql.get_cart(uid)
            total = Cart.get_cart_total(uid)
            oid = Order.create_order(uid, total)
            products = Cart.get_cart_products(uid)
            if oid:
                for product in products:
                    Order.add_order_product(oid, product["id"], product["price"], product["quantity"])
                Cart.empty_cart(uid)
                return True
    
    def wipe():
        """
        Deletes everything.

        Returns:
            bool: True if the database was successfully wiped, False otherwise.
        """
        return Sql.call_stored_procedure("Wipe")