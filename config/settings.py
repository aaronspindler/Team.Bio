import os
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from config.sentry import traces_sampler

sentry_sdk.init(
    dsn="https://7293ea960f6a43fba4b4f73fe60bb6bc@o555567.ingest.sentry.io/4503933521231872",
    integrations=[
        DjangoIntegration(),
    ],
    traces_sampler=traces_sampler,
    send_default_pii=True,
)

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", False)

PRICE_PER_USER = 100
DEFAULT_TRIAL_DAYS = 30

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "team.bio",
    "www.team.bio",
]
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    # Third-party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "debug_toolbar",
    "storages",
    "crispy_forms",
    "crispy_tailwind",
    "colorfield",
    # Local
    "accounts",
    "pages",
    "companies",
    "utils",
    "billing",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

DATABASES = {"default": env.db()}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": None},
        },
        "KEY_PREFIX": "teambio",
    }
}

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# AWS
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

# S3
AWS_STORAGE_BUCKET_NAME = "team-bio"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
PUBLIC_MEDIA_LOCATION = ""
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "config.storage_backends.PublicStorage"

# SES
EMAIL_BACKEND = "django_ses.SESBackend"
DEFAULT_FROM_EMAIL = '"Team Bio" <support@team.bio>'
SERVER_EMAIL = "support@team.bio"

INTERNAL_IPS = ["127.0.0.1"]

AUTH_USER_MODEL = "accounts.User"

SITE_ID = 1
BASE_URL = "https://team.bio/"
LOGIN_REDIRECT_URL = "company_home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

BLACKLISTED_DOMAIN_ROOTS = [
    "gmail.com",
    "live.com",
    "icloud.com",
    "live.ca",
    "proton.me",
]

# Stripe
STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = env("STRIPE_PRICE_ID")
STRIPE_ENDPOINT_SECRET = env("STRIPE_ENDPOINT_SECRET")

# Google Maps
GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY")

# Mapbox
MAPBOX_API_KEY = env("MAPBOX_API_KEY")

if DEBUG:
    BASE_URL = "http://localhost:8000/"
