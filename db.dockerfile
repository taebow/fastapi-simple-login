FROM postgres:latest

ENV POSTGRES_USER test
ENV POSTGRES_PASSWORD test
ENV POSTGRES_DB test

RUN mkdir -p /docker-entrypoint-initdb.d

RUN echo 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";' > /docker-entrypoint-initdb.d/uuid-ossp.sql
RUN echo 'CREATE EXTENSION IF NOT EXISTS "pgcrypto";' > /docker-entrypoint-initdb.d/pgcrypto.sql