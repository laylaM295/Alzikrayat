from app.controllers.photo_controller import PhotoController


photoController = PhotoController()

result = photoController.index()

print("Photos page:", result)