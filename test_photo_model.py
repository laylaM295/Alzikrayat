from app.models.photo import PhotoModel


photoModel = PhotoModel()

photoModel.createPhoto(
    3,
    "test-image.jpg",
    "Test Photo",
    "Test photo description"
)

print("Photo created successfully")

photos = photoModel.getAllPhotos()

print("All photos:", photos)