
from app.core.router import Router

from app.controllers.photo_controller import PhotoController
from app.controllers.auth_controller import AuthController
from app.controllers.comment_controller import CommentController


router = Router()

photoController = PhotoController()
authController = AuthController()
commentController = CommentController()


router.add(
    "GET",
    "/photos",
    (photoController, "index")
)

router.add(
    "GET",
    "/photo/{id}",
    (photoController, "show")
)

router.add(
    "GET",
    "/photo/{id}/comments",
    (commentController, "getComments")
)