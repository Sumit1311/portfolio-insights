CREATE TABLE public.nav_user
(
  _id character varying(36) NOT NULL,
  first_name text,
  last_name text,
  email_address character varying(100),
  mobile_no character varying(15),
  password text,
  email_verification character varying(36),
  user_type smallint,
  reset_password character varying(36),
  address character varying(255),
  CONSTRAINT nav_user_id_pk PRIMARY KEY (_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.nav_user
  OWNER TO admin;

-- Table: public.stock_list_bse

-- DROP TABLE public.stock_list_bse;

CREATE TABLE public.stock_list_bse
(
  security_code integer NOT NULL,
  security_id text NOT NULL,
  security_name text NOT NULL,
  status text NOT NULL,
  security_group text,
  face_value real,
  isin_no text,
  industry text,
  instrument text NOT NULL,
  CONSTRAINT stock_list_bse_pkey PRIMARY KEY (security_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.stock_list_bse
  OWNER TO admin;


-- Table: public.user_stock_profile_daily

-- DROP TABLE public.user_stock_profile_daily;

CREATE TABLE public.user_stock_profile_daily
(
  user_id character varying(36) NOT NULL,
  stock_date date NOT NULL,
  security_count numeric(100,0),
  profile_value double precision,
  units double precision,
  nav double precision,
  _id character varying(36) NOT NULL,
  CONSTRAINT user_stock_profile_daily_pkey PRIMARY KEY (_id),
  CONSTRAINT fk_user_id FOREIGN KEY (user_id)
      REFERENCES public.nav_user (_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.user_stock_profile_daily
  OWNER TO admin;

-- Table: public.user_stocks_trxn

-- DROP TABLE public.user_stocks_trxn;

CREATE TABLE public.user_stocks_trxn
(
  _id character varying(36) NOT NULL,
  user_id character varying(36) NOT NULL,
  security_code integer NOT NULL,
  security_count integer NOT NULL,
  trxn_date date,
  trxn_type character varying(10),
  trxn_flag numeric(1,0),
  CONSTRAINT user_stocks_trxn_pkey PRIMARY KEY (_id),
  CONSTRAINT user_stocks_trxn_security_code_fk FOREIGN KEY (security_code)
      REFERENCES public.stock_list_bse (security_code) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT user_stocks_trxn_user_id_fk FOREIGN KEY (user_id)
      REFERENCES public.nav_user (_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.user_stocks_trxn
  OWNER TO admin;

