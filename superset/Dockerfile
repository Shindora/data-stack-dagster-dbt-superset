FROM apache/superset:3.0.4 

ARG SUPERSET_ADMIN
ARG SUPERSET_PASSWORD
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG SUPERSET_SECRET_KEY
# Switching to root to install the required packages
USER root
COPY --chown=superset:superset ./superset/assets .
RUN pip install psycopg2-binary==2.9.9
RUN pip install duckdb-engine==0.11.1
RUN pip install duckdb==0.10.0
USER superset
RUN superset fab create-admin \
              --username ${SUPERSET_ADMIN} \
              --firstname Superset \
              --lastname Admin \
              --email admin@example.com \
              --password ${SUPERSET_PASSWORD}

RUN superset db upgrade
RUN superset init

RUN superset set_database_uri -d postgres -u "postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@oltp:5432/postgres"