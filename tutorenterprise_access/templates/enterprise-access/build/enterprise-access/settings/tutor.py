"""
Tutor settings overlay for enterprise-access.

We keep this small and environment-driven to reduce coupling to upstream changes.
It imports upstream production settings and overrides only what we must to run in Tutor.
"""
import os
from .production import *  # noqa: F401,F403

# -------------------------
# Core Django settings
# -------------------------

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

# Required secret key
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

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
        "LOCATION": "redis://{% if REDIS_USERNAME and REDIS_PASSWORD %}{{ REDIS_USERNAME }}:{{ REDIS_PASSWORD }}{% endif %}@{{ REDIS_HOST }}:{{ REDIS_PORT }}/{{ ENTERPRISECATALOG_CACHE_REDIS_DB }}",
    }
}

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", REDIS_URL)

# -------------------------
# Logging
# -------------------------
LOGGING["handlers"]["console"]["level"] = os.environ.get("DJANGO_LOG_LEVEL", "INFO")  # type: ignore[name-defined]

