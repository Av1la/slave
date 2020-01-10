create schema job;
create schema log;


CREATE TABLE job.queue (
    id bigserial, 
    md5 text,

    created_at decimal(22, 10),
    updated_at decimal(22, 10),
    started_at decimal(22, 10),
    finished_at decimal(22, 10)
);


CREATE TABLE job.worker (
    id bigserial, 
    md5 text,

    queue_md5 text,
    classname text,
    params text,
    result text,

    created_at decimal(22, 10),
    updated_at decimal(22, 10),
    started_at decimal(22, 10),
    finished_at decimal(22, 10)
);


CREATE TABLE log.worker (
    id bigserial, 
    md5 text,

    worker_md5 text,
    log text,
    created_at decimal(22, 10),
);

