from app.controllers.auth_controller import AuthController


result = AuthController.register(
    firstName="Layla",
    lastName="Test",
    email="layla.test@example.com",
    password="TestPassword123",
    location="Khartoum",
    description="Test account",
    occupation="Student"
)

print(result)