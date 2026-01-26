# syntax=docker/dockerfile:1

ARG OPENEDX_IMAGE={{ DOCKER_IMAGE_OPENEDX }}
FROM ${OPENEDX_IMAGE}

USER root

# Install Python 3.12 and build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    git gcc g++ make \
    libpq-dev default-libmysqlclient-dev \
 && add-apt-repository ppa:deadsnakes/ppa \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
 && rm -rf /var/lib/apt/lists/*

# Make Python 3.12 the default python/pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 120 \
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 120

# Bootstrap pip for Python 3.12
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

ARG ENTERPRISE_ACCESS_REPO={{ ENTERPRISE_ACCESS_REPO }}
ARG ENTERPRISE_ACCESS_VERSION={{ OPENEDX_COMMON_VERSION }}

ENV ENTERPRISE_ACCESS_APP_DIR=/openedx/enterprise-access
RUN mkdir -p ${ENTERPRISE_ACCESS_APP_DIR}
WORKDIR ${ENTERPRISE_ACCESS_APP_DIR}

# Try branch/tag checkout directly
RUN git clone --depth 1 --branch ${ENTERPRISE_ACCESS_VERSION} ${ENTERPRISE_ACCESS_REPO} . \
 || (git clone --depth 1 ${ENTERPRISE_ACCESS_REPO} . && git checkout ${ENTERPRISE_ACCESS_VERSION})

COPY ./settings/tutor.py ${ENTERPRISE_ACCESS_APP_DIR}/enterprise_access/settings/tutor.py

# Always install using Python 3.12
RUN if [ -f requirements.txt ]; then python3.12 -m pip install --no-cache-dir -r requirements.txt; fi \
 && python3.12 -m pip install --no-cache-dir -e .

ENV DJANGO_SETTINGS_MODULE=enterprise_access.settings.tutor

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "enterprise_access.wsgi:application"]
