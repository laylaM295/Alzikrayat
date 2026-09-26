
import re

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.models.user import UserModel


class AuthController:

    """
    Controller responsible for authentication operations,
    including user registration and login.
    """

    @staticmethod
    def register(
        firstName,
        lastName,
        email,
        password,
        location=None,
        description=None,
        occupation=None
    ):
        """
        Register a new user after validating the input data.

        Raises:
            ValueError: If the input data is invalid.
        """

        if not isinstance(firstName, str):
            raise ValueError("Invalid first name")

        if not isinstance(lastName, str):
            raise ValueError("Invalid last name")

        if not isinstance(email, str):
            raise ValueError("Invalid email address")

        if not isinstance(password, str):
            raise ValueError("Invalid password")

        if location is not None and not isinstance(location, str):
            raise ValueError("Invalid location")

        if description is not None and not isinstance(description, str):
            raise ValueError("Invalid description")

        if occupation is not None and not isinstance(occupation, str):
            raise ValueError("Invalid occupation")

        firstName = firstName.strip()
        lastName = lastName.strip()
        email = email.strip().lower()
        password = password

        if location is not None:
            location = location.strip()

        if description is not None:
            description = description.strip()

        if occupation is not None:
            occupation = occupation.strip()

        if not firstName or not lastName or not email or not password:
            raise ValueError("Required fields are missing")

        if len(firstName) > 50:
            raise ValueError(
                "First name must not exceed 50 characters"
            )

        if len(lastName) > 50:
            raise ValueError(
                "Last name must not exceed 50 characters"
            )

        if not re.fullmatch(
            r"[A-Za-z]+",
            firstName
        ):
            raise ValueError(
                "First name must contain letters only"
            )

        if not re.fullmatch(
            r"[A-Za-z]+",
            lastName
        ):
            raise ValueError(
                "Last name must contain letters only"
            )

        if len(email) > 255:
            raise ValueError(
                "Email must not exceed 255 characters"
            )

        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email
        ):
            raise ValueError(
                "Invalid email address"
            )

        if len(password) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )

        if len(password) > 128:
            raise ValueError(
                "Password must not exceed 128 characters"
            )

        if location and len(location) > 255:
            raise ValueError(
                "Location must not exceed 255 characters"
            )

        if description and len(description) > 1000:
            raise ValueError(
                "Description must not exceed 1000 characters"
            )

        if occupation and len(occupation) > 255:
            raise ValueError(
                "Occupation must not exceed 255 characters"
            )

        userModel = UserModel()

        existingUser = userModel.findUserByEmail(
            email
        )

        if existingUser:
            raise ValueError(
                "Email already exists"
            )

        passwordHash = generate_password_hash(
            password,
            method="pbkdf2:sha256"
        )

        userModel.createUser(
            firstName,
            lastName,
            email,
            passwordHash,
            location,
            description,
            occupation
        )

        return {
            "message": "User registered successfully"
        }

    @staticmethod
    def login(email, password):
        """
        Authenticate a user using email and password.

        Raises:
            ValueError: If the email or password is incorrect.
        """

        if not isinstance(email, str):
            raise ValueError(
                "Invalid email or password"
            )

        if not isinstance(password, str):
            raise ValueError(
                "Invalid email or password"
            )

        email = email.strip().lower()

        if not email or not password:
            raise ValueError(
                "Invalid email or password"
            )

        userModel = UserModel()

        user = userModel.findUserByEmail(
            email
        )

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        passwordIsCorrect = check_password_hash(
            user["password"],
            password
        )

        if not passwordIsCorrect:
            raise ValueError(
                "Invalid email or password"
            )

        return {
            "message": "Login successful",
            "user": user
        }