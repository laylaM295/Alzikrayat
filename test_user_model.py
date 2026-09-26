from app.models.user import UserModel


userModel = UserModel()

result = userModel.findUserByEmail("test@example.com")

print(result)