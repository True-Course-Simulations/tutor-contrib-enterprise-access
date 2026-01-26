# Prefer upstream dev settings if they exist in your branch.
# If your repo does NOT have enterprise_access.settings.devstack (or similar),
# keep the import below as production and just turn DEBUG on.
try:
    from enterprise_access.settings.devstack import *  # type: ignore  # pylint: disable=wildcard-import, unused-wildcard-import
except Exception:  # noqa: BLE001
    from enterprise_access.settings.production import *  # pylint: disable=wildcard-import, unused-wildcard-import

{% include "enterprise-access/apps/settings/partials/common.py" %}

DEBUG = True

# In dev you often want permissive cookies:
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
