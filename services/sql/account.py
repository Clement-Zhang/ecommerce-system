from services.sql.sql import Sql

class Account(Sql):
    def add_customer(username: str, password: str, fname: str, lname: str, email: str, phone: str):
        """
        Creates a new customer.

        Args:
            username (str): The username of the new customer.
            password (str): The password of the new customer.
            fname (str): The first name of the new customer.
            lname (str): The last name of the new customer.
            email (str): The email of the new customer.
            phone (str): The phone number of the new customer.

        Returns:
            True if the customer was successfully created, None otherwise.
        """
        return Account.call_stored_procedure("CreateCustomer", (username, password, fname, lname, email, phone))

    def add_admin(username: str, password: str, fname: str, lname: str, email: str, phone: str):
        """
        Creates a new admin.

        Args:
            username (str): The username of the new admin.
            password (str): The password of the new admin.
            fname (str): The first name of the new admin.
            lname (str): The last name of the new admin.
            email (str): The email of the new admin.
            phone (str): The phone number of the new admin.

        Returns:
            True if the admin was successfully created, None otherwise.
        """
        return Account.call_stored_procedure("CreateAdmin", (username, password, fname, lname, email, phone))

    def get_user_by_id(uid: int):
        """
        Gets a user's account.

        Args:
            uid (int): The id of the user.

        Returns:
            dict: The user's information if it exists, None otherwise.
        """
        return Account.call_stored_procedure("ReadAccountById", (uid,), fetch=1)

    def get_user_by_username_email(username: str, email: str):
        """
        Alternate method to get a user's account, use for resetting password.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.

        Returns:
            dict: The user's information if it exists, None otherwise.
        """
        return Account.call_stored_procedure("ReadAccountByUsernameEmail", (username, email), fetch=1)

    def get_user_by_username_password(username: str, password: str):
        """
        Gets a user's account information.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict: The user's information if it exists, None otherwise.
        """
        return Account.call_stored_procedure("ReadAccountByUsernamePassword", (username, password), fetch=1)

    def validate_user(username: str, password: str):
        """
        Validates a user's credentials.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            True if the user exists, False otherwise.
        """
        return Account.call_stored_procedure("ValidateAccount", (username, password), fetch=1)["e"]

    def existing_user(username: str, email: str):
        """
        Relaxed version of validate_user, use for resetting password.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return Account.call_stored_procedure("CheckAccountByUsernameEmail", (username, email), fetch=1)["e"]
    
    def check_user(uid: int):
        """
        Checks if a user exists.

        Args:
            uid (int): The user's id.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return Account.call_stored_procedure("CheckAccountById", (uid, ), fetch=1)["e"]

    def change_password(uid: int, password: str):
        """
        Changes a user's password.

        Args:
            uid (int): The user's id.
            password (str): The new password.

        Returns:
            True if the password was successfully changed, None otherwise.
        """
        if Account.check_user(uid):
            return Account.call_stored_procedure("UpdatePassword", (uid, password))

    def update_fname(uid: int, fname: str):
        """
        Updates a user's first name.

        Args:
            uid (int): The user's id.
            fname (str): The user's first name.

        Returns:
            True if the first name was successfully updated, None otherwise.
        """
        if Account.check_user(uid):
            return Account.call_stored_procedure("UpdateFname", (uid, fname))

    def update_lname(uid: int, lname: str):
        """
        Updates a user's last name.

        Args:
            uid (int): The user's id.
            lname (str): The user's last name.

        Returns:
            True if the last name was successfully updated, None otherwise.
        """
        if Account.check_user(uid):
            return Account.call_stored_procedure("UpdateLname", (uid, lname))

    def update_email(uid: int, email: str):
        """
        Updates a user's email.

        Args:
            uid (int): The user's id.
            email (str): The user's email.

        Returns:
            True if the email was successfully updated, None otherwise.
        """
        if Account.check_user(uid):
            return Account.call_stored_procedure("UpdateEmail", (uid, email))

    def update_phone(uid: int, phone: str):
        """
        Updates a user's phone number.

        Args:
            uid (int): The user's id.
            phone (str): The user's phone number.

        Returns:
            True if the phone number was successfully updated, None otherwise.
        """
        if Account.check_user(uid):
            return Account.call_stored_procedure("UpdatePhone", (uid, phone))