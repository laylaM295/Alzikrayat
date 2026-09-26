import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def getConnection():
    """
    Create and return a connection to the MySQL database.

    Returns:
        pymysql.Connection: Active MySQL database connection.

    Raises:
        pymysql.MySQLError: If the database connection fails.
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )