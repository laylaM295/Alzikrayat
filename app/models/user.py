from app.core.model import BaseModel


class UserModel(BaseModel):
    """
    Model responsible for database operations related to users.

    Returns:
        UserModel: A model for user database operations.
    """

    def createUser(
        self,
        firstName,
        lastName,
        email,
        password,
        location=None,
        description=None,
        occupation=None
    ):
        """
        Create a new user in the Users table.

        Args:
            firstName (str): User's first name.
            lastName (str): User's last name.
            email (str): User's email address.
            password (str): Securely hashed password.
            location (str): User's optional location.
            description (str): User's optional description.
            occupation (str): User's optional occupation.

        Returns:
            None: The user is inserted into the database.

        Raises:
            Exception: If the database operation fails.
        """

        query = """
            INSERT INTO Users
            (
                first_name,
                last_name,
                email,
                password,
                location,
                description,
                occupation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        parameters = (
            firstName,
            lastName,
            email,
            password,
            location,
            description,
            occupation
        )

        self.executeQuery(query, parameters)

    def findUserByEmail(self, email):
        """
        Find a user by email address.

        Args:
            email (str): Email address to search for.

        Returns:
            dict or None: User data if found, otherwise None.
        """

        query = """
            SELECT *
            FROM Users
            WHERE email = %s
        """

        return self.executeQuery(
            query,
            (email,),
            fetchOne=True
        )

    def getUserCount(self):
        """
        Count the total number of registered users.

        Returns:
            int: Number of registered users.
        """

        query = """
            SELECT COUNT(*) AS totalUsers
            FROM Users
        """

        result = self.executeQuery(
            query,
            fetchOne=True
        )

        return result["totalUsers"]
