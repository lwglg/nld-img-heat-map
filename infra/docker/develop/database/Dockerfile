FROM postgres:16-alpine

# Set timezone
ARG TZ
RUN apk add --no-cache tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# Healthcheck script to verify if database is up.
COPY ./infra/docker/develop/database/scripts/is-database-up.sh ./
COPY ./infra/docker/develop/database/init /docker-entrypoint-initdb.d/
RUN chmod +x is-database-up.sh

EXPOSE 5000

# two minutes should be enough to initialize the database
# 2min = 120s => 120s/5s = 24 retries...
HEALTHCHECK \
    --interval=5s \
    --timeout=2s \
    --retries=24 \
    CMD [ "./is-database-up.sh" ]
