from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_image(image):
    file_size = image.file.size
    limit = 5 * 1024 * 1024  # 5 MB limit
    if file_size > limit:
        raise ValidationError("Image size exceeds 5MB.")
