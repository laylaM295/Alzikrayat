from app.core.database import getConnection


class CommentModel:

    """
    Handles database operations related to photo comments.
    """

    def createComment(self, userId, photoId, comment):
        """
        Creates a new comment for a photo.
        """

        connection = getConnection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Comments
            (user_id, photo_id, comment)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (userId, photoId, comment)
        )

        connection.commit()

        commentId = cursor.lastrowid

        cursor.close()
        connection.close()

        return commentId

    def getCommentsByPhotoId(self, photoId):
        """
        Retrieves all comments for a specific photo.
        """

        connection = getConnection()
        cursor = connection.cursor()

        query = """
            SELECT
                Comments.id,
                Comments.comment,
                Comments.date_time,
                Users.first_name,
                Users.last_name
            FROM Comments
            INNER JOIN Users
                ON Comments.user_id = Users.id
            WHERE Comments.photo_id = %s
            ORDER BY Comments.date_time ASC
        """

        cursor.execute(
            query,
            (photoId,)
        )

        comments = cursor.fetchall()

        cursor.close()
        connection.close()

        return comments