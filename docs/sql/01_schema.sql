--
-- PostgreSQL database dump
--

\restrict ZKNm5hCxKSKrzNsbBf1MCs4okJZrk0IHMoNIwvZVtJ06yuvBjD4frxRLyGkA08g

-- Dumped from database version 17.11 (Debian 17.11-1.pgdg13+2)
-- Dumped by pg_dump version 17.11 (Debian 17.11-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: btree_gist; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gist WITH SCHEMA public;


--
-- Name: EXTENSION btree_gist; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION btree_gist IS 'support for indexing common datatypes in GiST';


--
-- Name: role; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.role AS ENUM (
    'user',
    'clerk'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.account (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(60) NOT NULL,
    role public.role NOT NULL,
    owner_id integer
);


--
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.account ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.building (
    id integer NOT NULL,
    cadastral_number character varying(50) NOT NULL,
    building_type_id integer NOT NULL,
    size_sqm numeric(10,2) NOT NULL,
    usable_area_sqm numeric(10,2) NOT NULL,
    floors smallint NOT NULL,
    year_built smallint NOT NULL,
    parcel_id integer NOT NULL,
    CONSTRAINT building_floors_check CHECK ((floors >= 1)),
    CONSTRAINT building_size_sqm_check CHECK ((size_sqm > (0)::numeric)),
    CONSTRAINT building_usable_area_sqm_check CHECK ((usable_area_sqm > (0)::numeric)),
    CONSTRAINT building_year_built_check CHECK ((year_built >= 1850)),
    CONSTRAINT valid_size CHECK ((usable_area_sqm <= size_sqm))
);


--
-- Name: building_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.building ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.building_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_ownership; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.building_ownership (
    id integer NOT NULL,
    owner_id integer NOT NULL,
    building_id integer NOT NULL,
    share numeric(5,2) NOT NULL,
    price numeric(14,2) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    CONSTRAINT building_ownership_dates_check CHECK (((end_date IS NULL) OR (end_date >= start_date))),
    CONSTRAINT building_ownership_price_check CHECK ((price >= (0)::numeric)),
    CONSTRAINT building_ownership_share_check CHECK (((share > (0)::numeric) AND (share <= (100)::numeric)))
);


--
-- Name: building_ownership_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.building_ownership ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.building_ownership_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.building_type (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


--
-- Name: building_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.building_type ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.building_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: company; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.company (
    id integer NOT NULL,
    tax_id character varying(50) NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: company_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.company ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: land_use; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.land_use (
    id integer NOT NULL,
    name character varying(60) NOT NULL
);


--
-- Name: land_use_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.land_use ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.land_use_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: owner; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.owner (
    id integer NOT NULL,
    single_user_id integer,
    company_id integer,
    CONSTRAINT owner_check CHECK ((((single_user_id IS NOT NULL) AND (company_id IS NULL)) OR ((single_user_id IS NULL) AND (company_id IS NOT NULL))))
);


--
-- Name: owner_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.owner ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.owner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parcel; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parcel (
    id integer NOT NULL,
    cadastral_number character varying(50) NOT NULL,
    address character varying(50) NOT NULL,
    size_sqm numeric(10,2) NOT NULL,
    land_use_id integer NOT NULL,
    CONSTRAINT parcel_size_sqm_check CHECK ((size_sqm > (0)::numeric))
);


--
-- Name: parcel_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.parcel ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.parcel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parcel_ownership; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parcel_ownership (
    id integer NOT NULL,
    owner_id integer NOT NULL,
    parcel_id integer NOT NULL,
    share numeric(5,2) NOT NULL,
    price numeric(14,2) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    CONSTRAINT parcel_ownership_dates_check CHECK (((end_date IS NULL) OR (end_date >= start_date))),
    CONSTRAINT parcel_ownership_price_check CHECK ((price >= (0)::numeric)),
    CONSTRAINT parcel_ownership_share_check CHECK (((share > (0)::numeric) AND (share <= (100)::numeric)))
);


--
-- Name: parcel_ownership_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.parcel_ownership ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.parcel_ownership_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: single_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.single_user (
    id integer NOT NULL,
    cnp character varying(13) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    phone character varying(20),
    CONSTRAINT valid_cnp CHECK ((length((cnp)::text) = 13))
);


--
-- Name: single_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.single_user ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.single_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: account account_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_email_key UNIQUE (email);


--
-- Name: account account_owner_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_owner_id_key UNIQUE (owner_id);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- Name: building building_cadastral_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_cadastral_number_key UNIQUE (cadastral_number);


--
-- Name: building_ownership building_ownership_no_overlap_excl; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_ownership
    ADD CONSTRAINT building_ownership_no_overlap_excl EXCLUDE USING gist (owner_id WITH =, building_id WITH =, daterange(start_date, end_date, '[]'::text) WITH &&);


--
-- Name: building_ownership building_ownership_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_ownership
    ADD CONSTRAINT building_ownership_pkey PRIMARY KEY (id);


--
-- Name: building building_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_pkey PRIMARY KEY (id);


--
-- Name: building_type building_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_type
    ADD CONSTRAINT building_type_name_key UNIQUE (name);


--
-- Name: building_type building_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_type
    ADD CONSTRAINT building_type_pkey PRIMARY KEY (id);


--
-- Name: single_user cnp; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.single_user
    ADD CONSTRAINT cnp UNIQUE (cnp);


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- Name: land_use land_use_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.land_use
    ADD CONSTRAINT land_use_name_key UNIQUE (name);


--
-- Name: land_use land_use_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.land_use
    ADD CONSTRAINT land_use_pkey PRIMARY KEY (id);


--
-- Name: owner owner_company_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.owner
    ADD CONSTRAINT owner_company_id_key UNIQUE (company_id);


--
-- Name: owner owner_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.owner
    ADD CONSTRAINT owner_pkey PRIMARY KEY (id);


--
-- Name: owner owner_single_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.owner
    ADD CONSTRAINT owner_single_user_id_key UNIQUE (single_user_id);


--
-- Name: parcel parcel_cadastral_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcel
    ADD CONSTRAINT parcel_cadastral_number_key UNIQUE (cadastral_number);


--
-- Name: parcel_ownership parcel_ownership_no_overlap_excl; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcel_ownership
    ADD CONSTRAINT parcel_ownership_no_overlap_excl EXCLUDE USING gist (owner_id WITH =, parcel_id WITH =, daterange(start_date, end_date, '[]'::text) WITH &&);


--
-- Name: parcel_ownership parcel_ownership_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcel_ownership
    ADD CONSTRAINT parcel_ownership_pkey PRIMARY KEY (id);


--
-- Name: parcel parcel_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcel
    ADD CONSTRAINT parcel_pkey PRIMARY KEY (id);


--
-- Name: single_user single_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.single_user
    ADD CONSTRAINT single_user_pkey PRIMARY KEY (id);


--
-- Name: company tax_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT tax_id UNIQUE (tax_id);


--
-- Name: idx_building_building_type_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_building_building_type_id ON public.building USING btree (building_type_id);


--
-- Name: idx_building_ownership_building_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_building_ownership_building_id ON public.building_ownership USING btree (building_id);


--
-- Name: idx_building_parcel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_building_parcel_id ON public.building USING btree (parcel_id);


--
-- Name: idx_parcel_land_use_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_parcel_land_use_id ON public.parcel USING btree (land_use_id);


--
-- Name: idx_parcel_ownership_parcel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_parcel_ownership_parcel_id ON public.parcel_ownership USING btree (parcel_id);


--
-- Name: account account_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.owner(id) ON DELETE SET NULL;


--
-- Name: building building_building_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_building_type_id_fkey FOREIGN KEY (building_type_id) REFERENCES public.building_type(id);


--
-- Name: building_ownership building_ownership_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_ownership
    ADD CONSTRAINT building_ownership_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.building(id) ON DELETE RESTRICT;


--
-- Name: building_ownership building_ownership_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_ownership
    ADD CONSTRAINT building_ownership_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.owner(id) ON DELETE RESTRICT;


--
-- Name: building building_parcel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_parcel_id_fkey FOREIGN KEY (parcel_id) REFERENCES public.parcel(id);


--
-- Name: owner owner_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.owner
    ADD CONSTRAINT owner_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(id);


--
-- Name: owner owner_single_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.owner
    ADD CONSTRAINT owner_single_user_id_fkey FOREIGN KEY (single_user_id) REFERENCES public.single_user(id);


--
-- Name: parcel parcel_land_use_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcel
    ADD CONSTRAINT parcel_land_use_id_fkey FOREIGN KEY (land_use_id) REFERENCES public.land_use(id);


--
-- Name: parcel_ownership parcel_ownership_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcel_ownership
    ADD CONSTRAINT parcel_ownership_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.owner(id) ON DELETE RESTRICT;


--
-- Name: parcel_ownership parcel_ownership_parcel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcel_ownership
    ADD CONSTRAINT parcel_ownership_parcel_id_fkey FOREIGN KEY (parcel_id) REFERENCES public.parcel(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict ZKNm5hCxKSKrzNsbBf1MCs4okJZrk0IHMoNIwvZVtJ06yuvBjD4frxRLyGkA08g

