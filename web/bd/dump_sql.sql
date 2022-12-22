--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Debian 14.5-1.pgdg110+1)
-- Dumped by pg_dump version 14.5 (Debian 14.5-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: horses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horses (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    count_win integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.horses OWNER TO postgres;

--
-- Name: horse_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.horses ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.horse_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: horse_jokey; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horse_jokey (
    id integer NOT NULL,
    id_horse integer NOT NULL,
    id_jokey integer NOT NULL
);


ALTER TABLE public.horse_jokey OWNER TO postgres;

--
-- Name: horse_jokey_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.horse_jokey ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.horse_jokey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: jockeys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jockeys (
    id integer NOT NULL,
    full_name character varying(50) NOT NULL,
    number_of_races character varying(20)
);


ALTER TABLE public.jockeys OWNER TO postgres;

--
-- Name: jokey_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.jockeys ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.jokey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: race_horse; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.race_horse (
    id_race integer NOT NULL,
    name_horse character varying(50) NOT NULL
);


ALTER TABLE public.race_horse OWNER TO postgres;

--
-- Name: race_jockey; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.race_jockey (
    id_race integer NOT NULL,
    name_jockey character varying(50) NOT NULL
);


ALTER TABLE public.race_jockey OWNER TO postgres;

--
-- Name: stat_race; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stat_race (
    id integer NOT NULL,
    date date NOT NULL,
    f_place character varying(50) NOT NULL,
    s_place character varying(50) NOT NULL,
    t_place character varying(50) NOT NULL
);


ALTER TABLE public.stat_race OWNER TO postgres;

--
-- Name: stat_race_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.stat_race ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.stat_race_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: upcoming_races; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.upcoming_races (
    id integer NOT NULL,
    date character(50) NOT NULL
);


ALTER TABLE public.upcoming_races OWNER TO postgres;

--
-- Name: upcoming_races_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.upcoming_races ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.upcoming_races_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    login character varying(40) NOT NULL,
    password character varying(200) NOT NULL,
    role_id integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: horse_jokey; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.horse_jokey (id, id_horse, id_jokey) FROM stdin;
1	1	1
\.


--
-- Data for Name: horses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.horses (id, name, count_win) FROM stdin;
1	Майкл	0
2	Джон	2
3	Хильда	1
\.


--
-- Data for Name: jockeys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jockeys (id, full_name, number_of_races) FROM stdin;
1	Егор	0
2	Максим	3
3	Аркадий Иванович	1
\.


--
-- Data for Name: race_horse; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.race_horse (id_race, name_horse) FROM stdin;
25	Майкл
25	Джон
26	Майкл
26	Хильда
\.


--
-- Data for Name: race_jockey; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.race_jockey (id_race, name_jockey) FROM stdin;
25	Максим
25	Аркадий Иванович
26	Егор
26	Аркадий Иванович
\.


--
-- Data for Name: stat_race; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stat_race (id, date, f_place, s_place, t_place) FROM stdin;
4	2022-10-15	Майкл	Хильда	Джеймс
5	2022-09-23	Хильда	Джеймс	Майкл
\.


--
-- Data for Name: upcoming_races; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.upcoming_races (id, date) FROM stdin;
25	2022-12-29                                        
26	2023-01-11                                        
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, login, password, role_id) FROM stdin;
2	user	pbkdf2:sha256:260000$eb3DxqnYlcTJP7qY$c237fd359a0b3c4574005e2f2f7750bc92a23ee192b66bd39ac5b7151a308d9b	1
1	renat	pbkdf2:sha256:260000$kZJ5OXlZFUmfrWHW$f59f721e7162417cb1c8a1182c5fbd2eec7e720e7915489f122106d762232b77	2
\.


--
-- Name: horse_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horse_id_seq', 3, true);


--
-- Name: horse_jokey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horse_jokey_id_seq', 1, true);


--
-- Name: jokey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.jokey_id_seq', 3, true);


--
-- Name: stat_race_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stat_race_id_seq', 5, true);


--
-- Name: upcoming_races_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.upcoming_races_id_seq', 26, true);


--
-- Name: horses horse_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horses
    ADD CONSTRAINT horse_pkey PRIMARY KEY (id);


--
-- Name: horse_jokey id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horse_jokey
    ADD CONSTRAINT id PRIMARY KEY (id_horse);


--
-- Name: jockeys jokey_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jockeys
    ADD CONSTRAINT jokey_pkey PRIMARY KEY (id);


--
-- Name: race_horse race_horse_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.race_horse
    ADD CONSTRAINT race_horse_pkey PRIMARY KEY (name_horse, id_race);


--
-- Name: race_jockey race_jockey_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.race_jockey
    ADD CONSTRAINT race_jockey_pkey PRIMARY KEY (id_race, name_jockey);


--
-- Name: stat_race stat_race_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stat_race
    ADD CONSTRAINT stat_race_pkey PRIMARY KEY (id);


--
-- Name: upcoming_races upcoming_races_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.upcoming_races
    ADD CONSTRAINT upcoming_races_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: horse_jokey F_H; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horse_jokey
    ADD CONSTRAINT "F_H" FOREIGN KEY (id_horse) REFERENCES public.horses(id);


--
-- Name: horse_jokey F_J; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horse_jokey
    ADD CONSTRAINT "F_J" FOREIGN KEY (id_jokey) REFERENCES public.jockeys(id);


--
-- PostgreSQL database dump complete
--

