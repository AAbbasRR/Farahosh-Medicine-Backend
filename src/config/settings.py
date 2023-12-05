from pathlib import Path
from decouple import config
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    "*",
]
FRONT_SITE_DOMAIN = config("FRONT_SITE_DOMAIN")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "corsheaders",
    "rest_framework",
    "django_filters",
    # installed apps
    "app_user",
    "app_medicine",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # cors-headers
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# Database
SQL_LITE_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

if config("USE_MYSQL", default=False, cast=bool):
    MYSQL_DATABASE = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_NAME"),
        "USER": config("MYSQL_USER"),
        "PASSWORD": config("MYSQL_PASS"),
        "HOST": config("MYSQL_HOST"),
        "PORT": config("MYSQL_PORT", cast=int),
    }

if config("USE_POSTGRES", default=False, cast=bool):
    POSTGRES_SQL_DATABASE = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_NAME"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASS"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT", cast=int),
    }


def get_default_detabase(default_database=config("DEFAULT_DATABASE_NAME", default="")):
    match default_database.upper():
        case "MYSQL":
            return MYSQL_DATABASE
        case "POSTGRESQL":
            return POSTGRES_SQL_DATABASE
        case _:
            return SQL_LITE_DATABASE


DATABASES = {"default": get_default_detabase()}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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

# ___django settings___ #
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "app_user.User"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
# Media files (Images, Files)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Internationalization
LANGUAGE_CODE = "fa"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ___django rest framework settings___ #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# __django rest framework simplejwt setting__ #
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        hours=config("ACCESS_TOKEN_LIFETIME", default=1, cast=int)
    ),
}

# __django multi language settings__ #
LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

# ___Redis settings___ #
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
REDIS_DB = config("REDIS_DB", default=0, cast=int)

# ___Request Api Options___ #
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = [
    "*",
]

# __Custom Settings__ #
DATE_INPUT_FORMATS = "%Y-%m-%d"
TIME_INPUT_FORMATS = "%H:%M:%S"
MAXIMUM_COUNT_TRY_WRONG_OTP_CODE = 5

# __SMS Portal__ #
SMS_PORTAL = {
    "username": config("SMS_PORTAL_USERNAME"),
    "pass": config("SMS_PORTAL_PASS"),
}
DEPENDENT_SMS_ON_DEBUG = config("DEPENDENT_SMS_ON_DEBUG", cast=bool, default=True)
