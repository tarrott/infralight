CREATE SCHEMA IF NOT EXISTS monitoring AUTHORIZATION postgres;

CREATE TABLE IF NOT EXISTS monitoring.hosts (
    time                TIMESTAMPTZ     NOT NULL,
    hostname            TEXT            NOT NULL,
    environment         TEXT            NULL,
    os                  TEXT            NULL,
    uptime              TEXT            NULL,
    total_cpu           TEXT            NULL,
    total_memory        TEXT            NULL,
    cpu_usage           DECIMAL(4,2)    NULL,
    memory_usage        DECIMAL(4,2)    NULL,
    disk_usage          DECIMAL(4,2)    NULL,
    containers_running  SMALLINT        NULL,
    containers_stopped  SMALLINT        NULL
);
SELECT create_hypertable('monitoring.hosts', 'time');

CREATE TABLE IF NOT EXISTS monitoring.containers (
    time                TIMESTAMPTZ     NOT NULL,
    name                TEXT            NOT NULL,
    image               TEXT            NULL,
    state               TEXT            NULL,
    status              TEXT            NULL,
    mounts              SMALLINT        NULL,
    networks            TEXT            NULL
);
SELECT create_hypertable('monitoring.containers', 'time');