import json
from services.sql.sql import Sql

class Product(Sql):
    def add_product(name: str, price: float, description: str, image: str, quantity: int):
        """
        Adds a product to the database.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            description (str): The description of the product.
            image (str): The image of the product.
            quantity (int): The quantity of the product.

        Returns:
            True if the product was successfully added, None otherwise.
        """
        if quantity > 0:
            return Product.call_stored_procedure("CreateProduct", (name, price, description, image, quantity))

    def get_products():
        """
        Get all products.

        Returns:
            list: A list of dictionaries representing the products.
        """
        return Product.call_stored_procedure("ReadProducts", fetch=2)

    def get_products_by_ids(pids: list):
        """
        Get products by their ids.

        Args:
            pids (list): The product ids to get.

        Returns:
            list: A list of dictionaries representing the products.
        """
        return Product.call_stored_procedure("ReadProductsByIds", (json.dumps(pids),), fetch=2)
    
    def check_product(pid: int):
        """
        Checks if a product exists.

        Args:
            pid (int): The product's id.

        Returns:
            bool: True if the product exists, False otherwise.
        """
        return Product.call_stored_procedure("CheckProduct", (pid,), fetch=1)["e"]
    
    def restock_product(pid: int, quantity: int):
        """
        Restocks a product.

        Args:
            pid (int): The product's id.
            quantity (int): The quantity to restock.

        Returns:
            True if the product was successfully restocked, None otherwise.
        """
        if Product.check_product(pid) and quantity > 0:
            return Product.call_stored_procedure("RestockProduct", (pid, quantity))