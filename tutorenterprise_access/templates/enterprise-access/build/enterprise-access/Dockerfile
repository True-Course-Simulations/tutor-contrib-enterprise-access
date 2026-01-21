# syntax=docker/dockerfile:1
# Enterprise Access service image built by Tutor.
#
# NOTE: We intentionally clone the upstream repo at build time instead of vendoring
# it inside this plugin.

ARG OPENEDX_IMAGE
FROM ${OPENEDX_IMAGE}

USER root

# Minimal build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    g++ \
    make \
    libpq-dev \
    default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

ARG ENTERPRISE_ACCESS_REPO

# App location
ENV ENTERPRISE_ACCESS_APP_DIR=/openedx/enterprise-access

RUN mkdir -p ${ENTERPRISE_ACCESS_APP_DIR}
WORKDIR ${ENTERPRISE_ACCESS_APP_DIR}

# Clone & checkout the requested ref. We use --depth=1 to keep builds fast.
RUN git clone --depth 1 ${ENTERPRISE_ACCESS_REPO} . \
 && (git fetch --depth 1 origin ${{ OPENEDX_COMMON_VERSION }} || true) \
 && git checkout ${{ OPENEDX_COMMON_VERSION }}

# Copy Tutor-specific settings overlay (kept in this plugin)
# These files should be robust across named releases; they only override config via env vars.
COPY ./settings/tutor.py ${ENTERPRISE_ACCESS_APP_DIR}/enterprise_access/settings/tutor.py

# Install python requirements
# enterprise-access repos typically provide requirements.txt; we fall back to pip install .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi \
 && pip install --no-cache-dir -e .

ENV DJANGO_SETTINGS_MODULE=enterprise_access.settings.tutor

EXPOSE 8000

# Default command: gunicorn webserver
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "enterprise_access.wsgi:application"]
