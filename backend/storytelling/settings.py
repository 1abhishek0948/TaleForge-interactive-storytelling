from datetime import timedelta
from pathlib import Path
import os
import sys
from urllib.parse import quote_plus, urlparse

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"

if str(APPS_DIR) not in sys.path:
    sys.path.insert(0, str(APPS_DIR))

load_dotenv(BASE_DIR / ".env")

try:
    import whitenoise  # noqa: F401

    HAS_WHITENOISE = True
except Exception:
    HAS_WHITENOISE = False


def csv_env(name: str, default: str = "") -> list[str]:
    return [value.strip() for value in os.getenv(name, default).split(",") if value.strip()]


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if not DEBUG and (
    not SECRET_KEY
    or SECRET_KEY == "unsafe-secret-key-change-me"
    or SECRET_KEY == "change-me-in-production"
):
    raise ImproperlyConfigured("Set a secure DJANGO_SECRET_KEY when DEBUG=false.")

ALLOWED_HOSTS = csv_env(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,.railway.app,.up.railway.app,.onrender.com",
)

railway_public_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
railway_static_url = os.getenv("RAILWAY_STATIC_URL", "").strip()
render_external_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
render_external_url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
for raw_value in (railway_public_domain, railway_static_url):
    if not raw_value:
        continue
    normalized = raw_value if "://" in raw_value else f"https://{raw_value}"
    host = urlparse(normalized).hostname
    if host and host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

for raw_value in (render_external_hostname, render_external_url):
    if not raw_value:
        continue
    normalized = raw_value if "://" in raw_value else f"https://{raw_value}"
    host = urlparse(normalized).hostname
    if host and host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "stories",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if HAS_WHITENOISE:
    MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = "storytelling.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "storytelling.wsgi.application"
ASGI_APPLICATION = "storytelling.asgi.application"

database_url = os.getenv("DATABASE_URL", "").strip()
if not database_url:
    db_name = os.getenv("DB_NAME") or os.getenv("PGDATABASE", "storytelling")
    db_user = quote_plus(os.getenv("DB_USER") or os.getenv("PGUSER", "postgres"))
    db_password = quote_plus(os.getenv("DB_PASSWORD") or os.getenv("PGPASSWORD", "postgres"))
    db_host = os.getenv("DB_HOST") or os.getenv("PGHOST", "localhost")
    db_port = os.getenv("DB_PORT") or os.getenv("PGPORT", "5432")
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

db_ssl_require_env = os.getenv("DB_SSL_REQUIRE")
if db_ssl_require_env is None:
    db_ssl_require = os.getenv("PGSSLMODE", "").lower() == "require" or (not DEBUG)
else:
    db_ssl_require = db_ssl_require_env.lower() == "true"

DATABASES = {
    "default": dj_database_url.parse(
        database_url,
        conn_max_age=600,
        ssl_require=db_ssl_require,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
if HAS_WHITENOISE:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.getenv("THROTTLE_ANON", "100/hour"),
        "user": os.getenv("THROTTLE_USER", "600/hour"),
        "auth": os.getenv("THROTTLE_AUTH", "30/hour"),
        "translation": os.getenv("THROTTLE_TRANSLATION", "60/hour"),
    },
    "DEFAULT_PAGINATION_CLASS": "stories.pagination.DefaultPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Interactive Storytelling API",
    "DESCRIPTION": "APIs for branching interactive storytelling.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CORS_ALLOWED_ORIGINS = csv_env("CORS_ALLOWED_ORIGINS", "http://localhost:5173")
csrf_from_env = csv_env("CSRF_TRUSTED_ORIGINS")
CSRF_TRUSTED_ORIGINS = csrf_from_env or CORS_ALLOWED_ORIGINS

frontend_url = os.getenv("FRONTEND_URL", "").strip()
if frontend_url:
    if frontend_url not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(frontend_url)
    if frontend_url not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(frontend_url)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
ENABLE_GOOGLE_TRANSLATE_PROXY = os.getenv("ENABLE_GOOGLE_TRANSLATE_PROXY", "false").lower() == "true"
SUPPORTED_TRANSLATION_LANGUAGES = csv_env("SUPPORTED_TRANSLATION_LANGUAGES", "en,hi")
ENABLE_DEMO_LOGIN_USERS = os.getenv("ENABLE_DEMO_LOGIN_USERS", "true" if DEBUG else "false").lower() == "true"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG and os.getenv("SECURE_SSL_REDIRECT", "true").lower() == "true"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "3600" if not DEBUG else "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
