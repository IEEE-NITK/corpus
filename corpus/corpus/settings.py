"""
Django settings for corpus project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

if os.getenv("LIVECYCLE"):
    from dotenv import load_dotenv

    load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "averysecretdjangokey")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.getenv("ENVIRONMENT") == "DEVELOPMENT") or (
    os.getenv("LIVECYCLE") is not None
)

# TODO: Stricter host policies
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]
if os.getenv("ENVIRONMENT", "PRODUCTION") == "PRODUCTION":
    ALLOWED_HOSTS.append("ieee.nitk.ac.in")
    CSRF_TRUSTED_ORIGINS.append("https://ieee.nitk.ac.in")

if os.getenv("LIVECYCLE"):
    ALLOWED_HOSTS.append("*")
    CSRF_TRUSTED_ORIGINS.extend(["http://*", "https://*"])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages.apps.PagesConfig",
    "config.apps.ConfigConfig",
    "accounts.apps.AccountsConfig",
    "embedathon.apps.EmbedathonConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "corpus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "corpus.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "corpus"),
        "USER": os.getenv("POSTGRES_USER", "corpus"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "corpus"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

if os.getenv("LIVECYCLE"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "corpus.db",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "templates/static"]
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "templates/static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Corpus Settings
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "accounts.backend.CorpusAuthBackend",
]
LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = ""
LOGOUT_REDIRECT_URL = "/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
