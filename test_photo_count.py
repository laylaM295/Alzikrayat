from app.models.photo import PhotoModel

photoModel = PhotoModel()

count = photoModel.getPhotoCount()

print("Total photos:", count)