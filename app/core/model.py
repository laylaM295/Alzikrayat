from app.core.database import getConnection


class BaseModel:
    """
    Base model that provides common database operations for application models.

    Args:
        None

    Returns:
        BaseModel: A reusable base model instance.
    """

    def executeQuery(self, query, parameters=None, fetchOne=False, fetchAll=False):
        """
        Execute a parameterized SQL query and optionally return its results.

        Args:
            query (str): SQL query written manually.
            parameters (tuple): Values used by the SQL query.
            fetchOne (bool): Return one database row if True.
            fetchAll (bool): Return all database rows if True.

        Returns:
            dict, list, or None: Query results when requested.

        Raises:
            Exception: If the SQL query fails.
        """
        connection = getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, parameters or ())

                if fetchOne:
                    result = cursor.fetchone()
                elif fetchAll:
                    result = cursor.fetchall()
                else:
                    result = None

                connection.commit()
                return result

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()