CREATE TABLE IF NOT EXISTS public.client_credentials
(
    client_id integer NOT NULL,
    clientname character varying(50) COLLATE pg_catalog."default",
    password character varying(50) COLLATE pg_catalog."default",
    email email COLLATE pg_catalog."default",
    created_on timestamp without time zone,
    CONSTRAINT client_credentials_pkey PRIMARY KEY (client_id)
)

