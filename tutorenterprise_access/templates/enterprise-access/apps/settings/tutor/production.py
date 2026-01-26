from enterprise_access.settings.production import *  # pylint: disable=wildcard-import, unused-wildcard-import

{% include "enterprise-access/apps/settings/partials/common.py" %}

# Production-ish defaults
DEBUG = False

# If you terminate TLS at Caddy/Traefik/nginx, this is typical:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
