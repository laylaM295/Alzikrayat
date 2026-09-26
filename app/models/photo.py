from app.core.model import BaseModel


class PhotoModel(BaseModel):
    """
    Model responsible for database operations related to photos.

    Returns:
        PhotoModel: A model for photo database operations.
    """

    def createPhoto(
        self,
        userId,
        fileName,
        title,
        description=None
    ):
        """
        Create a new photo in the Photos table.

        Args:
            userId (int): ID of the user who uploaded the photo.
            fileName (str): Name of the uploaded photo file.
            title (str): Title of the photo.
            description (str): Optional photo description.

        Returns:
            None: The photo is inserted into the database.
        """

        query = """
            INSERT INTO Photos
            (
                user_id,
                file_name,
                title,
                description
            )
            VALUES (%s, %s, %s, %s)
        """

        parameters = (
            userId,
            fileName,
            title,
            description
        )

        self.executeQuery(query, parameters)

    def getPhotoById(self, photoId):
        """
        Find a photo by its ID.

        Args:
            photoId (int): ID of the photo.

        Returns:
            dict or None: Photo data if found, otherwise None.
        """

        query = """
            SELECT *
            FROM Photos
            WHERE id = %s
        """

        return self.executeQuery(
            query,
            (photoId,),
            fetchOne=True
        )

    def getAllPhotos(self):
        """
        Retrieve all photos from the database.

        Returns:
            list: A list of all photos.
        """

        query = """
            SELECT *
            FROM Photos
            ORDER BY date_time DESC
        """

        return self.executeQuery(
            query,
            fetchAll=True
        )

    def deletePhoto(self, photoId):
        """
        Delete a photo by its ID.

        Args:
            photoId (int): ID of the photo to delete.

        Returns:
            None: The photo is deleted from the database.
        """

        query = """
            DELETE FROM Photos
            WHERE id = %s
        """

        self.executeQuery(
            query,
            (photoId,)
        )

    def getPhotoCount(self):
        """
        Count the total number of photos.

        Returns:
            int: Number of photos in the database.
        """

        query = """
            SELECT COUNT(*) AS totalPhotos
            FROM Photos
        """

        result = self.executeQuery(
            query,
            fetchOne=True
        )

        return result["totalPhotos"]
