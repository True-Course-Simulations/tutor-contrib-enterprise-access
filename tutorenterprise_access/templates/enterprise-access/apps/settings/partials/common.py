import os

# -------------------------------------------------------------------
# Common Tutor overrides for enterprise-access
# Rendered by Tutor into the container at build time.
# -------------------------------------------------------------------

DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", "0")))

SECRET_KEY = os.environ.get("ENTERPRISE_ACCESS_DJANGO_SECRET_KEY", "{{ ENTERPRISE_ACCESS_DJANGO_SECRET_KEY }}")

# If your service uses these:
TIME_ZONE = os.environ.get("TIME_ZONE", "{{ TIME_ZONE | default('UTC') }}")
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "{{ LANGUAGE_CODE | default('en-us') }}")

# Hosts / CSRF
ENTERPRISE_ACCESS_HOSTNAME = "{{ ENTERPRISE_ACCESS_HOST }}"
ALLOWED_HOSTS = list(set((ALLOWED_HOSTS if "ALLOWED_HOSTS" in globals() else []) + [
    ENTERPRISE_ACCESS_HOSTNAME,
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]))

CSRF_TRUSTED_ORIGINS = list(set((CSRF_TRUSTED_ORIGINS if "CSRF_TRUSTED_ORIGINS" in globals() else []) + [
    f"http://{ENTERPRISE_ACCESS_HOSTNAME}",
    f"https://{ENTERPRISE_ACCESS_HOSTNAME}",
]))

# Database (reuse Tutor MySQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ ENTERPRISE_ACCESS_MYSQL_DATABASE }}",
        "USER": "{{ ENTERPRISE_ACCESS_MYSQL_USERNAME }}",
        "PASSWORD": "{{ ENTERPRISE_ACCESS_MYSQL_PASSWORD }}",
        "HOST": "mysql",
        "PORT": 3306,
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

# Cache (reuse Tutor Redis)
REDIS_DB = int(os.environ.get("ENTERPRISE_ACCESS_REDIS_DB", "{{ ENTERPRISE_ACCESS_REDIS_DB }}"))
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://redis:6379/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "enterprise-access",
    }
}

# If the service uses Django sessions in cache:
SESSION_ENGINE = os.environ.get("SESSION_ENGINE", "django.contrib.sessions.backends.cache")
SESSION_CACHE_ALIAS = "default"

# Static/media defaults (safe even if unused)
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
