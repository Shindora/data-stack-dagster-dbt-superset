FROM python:3.11-slim AS compile-image
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    git \
    g++ \
    cmake \
    libssl-dev

RUN python -m venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"


RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

FROM python:3.11-slim AS build-image

COPY --from=compile-image /opt/venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY dagster-dbt dagster-dbt

WORKDIR /dagster-dbt

RUN pip install -e ".[dev]"

WORKDIR /dagster-dbt/ecommerce_dm/dbt

RUN dbt deps

WORKDIR /dagster-dbt/ecommerce_dm
