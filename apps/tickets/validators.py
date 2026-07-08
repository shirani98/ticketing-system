ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


def validate_image_upload(uploaded_file) -> None:
    from rest_framework.exceptions import ValidationError

    if uploaded_file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            {"photo": "Only JPEG, PNG, and WebP images are allowed."}
        )
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        raise ValidationError({"photo": "Image must be 5 MB or smaller."})
