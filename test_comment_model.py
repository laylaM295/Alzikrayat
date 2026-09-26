from app.models.comment import CommentModel


commentModel = CommentModel()

commentId = commentModel.createComment(
    3,
    6,
    "This is a test comment."
)

print("Created comment ID:", commentId)

comments = commentModel.getCommentsByPhotoId(6)

print("Comments:")

for comment in comments:
    print(comment)