import json
from services.sql.sql import Sql
from services.sql.account import Account
from services.sql.product import Product

class Order(Sql):
    def create_order(uid: int, total: float):
        """
        Creates an order for a user.

        Args:
            uid (int): The user's id.
            total (float): The total cost of the order.

        Returns:
            The order id if the order was successfully created, None otherwise.
        """
        if Account.check_user(uid):
            return Order.call_stored_procedure("CreateOrder", (uid, total), fetch=1)["id"]

    def get_order(oid: int):
        """
        Gets the overall summary of an order by its id.

        Args:
            oid (int): The order's id.

        Returns:
            dict: A dictionary representing the order if it exists, None otherwise.
        """
        if Order.check_order(oid):
            return Order.call_stored_procedure("ReadOrder", (oid,), fetch=1)

    def get_order_products(oid: int):
        """
        Gets the products in an order.

        Args:
            oid (int): The order's id.

        Returns:
            list: A list of dictionaries representing the products in the order.
        """
        if Order.check_order(oid):
            return Order.call_stored_procedure("ReadOrderProducts", (oid,), fetch=2)
    
    def get_order_total(oid: int):
        """
        Gets the total cost of an order.

        Args:
            oid (int): The order's id.

        Returns:
            float: The total cost of the order.
        """
        if Order.check_order(oid):
            return Order.call_stored_procedure("ReadOrderTotalPrice", (oid,), fetch=1)["total_price"]

    def get_orders(uid: int):
        """
        Gets all the orders for a user.

        Args:
            uid (int): The user's id.

        Returns:
            list: A list of dictionaries representing the orders.
        """
        if Account.check_user(uid):
            return Order.call_stored_procedure("ReadOrders", (uid,), fetch=2)
    
    def check_order(oid: int):
        """
        Checks if an order exists.

        Args:
            oid (int): The order's id.

        Returns:
            bool: True if the order exists, False otherwise.
        """
        return Order.call_stored_procedure("CheckOrder", (oid,), fetch=1)["e"]
    
    def add_order_product(oid: int, pid: int, price: float, quantity: int):
        """
        Adds a product to an order.

        Args:
            oid (int): The order's id.
            pid (int): The product's id.
            price (float): The price of the product at time of the order creation.
            quantity (int): The quantity of the product.

        Returns:
            True if the product was successfully added, None otherwise.
        """
        if Order.check_order(oid) and Product.check_product(pid) and quantity > 0:
            return Order.call_stored_procedure("CreateOrderProduct", (oid, pid, price, quantity))

    def cancel_orders(oids: list):
        """
        Cancels orders.

        Args:
            oids (list): The order ids to cancel.

        Returns:
            True if the orders were successfully cancelled, None otherwise.
        """
        return Order.call_stored_procedure("CancelOrders", (json.dumps(oids),))