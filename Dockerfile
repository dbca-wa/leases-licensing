# syntax = docker/dockerfile:1.2

# Prepare the base environment.
FROM ubuntu:24.04 AS builder_base_oim_leaseslicensing

LABEL maintainer="asi@dbca.wa.gov.au"
LABEL org.opencontainers.image.source="https://github.com/dbca-wa/leases-licensing"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Australia/Perth \
    EMAIL_HOST="email.server" \
    DEFAULT_FROM_EMAIL='no-reply@dbca.wa.gov.au' \
    NOTIFICATION_EMAIL='none@none.com' \
    NON_PROD_EMAIL='none@none.com' \
    PRODUCTION_EMAIL=False \
    EMAIL_INSTANCE='DEV' \
    SECRET_KEY="ThisisNotRealKey" \
    SITE_PREFIX='lals-dev' \
    SITE_DOMAIN='dbca.wa.gov.au' \
    OSCAR_SHOP_NAME='Parks & Wildlife' \
    BPAY_ALLOWED=False \
    POETRY_VERSION=2.1.3 \
    NODE_MAJOR=22

FROM builder_base_oim_leaseslicensing AS apt_packages_leaseslicensing

# Use Australian Mirrors
RUN sed 's/archive.ubuntu.com/au.archive.ubuntu.com/g' /etc/apt/sources.list > /etc/apt/sourcesau.list && \
    mv /etc/apt/sourcesau.list /etc/apt/sources.list
# Use Australian Mirrors

RUN --mount=type=cache,target=/var/cache/apt apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    binutils \
    ca-certificates \
    cron \
    curl \
    libfreetype-dev \
    gdal-bin \
    gnupg \
    g++ \
    gcc \
    git \
    gunicorn \
    htop \
    ipython3 \
    libgdal-dev \
    libmagic-dev \
    libproj-dev \
    libpq-dev \
    libreoffice \
    libspatialindex-dev \
    mtr \
    patch \
    pipx \
    postgresql-client \
    python3-dev \
    python3-gdal \
    python3-pil \
    python3-pip \
    python3-setuptools \
    python3-venv \
    ipython3 \
    rsyslog \
    sqlite3 \
    ssh \
    sudo \
    tzdata \
    vim \
    wget && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates

FROM apt_packages_leaseslicensing AS node_leaseslicensing

# install node 22
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs

FROM node_leaseslicensing AS configure_leaseslicensing

COPY startup.sh  /

RUN chmod 755 /startup.sh && \
    chmod +s /startup.sh && \
    groupadd -g 5000 oim && \
    useradd -g 5000 -u 5000 oim -s /bin/bash -d /app && \
    usermod -a -G sudo oim && \
    echo "oim  ALL=(ALL)  NOPASSWD: /startup.sh" > /etc/sudoers.d/oim && \
    mkdir /app && \
    chown -R oim.oim /app && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/default_script_installer.sh -O /tmp/default_script_installer.sh && \
    chmod 755 /tmp/default_script_installer.sh && \
    /tmp/default_script_installer.sh && \
    rm -rf /tmp/*

FROM configure_leaseslicensing AS python_dependencies_leaseslicensing

WORKDIR /app
USER oim

ENV POETRY_HOME=/app/poetry
ENV PATH=$POETRY_HOME/bin:$PATH
COPY --chown=oim:oim pyproject.toml poetry.lock ./
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION
RUN poetry completions bash > ~/.bash_completion && \
    poetry run pip install --upgrade pip
RUN --mount=type=cache,target=~/.cache/pypoetry/cache poetry install --only main --no-interaction --no-ansi

FROM python_dependencies_leaseslicensing AS install_build_vue3_leaseslicensing

COPY --chown=oim:oim leaseslicensing ./leaseslicensing

RUN cd /app/leaseslicensing/frontend/leaseslicensing ; npm ci --omit=dev && \
    cd /app/leaseslicensing/frontend/leaseslicensing ; npm run build

FROM install_build_vue3_leaseslicensing AS collect_static_leaseslicensing

COPY --chown=oim:oim manage.py manage.sh ./
RUN touch /app/.env && \
    poetry run python manage.py collectstatic --no-input

FROM collect_static_leaseslicensing AS launch_leaseslicensing

COPY --chown=oim:oim gunicorn.ini.py python-cron ./
EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]
