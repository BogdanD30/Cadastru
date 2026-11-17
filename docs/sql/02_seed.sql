--
-- PostgreSQL database dump
--

\restrict I1cuSVksg1fL7WX5iEQdEy5sRGQyMO4g4lALEHJi9oLMd1V2QWNNqGlTd9iS6uV

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
-- Data for Name: building_type; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.building_type (id, name) OVERRIDING SYSTEM VALUE VALUES (1, 'House');
INSERT INTO public.building_type (id, name) OVERRIDING SYSTEM VALUE VALUES (2, 'Apartment block');
INSERT INTO public.building_type (id, name) OVERRIDING SYSTEM VALUE VALUES (3, 'Garage');
INSERT INTO public.building_type (id, name) OVERRIDING SYSTEM VALUE VALUES (4, 'Warehouse');
INSERT INTO public.building_type (id, name) OVERRIDING SYSTEM VALUE VALUES (5, 'Office building');
INSERT INTO public.building_type (id, name) OVERRIDING SYSTEM VALUE VALUES (6, 'Shed');


--
-- Data for Name: land_use; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.land_use (id, name) OVERRIDING SYSTEM VALUE VALUES (2, 'Residential');
INSERT INTO public.land_use (id, name) OVERRIDING SYSTEM VALUE VALUES (3, 'Agricultural');
INSERT INTO public.land_use (id, name) OVERRIDING SYSTEM VALUE VALUES (4, 'Commercial');
INSERT INTO public.land_use (id, name) OVERRIDING SYSTEM VALUE VALUES (5, 'Industrial');
INSERT INTO public.land_use (id, name) OVERRIDING SYSTEM VALUE VALUES (6, 'Forest');
INSERT INTO public.land_use (id, name) OVERRIDING SYSTEM VALUE VALUES (7, 'Pasture');


--
-- Name: building_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.building_type_id_seq', 6, true);


--
-- Name: land_use_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.land_use_id_seq', 7, true);


--
-- PostgreSQL database dump complete
--

\unrestrict I1cuSVksg1fL7WX5iEQdEy5sRGQyMO4g4lALEHJi9oLMd1V2QWNNqGlTd9iS6uV

