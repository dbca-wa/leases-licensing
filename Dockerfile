# syntax = docker/dockerfile:1

ARG BASE_IMAGE=ghcr.io/dbca-wa/docker-apps-dev:ubuntu_2604_base_python

# --- Builder: all build-time tools, Node.js, Poetry, Vue build, collectstatic ---
FROM ${BASE_IMAGE} AS builder

LABEL maintainer="asi@dbca.wa.gov.au"
LABEL org.opencontainers.image.source="https://github.com/dbca-wa/leases-licensing"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Australia/Perth \
    NODE_MAJOR=24 \
    EMAIL_INSTANCE='DEV' \    
    NON_PROD_EMAIL='none@none.com' \
    POETRY_VERSION=2.1.3 \
    SECRET_KEY="ThisisNotRealKey" \
    PRODUCTION_EMAIL=False \
    SITE_PREFIX='lals-dev' \
    SITE_DOMAIN='dbca.wa.gov.au'

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    binutils \
    ca-certificates \
    curl \
    libfreetype-dev \
    gdal-bin \
    gnupg \
    g++ \
    gcc \
    git \
    libgdal-dev \
    libmagic-dev \
    libproj-dev \
    libpq-dev \
    libspatialindex-dev \
    patch \
    python3-dev \
    python3-gdal \
    python3-pil \
    python3-pip \
    python3-setuptools \
    python3-venv \
    tzdata && \
    update-ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js and clean up in the same layer
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install --no-install-recommends -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -g 5000 oim && \
    useradd -g 5000 -u 5000 oim -s /bin/bash -d /app && \
    mkdir /app && \
    chown -R oim:oim /app

WORKDIR /app
USER oim

ENV POETRY_HOME=/app/poetry
ENV VIRTUAL_ENV=/app/.venv
ENV PATH=$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH

# Install Poetry into its own venv
RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install --upgrade pip && \
    $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION

# 1) Copy only dependency files first so the install layer is cached independently of code changes
COPY --chown=oim:oim pyproject.toml poetry.lock poetry.toml ./
RUN poetry install --only main --no-interaction --no-ansi

# 2) Copy application code (changes here won't bust the poetry install cache)
COPY --chown=oim:oim manage.py manage.sh ./
COPY --chown=oim:oim leaseslicensing ./leaseslicensing

# Build Vue frontend, then discard node_modules so they aren't copied to runtime
RUN cd /app/leaseslicensing/frontend/leaseslicensing && npm ci --omit=dev
RUN cd /app/leaseslicensing/frontend/leaseslicensing && npm run build && \
    rm -rf /app/leaseslicensing/frontend/leaseslicensing/node_modules

# Collect static files
RUN touch /app/.env && \
    poetry run python manage.py collectstatic --no-input && \
    poetry run python manage.py script_hash_indexes --skip-checks

# --- Runtime: clean image with only runtime packages and built artifacts ---
FROM ${BASE_IMAGE} AS runtime

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
    ENABLE_SRI_CHECK=True

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    ca-certificates \
    tzdata \
    wget && \
    apt-get remove --purge -y binutils rust-coreutils git mtr patch vim 2>/dev/null || true && \
    apt-get autoremove -y && \
    update-ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -g 5000 oim && \
    useradd -g 5000 -u 5000 oim -s /bin/bash -d /app && \
    usermod -a -G sudo oim && \
    mkdir -p /app/logs && \
    chown -R oim:oim /app && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY startup.sh /
RUN chmod 755 /startup.sh && \
    chmod +s /startup.sh && \
    echo "oim  ALL=(ALL)  NOPASSWD: /startup.sh" > /etc/sudoers.d/oim && \
    wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/default_script_installer.sh \
        -O /tmp/default_script_installer.sh && \
    chmod 755 /tmp/default_script_installer.sh && \
    /tmp/default_script_installer.sh && \
    rm -rf /tmp/*

USER oim
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH

COPY --from=builder --chown=oim:oim /app/.venv /app/.venv
COPY --from=builder --chown=oim:oim /app/leaseslicensing /app/leaseslicensing
COPY --from=builder --chown=oim:oim /app/staticfiles_ll /app/staticfiles_ll
COPY --from=builder --chown=oim:oim /app/manage.py /app/manage.py
COPY --from=builder --chown=oim:oim /app/manage.sh /app/manage.sh
COPY --from=builder --chown=oim:oim /app/pyproject.toml /app/pyproject.toml
COPY --from=builder --chown=oim:oim /app/.env /app/.env
COPY --from=builder --chown=oim:oim /app/sri-manifest.json /app/sri-manifest.json
COPY --from=builder --chown=oim:oim /app/sri-files /app/sri-files
COPY --chown=oim:oim gunicorn.ini.py python-cron ./

EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]
