CREATE SCHEMA IF NOT EXISTS monitoring AUTHORIZATION postgres;

CREATE TABLE monitoring.hosts (
    time                TIMESTAMPTZ     NOT NULL,
    hostname            TEXT            NOT NULL,
    environment         TEXT            NULL,
    os                  TEXT            NULL,
    total_cpu           SMALLINT        NULL,
    total_memory        DECIMAL(4,2)    NULL,
    cpu_usage           DECIMAL(4,2)    NULL,
    memory_usage        DECIMAL(4,2)    NULL,
    disk_usage          DECIMAL(4,2)    NULL,
    containers_running  SMALLINT        NULL,
    containers_stopped  SMALLINT        NULL,
    docker_cpus         SMALLINT        NULL,
    docker_memory       DECIMAL(4,2)    NULL
);

SELECT create_hypertable('monitoring.hosts', 'time');



CREATE TABLE monitoring.containers (
    time                TIMESTAMPTZ     NOT NULL,
    name                TEXT            NOT NULL,
    image               TEXT            NULL,
    state               TEXT            NULL,
    status              TEXT            NULL,
    mounts              SMALLINT        NULL,
    networks            TEXT            NULL
);

SELECT create_hypertable('monitoring.containers', 'time');