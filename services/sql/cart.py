import json
from services.sql.sql import Sql
from services.sql.product import Product
from services.sql.account import Account

class Cart(Sql):
    def add_to_cart(uid: int, pid: int, quantity: int):
        """
        Adds a product to the user's cart.

        Add method: If the product is not in the cart, it will be added as a new product.
        If the product is already in the cart, assume the user misunderstood the function name and wants to add to the quantity of the product.

        Args:
            uid (int): The user's id.
            pid (int): The product's id.
            quantity (int): The quantity of the product to add.

        Returns:
            True if the product was successfully added, None otherwise.
        """
        if Cart.check_cart(uid) and Product.check_product(pid) and quantity > 0:
            if Cart.check_cart_product(uid, pid):
                product = Cart.call_stored_procedure("ReadCartProductsByIds", (uid, json.dumps([pid])), fetch=1)
                quantity += product["quantity"]
                return Cart.update_cart_product(uid, pid, quantity)
            return Cart.call_stored_procedure("CreateCartProduct", (uid, pid, quantity))

    def get_cart(uid: int):
        """
        Gets the summary of the overall cart.

        Args:
            uid (int): The user's id.

        Returns:
            dict: The summary of the user's cart if it exists, None otherwise.
        """
        if Cart.check_cart(uid):
            return Cart.call_stored_procedure("ReadCart", (uid,), fetch=1)

    def get_cart_products(uid: int):
        """
        Gets the products in the user's cart.

        Args:
            uid (int): The user's id.

        Returns:
            list: A list of dictionaries representing the products in the cart.
        """
        if Cart.check_cart(uid):
            return Cart.call_stored_procedure("ReadCartProducts", (uid,), fetch=2)

    def get_cart_total(uid: int):
        """
        Gets the total cost of the user's cart.

        Args:
            uid (int): The user's id.

        Returns:
            float: The total cost of the user's cart.
        """
        if Cart.check_cart(uid):
            return Cart.call_stored_procedure("ReadCartTotalPrice", (uid,), fetch=1)["total_price"]
    
    def check_cart(uid: int):
        """
        Checks if a user has a cart.

        Args:
            uid (int): The user's id.

        Returns:
            bool: True if the user has a cart, False otherwise.
        """
        if Account.check_user(uid):
            return Cart.call_stored_procedure("CheckCart", (uid,), fetch=1)["e"]

    def check_cart_product(uid: int, pid: int):
        """
        Checks if a product is in the user's cart.

        Args:
            uid (int): The user's id.
            pid (int): The product's id.

        Returns:
            bool: True if the product is in the cart, False otherwise.
        """
        if Cart.check_cart(uid):
            return Cart.call_stored_procedure("CheckCartProduct", (uid, pid), fetch=1)["e"]

    def update_cart_product(uid: int, pid: int, quantity: int):
        """
        Update a product in the user's cart.

        Update method: If the quantity > 0, the product's quantity will be set to the new quantity.
        If the quantity == 0, assume the user misunderstood the function name and wants to remove the product from the cart.

        Args:
            uid (int): The user's id.
            pid (int): The product's id.
            quantity (int): The new quantity of the product.

        Returns:
            True if the cart was successfully updated, None otherwise.
        """
        if Cart.check_cart(uid):
            if Cart.check_cart_product(uid, pid):
                if quantity == 0:
                    return Cart.remove_from_cart(uid, [pid])
                else:
                    return Cart.call_stored_procedure("UpdateCartProduct", (uid, pid, quantity))
            else:
                return Cart.add_to_cart(uid, pid, quantity)

    def update_cart(uid: int, products: list):
        """
        Updates the user's cart. Can be used everywhere.

        Args:
            uid (int): The user's id.
            products (list): The products in the cart.

        Returns:
            True if the cart was successfully updated, None otherwise.
        """
        if Cart.check_cart(uid):
            for pid, quantity in products:
                if Product.check_product(pid):
                    if Cart.check_cart_product(uid, pid):
                        Cart.update_cart_product(uid, pid, quantity)
                    else:
                        Cart.add_to_cart(uid, pid, quantity)
                else:
                    return None

    def remove_from_cart(uid: int, pids: list):
        """
        Removes products from the user's cart.

        Args:
            uid (int): The user's id.
            pids (list): The product ids to remove from the cart.

        Returns:
            True if the products were successfully removed, None otherwise.
        """
        if Cart.check_cart(uid):
            return Cart.call_stored_procedure("DeleteCartProducts", (uid, json.dumps(pids)))
    
    def empty_cart(uid: int):
        """
        Empties the user's cart.

        Args:
            uid (int): The user's id.

        Returns:
            True if the cart was successfully emptied, None otherwise.
        """
        if Cart.check_cart(uid):
            return Cart.call_stored_procedure("DeleteAllCartProducts", (uid,))