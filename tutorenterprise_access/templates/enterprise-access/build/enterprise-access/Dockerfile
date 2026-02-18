# syntax=docker/dockerfile:1
FROM python:3.12-slim

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc g++ make curl \
    libpq-dev default-libmysqlclient-dev pkg-config \
  && rm -rf /var/lib/apt/lists/*

ARG ENTERPRISE_ACCESS_REPO={{ ENTERPRISE_ACCESS_REPO }}
ARG ENTERPRISE_ACCESS_VERSION={{ OPENEDX_COMMON_VERSION }}

ENV ENTERPRISE_ACCESS_APP_DIR=/openedx/enterprise-access
WORKDIR ${ENTERPRISE_ACCESS_APP_DIR}

RUN git clone --depth 1 --branch ${ENTERPRISE_ACCESS_VERSION} ${ENTERPRISE_ACCESS_REPO} . \
 || (git clone --depth 1 ${ENTERPRISE_ACCESS_REPO} . && git checkout ${ENTERPRISE_ACCESS_VERSION})

RUN python -m venv /openedx/venv

# Install deps INTO THE VENV explicitly + install the app
RUN /openedx/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel \
 && /openedx/venv/bin/pip install --no-cache-dir -r requirements/production.txt \
 && /openedx/venv/bin/pip install --no-cache-dir django-log-request-id django-redis

ENV DJANGO_SETTINGS_MODULE=enterprise_access.settings.tutor.production
EXPOSE 8000

# Force venv gunicorn regardless of PATH overrides
CMD ["/openedx/venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "enterprise_access.wsgi:application"]
