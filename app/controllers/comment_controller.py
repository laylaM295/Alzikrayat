from app.models.comment import CommentModel


class CommentController:

    """
    Handles application logic related to photo comments.
    """

    def __init__(self):
        """
        Initializes the comment controller.
        """

        self.commentModel = CommentModel()

    def getComments(self, photoId):
        """
        Retrieves all comments for a specific photo.
        """

        return self.commentModel.getCommentsByPhotoId(
            photoId
        )

    def addComment(self, userId, photoId, commentText):
        """
        Validates and creates a new comment for a photo.
        """

        if not commentText or not commentText.strip():
            raise ValueError(
                "Comment cannot be empty."
            )

        commentText = commentText.strip()

        if len(commentText) > 1000:
            raise ValueError(
                "Comment must not exceed 1000 characters."
            )

        commentId = self.commentModel.createComment(
            userId,
            photoId,
            commentText
        )

        return {
            "id": commentId,
            "user_id": userId,
            "photo_id": photoId,
            "comment": commentText
        }