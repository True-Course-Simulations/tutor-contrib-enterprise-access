import os

# -------------------------------------------------------------------
# Common Tutor overrides for enterprise-access
# Rendered by Tutor into the container at build time.
# -------------------------------------------------------------------

# -------------------------
# Logging
# -------------------------
LOGGING["handlers"]["console"]["level"] = os.environ.get("DJANGO_LOG_LEVEL", "INFO")  # type: ignore[name-defined]

DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", "0")))

SECRET_KEY = os.environ.get("ENTERPRISE_ACCESS_DJANGO_SECRET_KEY", "{{ ENTERPRISE_ACCESS_DJANGO_SECRET_KEY }}")

# If your service uses these:
TIME_ZONE = os.environ.get("TIME_ZONE", "{{ TIME_ZONE | default('UTC') }}")
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "{{ LANGUAGE_CODE | default('en-us') }}")

# Hosts / CORS / CSRF
_mfe_origin = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}"

# ALLOWED_HOSTS: extend safely
ALLOWED_HOSTS = list(set((globals().get("ALLOWED_HOSTS", []) or []) + [
    "{{ ENTERPRISE_ACCESS_HOST }}",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]))

# ---- CORS ----
# Prefer modern setting name; keep old one too for older django-cors-headers
CORS_ALLOWED_ORIGINS = list(set((globals().get("CORS_ALLOWED_ORIGINS", []) or []) + [
    _mfe_origin,
]))
CORS_ORIGIN_WHITELIST = list(set((globals().get("CORS_ORIGIN_WHITELIST", []) or []) + [
    _mfe_origin,
]))

# Most MFEs need cookies (session/JWT cookie). Without this you'll see blocked credentialed requests.
CORS_ALLOW_CREDENTIALS = True

# ---- CSRF ----
# Extend, don't overwrite, because upstream may set other trusted origins.
CSRF_TRUSTED_ORIGINS = list(set((globals().get("CSRF_TRUSTED_ORIGINS", []) or []) + [
    _mfe_origin,
]))

CSRF_COOKIE_SECURE = False

# -------------------------
# Database (MySQL by default in Tutor)
# -------------------------
DB_NAME = os.environ.get("ENTERPRISE_ACCESS_MYSQL_DATABASE", "enterprise_access")
DB_USER = os.environ.get("ENTERPRISE_ACCESS_MYSQL_USERNAME", "enterprise_access")
DB_PASSWORD = os.environ.get("ENTERPRISE_ACCESS_MYSQL_PASSWORD", "")
DB_HOST = os.environ.get("ENTERPRISE_ACCESS_MYSQL_HOST", "mysql")
DB_PORT = int(os.environ.get("ENTERPRISE_ACCESS_MYSQL_PORT", "3306"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

# -------------------------
# Cache + Celery (Redis from Tutor)
# -------------------------
REDIS_HOST = os.environ.get("ENTERPRISE_ACCESS_REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("ENTERPRISE_ACCESS_REDIS_PORT", "6379"))
REDIS_DB = int(os.environ.get("ENTERPRISE_ACCESS_REDIS_DB", "9"))  # keep separate from LMS/CMS by default

REDIS_URL = os.environ.get("ENTERPRISE_ACCESS_REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "KEY_PREFIX": "enterprise-access",
        "LOCATION": REDIS_URL,
    }
}

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", REDIS_URL)

# If the service uses Django sessions in cache:
SESSION_ENGINE = os.environ.get("SESSION_ENGINE", "django.contrib.sessions.backends.cache")
SESSION_CACHE_ALIAS = "default"

# Static/media defaults (safe even if unused)
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATIC_ROOT = os.environ.get("STATIC_ROOT", "/openedx/staticfiles")

MIDDLEWARE = list(MIDDLEWARE)

if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
    try:
        idx = MIDDLEWARE.index("django.contrib.sessions.middleware.SessionMiddleware")
    except ValueError:
        idx = 0
    MIDDLEWARE.insert(idx + 1, "whitenoise.middleware.WhiteNoiseMiddleware")

MIDDLEWARE = tuple(MIDDLEWARE)

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

import json
{% set jwt_rsa_key | rsa_import_key %}{{ JWT_RSA_PRIVATE_KEY }}{% endset %}

# --- JWT (match other Tutor services: embed JWKS instead of fetching over HTTP) ---
JWT_AUTH["JWT_ISSUER"] = "{{ JWT_COMMON_ISSUER }}"
JWT_AUTH["JWT_AUDIENCE"] = "{{ JWT_COMMON_AUDIENCE }}"
JWT_AUTH["JWT_SECRET_KEY"] = "{{ JWT_COMMON_SECRET_KEY }}"

# Enterprise-access tokens in your browser are RS512, so keep algorithm consistent.
JWT_AUTH["JWT_ALGORITHM"] = "RS512"
JWT_AUTH["JWT_VERIFY_EXPIRATION"] = True

# Embed a JWKS payload (avoid network fetch to /oauth2/jwks/)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "{{ jwt_rsa_key.e|long_to_base64 }}",
                "n": "{{ jwt_rsa_key.n|long_to_base64 }}",
            }
        ]
    }
)

# Allow tokens from the common issuer/audience, and use the LMS secret key mapping like other services
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "{{ JWT_COMMON_ISSUER }}",
        "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
        "SECRET_KEY": "{{ OPENEDX_SECRET_KEY }}",
    }
]

# Make sure edx-drf-extensions knows where to load user info (often needed for mapping / permissions)
EDX_DRF_EXTENSIONS = {
    "OAUTH2_USER_INFO_URL": "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2/user_info",
}
