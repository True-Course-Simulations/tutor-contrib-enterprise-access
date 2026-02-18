# syntax=docker/dockerfile:1
FROM python:3.12-slim

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc g++ make curl \
    libpq-dev default-libmysqlclient-dev pkg-config \
  && rm -rf /var/lib/apt/lists/*

# Create unprivileged app user (like license-manager)
ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app

ARG ENTERPRISE_ACCESS_REPO={{ ENTERPRISE_ACCESS_REPO }}
ARG ENTERPRISE_ACCESS_VERSION={{ OPENEDX_COMMON_VERSION }}

ENV ENTERPRISE_ACCESS_APP_DIR=/openedx/enterprise-access
WORKDIR ${ENTERPRISE_ACCESS_APP_DIR}

RUN git clone --depth 1 --branch ${ENTERPRISE_ACCESS_VERSION} ${ENTERPRISE_ACCESS_REPO} . \
 || (git clone --depth 1 ${ENTERPRISE_ACCESS_REPO} . && git checkout ${ENTERPRISE_ACCESS_VERSION})

# Create venv
RUN python -m venv /openedx/venv

# Make venv default python/pip everywhere (this prevents "no Django" issues)
ENV VIRTUAL_ENV=/openedx/venv
ENV PATH="/openedx/venv/bin:${PATH}"

# Install python deps
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements/production.txt \
 && pip install --no-cache-dir django-log-request-id django-redis whitenoise gunicorn

# Copy plugin management commands into the repo
COPY --chown=app:app ./apps/enterprise_access/management/commands/*.py \
  /openedx/enterprise-access/enterprise_access/apps/core/management/commands/

ENV DJANGO_SETTINGS_MODULE=enterprise_access.settings.production

# Ensure static root is known + collect into it
# NOTE: Like license-manager, we use repo settings at build time.
# At runtime Tutor overrides DJANGO_SETTINGS_MODULE to enterprise_access.settings.tutor.production.
ENV STATIC_ROOT=/openedx/staticfiles
RUN mkdir -p /openedx/staticfiles \
 && python manage.py collectstatic --noinput \
 && cp -r /openedx/enterprise-access/enterprise_access/assets/* /openedx/staticfiles/

# Runtime user
USER ${APP_USER_ID}

# Runtime default settings
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "enterprise_access.wsgi:application"]
