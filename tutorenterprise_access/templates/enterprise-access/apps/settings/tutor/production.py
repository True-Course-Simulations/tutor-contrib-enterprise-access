from enterprise_access.settings.production import *  # pylint: disable=wildcard-import, unused-wildcard-import

{% include "enterprise-access/apps/settings/partials/common.py" %}

DEBUG = False

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ ENTERPRISE_ACCESS_OAUTH2_KEY_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_ACCESS_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "{{ 'https' if ENABLE_HTTPS else 'http' }}://{{ LMS_HOST }}"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ENABLE_HTTPS %}True{% else %}False{% endif %}
BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ENTERPRISE_ACCESS_OAUTH2_KEY }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_ACCESS_OAUTH2_SECRET }}"