from app.models.user import UserModel

userModel = UserModel()

count = userModel.getUserCount()

print("Total users:", count)