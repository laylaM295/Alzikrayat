from app.core.controller import BaseController
from app.models.photo import PhotoModel


class PhotoController(BaseController):
    """
    Controller responsible for handling photo-related requests.

    Returns:
        PhotoController: A controller for photo operations.
    """

    def __init__(self):
        """
        Initialize the photo controller.

        Returns:
            None
        """
        self.photoModel = PhotoModel()

    def show(self, photoId):
        """
        Display a specific photo using its ID.

        Args:
            photoId (str): ID of the photo.

        Returns:
            dict: Photo details view data or not-found message.
        """

        photo = self.photoModel.getPhotoById(photoId)

        if not photo:
            return {
                "message": "Photo not found"
            }

        return self.render(
            "photo_details",
            {
                "photo": photo
            }
        )

    def index(self):
        """
        Display all photos.

        Returns:
            dict: All photos information.
        """

        photos = self.photoModel.getAllPhotos()

        return self.render(
            "photos",
            {
                "photos": photos
            }
        )

    def delete(self, photoId, userId):
        """
        Delete a photo only if it belongs to the current user.

        Args:
            photoId (str): ID of the photo.
            userId (int): ID of the currently logged-in user.

        Returns:
            dict: Deletion result.
        """

        photo = self.photoModel.getPhotoById(photoId)

        if not photo:
            return {
                "message": "Photo not found"
            }

        if photo["user_id"] != userId:
            return {
                "message": "You are not allowed to delete this photo"
            }

        self.photoModel.deletePhoto(photoId)

        return {
            "message": "Photo deleted successfully"
        }