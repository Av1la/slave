

CREATE TABLE account_ml (
    id serial,

    usr text NOT NULL,
    psw text NOT NULL,

    mlid text,
    first_name text,
    last_name text,
    permalink text,
    mltype text,

    -- obtido no ultimo estagio
    token text,
    client_id text,
    client_secret text,

    -- dados de controle
    created_at int,
    captured_at int,
    started_at int,
    finished_at int,
    last_token_check int
);