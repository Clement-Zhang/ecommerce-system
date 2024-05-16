import mysql.connector
from itertools import chain


class Sql:
    _instance = None
    HOST = "localhost"
    USER = "root"
    PASSWORD = ""
    DATABASE = "karel"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sql, cls).__new__(cls)
        return cls._instance

    def create_connection():
        """
        Establish a connection to the SQL database using predefined configuration.

        Returns:
            mysql.connector.connection.MySQLConnection: An instance of the connection object to the database.
        """
        return mysql.connector.connect(host=Sql.HOST, user=Sql.USER, password=Sql.PASSWORD, database=Sql.DATABASE)

    def call_stored_procedure(proc_name: str, params: tuple = (), fetch: int = 0):
        """
        Calls a stored procedure in the SQL database with the provided parameters.

        Args:
            proc_name (str): The name of the stored procedure to call.
            params (tuple, optional): The parameters to pass to the stored procedure.
            fetch (int, optional): The fetch mode to use. Intended usage: 0 for no fetch, 1 for fetchone, 2 for fetchall. Tolerant of typos such as >2 and <0.

        Returns:
            list, dict, bool, or None: Depending on the flags set and the procedure called, it may return:
                                    - A list of dictionaries representing the fetched rows if fetch==2.
                                    - A single dictionary if fetch==1.
                                    - True fetch==0 and the procedure executed successfully.
                                    - None if there is an error.
        """
        connection = Sql.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.callproc(proc_name, args=params)
            connection.commit()
            if fetch == 1:
                for result in cursor.stored_results():
                    return result.fetchone()
            elif fetch >= 2:
                return [result for result in chain(*cursor.stored_results())]
            else:
                return True
        except mysql.connector.Error as err:
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()