from .development import *  # pylint: disable=wildcard-import, unused-wildcard-import

REDIS_DB = int(os.environ.get("ENTERPRISE_ACCESS_REDIS_DB", "{{ ENTERPRISE_ACCESS_REDIS_DB }}"))
CELERY_BROKER_URL = f"redis://redis:6379/{REDIS_DB}"
CELERY_RESULT_BACKEND = f"redis://redis:6379/{REDIS_DB}"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Optional: make local debugging easier (turn on only if you want synchronous tasks)
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True
