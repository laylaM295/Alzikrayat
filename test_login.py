from app.controllers.auth_controller import AuthController


result = AuthController.login(
    email="layla.test@example.com",
    password="TestPassword123"
)

print(result["message"])
print(result["user"]["first_name"])
print(result["user"]["email"])