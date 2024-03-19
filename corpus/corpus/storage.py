import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CKEditorStorage(FileSystemStorage):
    location = os.path.join(settings.MEDIA_ROOT, "ckeditor")
    base_url = urljoin(settings.MEDIA_URL, "ckeditor/")
