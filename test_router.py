from app.routes import router


allPhotosResult = router.dispatch(
    "GET",
    "/photos"
)

print("All photos route:", allPhotosResult)


singlePhotoResult = router.dispatch(
    "GET",
    "/photo/25"
)

print("Single photo route:", singlePhotoResult)