-- BOMTS AI existing PostgreSQL baseline
-- Generated from db/model.json. Apply only to an empty temporary database.
BEGIN;

CREATE TABLE public.ai_reference_briefings (
    id integer NOT NULL,
    query character varying(512),
    clean_title character varying(512) NOT NULL,
    source_url character varying(512) NOT NULL,
    source_name character varying(255),
    topic character varying(100),
    published_at timestamp with time zone,
    collected_at timestamp with time zone DEFAULT now(),
    freshness_status character varying(50),
    korean_summary text,
    key_changes text,
    why_it_matters text,
    dev_ai_application_note text,
    suggested_tasks text,
    risk_or_caution text,
    tags character varying(512),
    provider_used character varying(100),
    quality_score double precision,
    status character varying(50),
    created_at timestamp with time zone DEFAULT now(),
    indexed_at timestamp with time zone,
    document_id integer
);

CREATE TABLE public.ask_logs (
    id integer NOT NULL,
    question text NOT NULL,
    endpoint_type character varying(50) NOT NULL,
    intent character varying(50),
    answer text,
    provider character varying(50),
    model character varying(100),
    latency_ms integer,
    retrieval_count integer,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.ask_source_logs (
    id integer NOT NULL,
    ask_log_id integer NOT NULL,
    document_id integer,
    chunk_id integer,
    title character varying(255),
    content text,
    score double precision,
    source character varying(255)
);

CREATE TABLE public.content_sources (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    base_url character varying(255) NOT NULL,
    source_type character varying(50),
    category character varying(50),
    enabled boolean,
    crawl_interval_hours integer,
    last_crawled_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.crawled_pages (
    id integer NOT NULL,
    source_id integer NOT NULL,
    url character varying(512) NOT NULL,
    title character varying(512),
    content text,
    summary text,
    author character varying(255),
    published_at timestamp with time zone,
    crawled_at timestamp with time zone DEFAULT now(),
    status character varying(50),
    error_message text,
    document_id integer
);

CREATE TABLE public.document_chunks (
    id integer NOT NULL,
    document_id integer NOT NULL,
    chunk_index integer NOT NULL,
    content text NOT NULL,
    char_start integer NOT NULL,
    char_end integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.documents (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    source character varying(255),
    license character varying(255),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);

CREATE TABLE public.feedback_logs (
    id integer NOT NULL,
    ask_log_id integer NOT NULL,
    rating character varying(50) NOT NULL,
    comment text,
    created_at timestamp with time zone DEFAULT now()
);

CREATE SEQUENCE public.ai_reference_briefings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.ai_reference_briefings_id_seq OWNED BY public.ai_reference_briefings.id;

CREATE SEQUENCE public.ask_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.ask_logs_id_seq OWNED BY public.ask_logs.id;

CREATE SEQUENCE public.ask_source_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.ask_source_logs_id_seq OWNED BY public.ask_source_logs.id;

CREATE SEQUENCE public.content_sources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.content_sources_id_seq OWNED BY public.content_sources.id;

CREATE SEQUENCE public.crawled_pages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.crawled_pages_id_seq OWNED BY public.crawled_pages.id;

CREATE SEQUENCE public.document_chunks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.document_chunks_id_seq OWNED BY public.document_chunks.id;

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;

CREATE SEQUENCE public.feedback_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.feedback_logs_id_seq OWNED BY public.feedback_logs.id;

ALTER TABLE ONLY public.ai_reference_briefings ALTER COLUMN id SET DEFAULT nextval('public.ai_reference_briefings_id_seq'::regclass);

ALTER TABLE ONLY public.ask_logs ALTER COLUMN id SET DEFAULT nextval('public.ask_logs_id_seq'::regclass);

ALTER TABLE ONLY public.ask_source_logs ALTER COLUMN id SET DEFAULT nextval('public.ask_source_logs_id_seq'::regclass);

ALTER TABLE ONLY public.content_sources ALTER COLUMN id SET DEFAULT nextval('public.content_sources_id_seq'::regclass);

ALTER TABLE ONLY public.crawled_pages ALTER COLUMN id SET DEFAULT nextval('public.crawled_pages_id_seq'::regclass);

ALTER TABLE ONLY public.document_chunks ALTER COLUMN id SET DEFAULT nextval('public.document_chunks_id_seq'::regclass);

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);

ALTER TABLE ONLY public.feedback_logs ALTER COLUMN id SET DEFAULT nextval('public.feedback_logs_id_seq'::regclass);

ALTER TABLE ONLY public.ai_reference_briefings
    ADD CONSTRAINT ai_reference_briefings_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.ask_logs
    ADD CONSTRAINT ask_logs_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.ask_source_logs
    ADD CONSTRAINT ask_source_logs_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.content_sources
    ADD CONSTRAINT content_sources_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.crawled_pages
    ADD CONSTRAINT crawled_pages_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.crawled_pages
    ADD CONSTRAINT crawled_pages_url_key UNIQUE (url);

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.feedback_logs
    ADD CONSTRAINT feedback_logs_pkey PRIMARY KEY (id);

CREATE INDEX ix_ai_reference_briefings_id ON public.ai_reference_briefings USING btree (id);

CREATE INDEX ix_ask_logs_id ON public.ask_logs USING btree (id);

CREATE INDEX ix_ask_source_logs_id ON public.ask_source_logs USING btree (id);

CREATE INDEX ix_content_sources_id ON public.content_sources USING btree (id);

CREATE INDEX ix_crawled_pages_id ON public.crawled_pages USING btree (id);

CREATE INDEX ix_document_chunks_id ON public.document_chunks USING btree (id);

CREATE INDEX ix_documents_id ON public.documents USING btree (id);

CREATE INDEX ix_feedback_logs_id ON public.feedback_logs USING btree (id);

ALTER TABLE ONLY public.ai_reference_briefings
    ADD CONSTRAINT ai_reference_briefings_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE SET NULL;

ALTER TABLE ONLY public.ask_source_logs
    ADD CONSTRAINT ask_source_logs_ask_log_id_fkey FOREIGN KEY (ask_log_id) REFERENCES public.ask_logs(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.crawled_pages
    ADD CONSTRAINT crawled_pages_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE SET NULL;

ALTER TABLE ONLY public.crawled_pages
    ADD CONSTRAINT crawled_pages_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.content_sources(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.feedback_logs
    ADD CONSTRAINT feedback_logs_ask_log_id_fkey FOREIGN KEY (ask_log_id) REFERENCES public.ask_logs(id) ON DELETE CASCADE;

COMMIT;
