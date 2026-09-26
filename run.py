
import os
import uuid
import secrets
import hmac
from datetime import datetime

from dotenv import load_dotenv

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    make_response,
    session,
    send_from_directory
)

from werkzeug.utils import secure_filename

from app.core.router import Router
from app.controllers.auth_controller import AuthController
from app.controllers.photo_controller import PhotoController
from app.controllers.comment_controller import CommentController
from app.models.user import UserModel
from app.models.photo import PhotoModel


load_dotenv()


app = Flask(
    __name__,
    template_folder="app/views",
    static_folder="public",
    static_url_path="/public"
)


app.secret_key = os.getenv("SECRET_KEY")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "public",
    "images",
    "uploads"
)


ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp"
}


def getCsrfToken():
    """
    Creates and returns a CSRF token stored in the session.
    """

    if "csrfToken" not in session:
        session["csrfToken"] = secrets.token_hex(32)

    return session["csrfToken"]


def validateCsrfToken():
    """
    Validates the CSRF token sent by the client.
    """

    requestToken = request.headers.get(
        "X-CSRF-Token"
    )

    sessionToken = session.get(
        "csrfToken"
    )

    if not requestToken or not sessionToken:
        return False

    return hmac.compare_digest(
        requestToken,
        sessionToken
    )


@app.context_processor
def injectCsrfToken():
    """
    Makes the CSRF token available to all templates.
    """

    return {
        "csrfToken": getCsrfToken()
    }


def allowedFile(filename):
    """
    Checks whether the uploaded file has an allowed extension.
    """

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


def isRealImage(file):
    """
    Detects the actual image type from the file header.
    """

    header = file.read(12)

    file.seek(0)

    if header.startswith(b"\xff\xd8\xff"):
        return "jpg"

    if header.startswith(
        b"\x89PNG\r\n\x1a\n"
    ):
        return "png"

    if (
        header.startswith(b"GIF87a")
        or header.startswith(b"GIF89a")
    ):
        return "gif"

    if (
        header.startswith(b"RIFF")
        and header[8:12] == b"WEBP"
    ):
        return "webp"

    return None


def extensionMatchesImage(
    filename,
    realImageType
):
    """
    Checks whether the file extension matches
    the actual image type.
    """

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    if realImageType == "jpg":
        return extension in {
            "jpg",
            "jpeg"
        }

    return extension == realImageType


@app.errorhandler(413)
def fileTooLarge(error):
    """
    Handles files that exceed the maximum upload size.
    """

    return jsonify({
        "error": "File size must not exceed 5 MB"
    }), 413


authController = AuthController()
photoController = PhotoController()
userModel = UserModel()
photoModel = PhotoModel()
commentController = CommentController()


def home():
    """
    Displays the home page.
    """

    totalUsers = userModel.getUserCount()

    totalPhotos = photoModel.getPhotoCount()

    return render_template(
        "home.html",
        totalUsers=totalUsers,
        totalPhotos=totalPhotos
    )


def photos():
    """
    Displays all uploaded photos.
    """

    photosList = photoModel.getAllPhotos()

    currentUserId = session.get(
        "userId"
    )

    return render_template(
        "photos.html",
        photos=photosList,
        currentUserId=currentUserId
    )


def photoDetails(id):
    """
    Displays photo details and its comments.
    """

    photo = photoModel.getPhotoById(
        id
    )

    if not photo:
        return "Photo not found", 404

    comments = commentController.getComments(
        id
    )

    return render_template(
        "photo_details.html",
        photo=photo,
        comments=comments
    )


def register():
    """
    Handles user registration.
    """

    if request.method == "GET":

        return render_template(
            "register.html"
        )

    if not validateCsrfToken():

        return jsonify({
            "error": "Invalid CSRF token."
        }), 403

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid request."
        }), 400

    try:

        user = authController.register(
            data.get("firstName"),
            data.get("lastName"),
            data.get("email"),
            data.get("password"),
            data.get("location"),
            data.get("description"),
            data.get("occupation")
        )

        return jsonify({
            "message": "Registration successful",
            "user": user
        }), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


def login():
    """
    Handles user login and creates a session.
    """

    if request.method == "GET":

        lastLogin = request.cookies.get(
            "lastLogin"
        )

        return render_template(
            "login.html",
            lastLogin=lastLogin
        )

    if not validateCsrfToken():

        return jsonify({
            "error": "Invalid CSRF token."
        }), 403

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid request."
        }), 400

    try:

        loginResult = authController.login(
            data.get("email"),
            data.get("password")
        )

        user = loginResult["user"]

        session["userId"] = user["id"]
        session["userEmail"] = user["email"]
        session["userName"] = user["first_name"]

        safeUser = {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "location": user["location"],
            "description": user["description"],
            "occupation": user["occupation"]
        }

        response = make_response(
            jsonify({
                "message": "Login successful",
                "user": safeUser
            })
        )

        response.set_cookie(
            "lastLogin",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            max_age=7 * 24 * 60 * 60,
            httponly=True,
            samesite="Lax"
        )

        return response

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


def logout():
    """
    Logs the user out and clears the session.
    """

    session.clear()

    response = make_response(
        redirect("/login")
    )

    response.delete_cookie(
        "lastLogin"
    )

    return response


def upload():
    """
    Handles photo upload.
    """

    if request.method == "GET":

        if "userId" not in session:

            return redirect("/login")

        return render_template(
            "upload.html"
        )

    if "userId" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    photo = request.files.get(
        "photo"
    )

    title = request.form.get(
        "title",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    if not photo:

        return jsonify({
            "error": "Please choose a photo."
        }), 400

    if not photo.filename:

        return jsonify({
            "error": "Please choose a photo."
        }), 400

    if not allowedFile(
        photo.filename
    ):

        return jsonify({
            "error": (
                "Only JPG, JPEG, PNG, GIF, "
                "and WEBP files are allowed."
            )
        }), 400

    realImageType = isRealImage(
        photo
    )

    if realImageType is None:

        return jsonify({
            "error": (
                "The uploaded file is not "
                "a valid image."
            )
        }), 400

    if not extensionMatchesImage(
        photo.filename,
        realImageType
    ):

        return jsonify({
            "error": (
                "The file extension does not "
                "match the actual image type."
            )
        }), 400

    if not photo.mimetype.startswith(
        "image/"
    ):

        return jsonify({
            "error": "Invalid image type."
        }), 400

    if not title:

        return jsonify({
            "error": "Photo title is required."
        }), 400

    if len(title) > 200:

        return jsonify({
            "error": (
                "Photo title must not exceed "
                "200 characters."
            )
        }), 400

    if len(description) > 1000:

        return jsonify({
            "error": (
                "Description must not exceed "
                "1000 characters."
            )
        }), 400

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    originalExtension = (
        photo.filename
        .rsplit(".", 1)[1]
        .lower()
    )

    uniqueFilename = (
        str(uuid.uuid4())
        + "."
        + originalExtension
    )

    safeFilename = secure_filename(
        uniqueFilename
    )

    filePath = os.path.join(
        UPLOAD_FOLDER,
        safeFilename
    )

    try:

        photo.save(
            filePath
        )

        userId = session["userId"]

        photoModel.createPhoto(
            userId,
            safeFilename,
            title,
            description
        )

        return jsonify({
            "message": (
                "Photo uploaded successfully"
            )
        }), 201

    except Exception:

        if os.path.exists(filePath):

            os.remove(
                filePath
            )

        return jsonify({
            "error": "Failed to upload photo."
        }), 500


def deletePhoto(id):
    """
    Deletes a photo only when it belongs
    to the logged-in user.
    """

    if "userId" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    photo = photoModel.getPhotoById(
        id
    )

    if not photo:

        return jsonify({
            "error": "Photo not found."
        }), 404

    userId = session["userId"]

    if photo["user_id"] != userId:

        return jsonify({
            "error": (
                "You are not allowed "
                "to delete this photo."
            )
        }), 403

    try:

        filePath = os.path.join(
            UPLOAD_FOLDER,
            photo["file_name"]
        )

        if os.path.exists(filePath):

            os.remove(
                filePath
            )

        photoModel.deletePhoto(
            id
        )

        return jsonify({
            "message": (
                "Photo deleted successfully."
            )
        })

    except Exception:

        return jsonify({
            "error": "Failed to delete photo."
        }), 500


def getComments(photoId):
    """
    Returns all comments for a specific photo.
    """

    comments = commentController.getComments(
        photoId
    )

    return jsonify(
        comments
    )


def addComment():
    """
    Adds a new comment to a photo.
    """

    if "userId" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid request."
        }), 400

    photoId = data.get(
        "photoId"
    )

    commentText = data.get(
        "comment",
        ""
    )

    if not photoId:

        return jsonify({
            "error": "Photo ID is required."
        }), 400

    photo = photoModel.getPhotoById(
        photoId
    )

    if not photo:

        return jsonify({
            "error": "Photo not found."
        }), 404

    try:

        comment = commentController.addComment(
            session["userId"],
            photoId,
            commentText
        )

        return jsonify({
            "message": (
                "Comment added successfully."
            ),
            "comment": comment
        }), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


def uploadedImage(filename):
    """
    Serves an uploaded image from the upload folder.
    """

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# Create the application's manual router.

router = Router()


router.add(
    "GET",
    "/",
    home
)

router.add(
    "GET",
    "/photos",
    photos
)

router.add(
    "GET",
    "/photo/{id}",
    photoDetails
)

router.add(
    "GET",
    "/register",
    register
)

router.add(
    "POST",
    "/register",
    register
)

router.add(
    "GET",
    "/login",
    login
)

router.add(
    "POST",
    "/login",
    login
)

router.add(
    "GET",
    "/logout",
    logout
)

router.add(
    "GET",
    "/upload",
    upload
)

router.add(
    "POST",
    "/upload",
    upload
)

router.add(
    "DELETE",
    "/delete-photo/{id}",
    deletePhoto
)

router.add(
    "GET",
    "/comments/{photoId}",
    getComments
)

router.add(
    "POST",
    "/comments",
    addComment
)

router.add(
    "GET",
    "/uploads/{filename}",
    uploadedImage
)


@app.route(
    "/",
    defaults={"path": ""}
)
@app.route(
    "/<path:path>",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
)
def manualRouterHandler(path):
    """
    Pass every application request to the custom manual router.

    Flask is used only to receive the HTTP request.
    URL matching and dispatching are handled by the custom Router.
    """

    requestPath = "/" + path

    try:

        return router.dispatch(
            request.method,
            requestPath
        )

    except ValueError:

        return jsonify({
            "error": "Route not found"
        }), 404


if __name__ == "__main__":

    app.run()
