--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: knox_authtoken; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.knox_authtoken (
    digest character varying(128) NOT NULL,
    salt character varying(16) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    expires timestamp with time zone,
    token_key character varying(8) NOT NULL
);


ALTER TABLE public.knox_authtoken OWNER TO postgres;

--
-- Name: mitglieder_aboheft; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_aboheft (
    adresse_ptr_id integer NOT NULL,
    abonummer integer NOT NULL,
    anrede character varying(100),
    titel character varying(100),
    vorname character varying(100),
    nachname character varying(100),
    surname2 character varying(100),
    surname3 character varying(100),
    tel character varying(100),
    fax character varying(100),
    heftanzahl integer,
    beigz character varying(20),
    beidat date,
    storndat date,
    rueckstand double precision NOT NULL,
    gutschrift double precision NOT NULL,
    aboart character varying(2) NOT NULL,
    aboanfang date,
    aboende date,
    anmerkung text,
    kundennummer_id integer NOT NULL
);


ALTER TABLE public.mitglieder_aboheft OWNER TO postgres;

--
-- Name: mitglieder_abonnent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_abonnent (
    id integer NOT NULL,
    kundennummer integer NOT NULL,
    titel character varying(100),
    name character varying(100) NOT NULL,
    name2 character varying(100),
    name3 character varying(100),
    tel character varying(100),
    fax character varying(100),
    uid character varying(20),
    prozent double precision NOT NULL,
    rechnungsanzahl integer NOT NULL,
    dsgvo boolean NOT NULL,
    email character varying(100),
    rechnungsanschrift_id integer NOT NULL
);


ALTER TABLE public.mitglieder_abonnent OWNER TO postgres;

--
-- Name: mitglieder_abonnent_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_abonnent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_abonnent_id_seq OWNER TO postgres;

--
-- Name: mitglieder_abonnent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_abonnent_id_seq OWNED BY public.mitglieder_abonnent.id;


--
-- Name: mitglieder_adresse; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_adresse (
    id integer NOT NULL,
    pobox integer,
    strasse character varying(100),
    plz character varying(20),
    ort character varying(100),
    country_id integer
);


ALTER TABLE public.mitglieder_adresse OWNER TO postgres;

--
-- Name: mitglieder_adresse_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_adresse_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_adresse_id_seq OWNER TO postgres;

--
-- Name: mitglieder_adresse_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_adresse_id_seq OWNED BY public.mitglieder_adresse.id;


--
-- Name: mitglieder_anrede; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_anrede (
    id integer NOT NULL,
    anrede character varying(100) NOT NULL,
    oldid integer NOT NULL
);


ALTER TABLE public.mitglieder_anrede OWNER TO postgres;

--
-- Name: mitglieder_anrede_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_anrede_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_anrede_id_seq OWNER TO postgres;

--
-- Name: mitglieder_anrede_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_anrede_id_seq OWNED BY public.mitglieder_anrede.id;


--
-- Name: mitglieder_beruf; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_beruf (
    id integer NOT NULL,
    beruf character varying(100) NOT NULL,
    bezeichnung character varying(100) NOT NULL,
    oldid integer NOT NULL
);


ALTER TABLE public.mitglieder_beruf OWNER TO postgres;

--
-- Name: mitglieder_beruf_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_beruf_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_beruf_id_seq OWNER TO postgres;

--
-- Name: mitglieder_beruf_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_beruf_id_seq OWNED BY public.mitglieder_beruf.id;


--
-- Name: mitglieder_emailid; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_emailid (
    id integer NOT NULL,
    uuid4 uuid NOT NULL,
    bezahltam timestamp with time zone NOT NULL,
    mitglied_id integer NOT NULL
);


ALTER TABLE public.mitglieder_emailid OWNER TO postgres;

--
-- Name: mitglieder_emailid_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_emailid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_emailid_id_seq OWNER TO postgres;

--
-- Name: mitglieder_emailid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_emailid_id_seq OWNED BY public.mitglieder_emailid.id;


--
-- Name: mitglieder_emailid_offeneposten; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_emailid_offeneposten (
    id integer NOT NULL,
    emailid_id integer NOT NULL,
    offeneposten_id integer NOT NULL
);


ALTER TABLE public.mitglieder_emailid_offeneposten OWNER TO postgres;

--
-- Name: mitglieder_emailid_offeneposten_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_emailid_offeneposten_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_emailid_offeneposten_id_seq OWNER TO postgres;

--
-- Name: mitglieder_emailid_offeneposten_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_emailid_offeneposten_id_seq OWNED BY public.mitglieder_emailid_offeneposten.id;


--
-- Name: mitglieder_institution; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_institution (
    id integer NOT NULL,
    mitgliedsnummer integer NOT NULL,
    institution_name character varying(100),
    name2 character varying(100),
    name3 character varying(100),
    tel character varying(100),
    fax character varying(100),
    email character varying(100),
    homepage character varying(100),
    beigz character varying(20),
    beidat date,
    storndat date,
    versand character varying(20),
    sub character varying(10),
    heftanzahl integer,
    anmerkung text,
    dsgvo boolean NOT NULL,
    berufsgruppe_id integer,
    kostenart_id integer,
    lieferadresse_id integer NOT NULL,
    mitgliedsart_id integer,
    rechnungsadresse_id integer NOT NULL,
    wohnadresse_id integer NOT NULL
);


ALTER TABLE public.mitglieder_institution OWNER TO postgres;

--
-- Name: mitglieder_institution_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_institution_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_institution_id_seq OWNER TO postgres;

--
-- Name: mitglieder_institution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_institution_id_seq OWNED BY public.mitglieder_institution.id;


--
-- Name: mitglieder_institution_vortrag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_institution_vortrag (
    id integer NOT NULL,
    institution_id integer NOT NULL,
    vortragsort_id integer NOT NULL
);


ALTER TABLE public.mitglieder_institution_vortrag OWNER TO postgres;

--
-- Name: mitglieder_institution_vortrag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_institution_vortrag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_institution_vortrag_id_seq OWNER TO postgres;

--
-- Name: mitglieder_institution_vortrag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_institution_vortrag_id_seq OWNED BY public.mitglieder_institution_vortrag.id;


--
-- Name: mitglieder_kosten; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_kosten (
    id integer NOT NULL,
    art character varying(3) NOT NULL,
    bezeichnung character varying(100) NOT NULL,
    betrag double precision
);


ALTER TABLE public.mitglieder_kosten OWNER TO postgres;

--
-- Name: mitglieder_kosten_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_kosten_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_kosten_id_seq OWNER TO postgres;

--
-- Name: mitglieder_kosten_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_kosten_id_seq OWNED BY public.mitglieder_kosten.id;


--
-- Name: mitglieder_land; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_land (
    id integer NOT NULL,
    land character varying(100) NOT NULL,
    iso character varying(4) NOT NULL,
    "EU" boolean NOT NULL,
    oldid integer NOT NULL
);


ALTER TABLE public.mitglieder_land OWNER TO postgres;

--
-- Name: mitglieder_land_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_land_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_land_id_seq OWNER TO postgres;

--
-- Name: mitglieder_land_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_land_id_seq OWNED BY public.mitglieder_land.id;


--
-- Name: mitglieder_mitgliedsart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_mitgliedsart (
    id integer NOT NULL,
    mitart character varying(3) NOT NULL,
    bezeichnung character varying(100) NOT NULL,
    anmerkung character varying(1000) NOT NULL
);


ALTER TABLE public.mitglieder_mitgliedsart OWNER TO postgres;

--
-- Name: mitglieder_mitgliedsart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_mitgliedsart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_mitgliedsart_id_seq OWNER TO postgres;

--
-- Name: mitglieder_mitgliedsart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_mitgliedsart_id_seq OWNED BY public.mitglieder_mitgliedsart.id;


--
-- Name: mitglieder_offeneposten; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_offeneposten (
    id integer NOT NULL,
    erstellt timestamp with time zone NOT NULL,
    bezahltam timestamp with time zone,
    offen double precision NOT NULL,
    zahlung double precision,
    bezahlt boolean NOT NULL,
    description character varying(100),
    mitglied_id integer NOT NULL
);


ALTER TABLE public.mitglieder_offeneposten OWNER TO postgres;

--
-- Name: mitglieder_offeneposten_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_offeneposten_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_offeneposten_id_seq OWNER TO postgres;

--
-- Name: mitglieder_offeneposten_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_offeneposten_id_seq OWNED BY public.mitglieder_offeneposten.id;


--
-- Name: mitglieder_passwortlink; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_passwortlink (
    id integer NOT NULL,
    linkvalue character varying(10) NOT NULL,
    date timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.mitglieder_passwortlink OWNER TO postgres;

--
-- Name: mitglieder_passwortlink_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_passwortlink_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_passwortlink_id_seq OWNER TO postgres;

--
-- Name: mitglieder_passwortlink_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_passwortlink_id_seq OWNED BY public.mitglieder_passwortlink.id;


--
-- Name: mitglieder_titel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_titel (
    id integer NOT NULL,
    titel character varying(100) NOT NULL,
    oldid integer NOT NULL
);


ALTER TABLE public.mitglieder_titel OWNER TO postgres;

--
-- Name: mitglieder_titel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_titel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_titel_id_seq OWNER TO postgres;

--
-- Name: mitglieder_titel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_titel_id_seq OWNED BY public.mitglieder_titel.id;


--
-- Name: mitglieder_vereinsmitglied; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_vereinsmitglied (
    mitgliedsnummer integer NOT NULL,
    anrede character varying(100),
    titel character varying(100),
    namenszusatz character varying(100),
    tel character varying(100),
    fax character varying(100),
    beigz character varying(20),
    beidat date,
    storndat date,
    versand character varying(20),
    gebdat date,
    diplomdat date,
    diplomort character varying(100),
    sub character varying(10),
    vortragold character varying(10),
    heftanzahl integer,
    anmerkung text,
    dsgvo boolean NOT NULL,
    berufsgruppe_id integer,
    kostenart_id integer,
    lieferadresse_id integer,
    mitgliedsart_id integer,
    rechnungsadresse_id integer,
    wohnadresse_id integer,
    user_ptr_id integer NOT NULL
);


ALTER TABLE public.mitglieder_vereinsmitglied OWNER TO postgres;

--
-- Name: mitglieder_vereinsmitglied_vortrag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_vereinsmitglied_vortrag (
    id integer NOT NULL,
    vereinsmitglied_id integer NOT NULL,
    vortragsort_id integer NOT NULL
);


ALTER TABLE public.mitglieder_vereinsmitglied_vortrag OWNER TO postgres;

--
-- Name: mitglieder_vereinsmitglied_vortrag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_vereinsmitglied_vortrag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_vereinsmitglied_vortrag_id_seq OWNER TO postgres;

--
-- Name: mitglieder_vereinsmitglied_vortrag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_vereinsmitglied_vortrag_id_seq OWNED BY public.mitglieder_vereinsmitglied_vortrag.id;


--
-- Name: mitglieder_versand; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_versand (
    id integer NOT NULL,
    versand character varying(3) NOT NULL,
    bezeichnung character varying(100) NOT NULL
);


ALTER TABLE public.mitglieder_versand OWNER TO postgres;

--
-- Name: mitglieder_versand_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_versand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_versand_id_seq OWNER TO postgres;

--
-- Name: mitglieder_versand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_versand_id_seq OWNED BY public.mitglieder_versand.id;


--
-- Name: mitglieder_vortragold; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_vortragold (
    id integer NOT NULL,
    oldid integer NOT NULL,
    "Vortragsort" character varying(10) NOT NULL
);


ALTER TABLE public.mitglieder_vortragold OWNER TO postgres;

--
-- Name: mitglieder_vortragold_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_vortragold_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_vortragold_id_seq OWNER TO postgres;

--
-- Name: mitglieder_vortragold_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_vortragold_id_seq OWNED BY public.mitglieder_vortragold.id;


--
-- Name: mitglieder_vortragsort; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitglieder_vortragsort (
    id integer NOT NULL,
    "Vortragsort" character varying(20) NOT NULL
);


ALTER TABLE public.mitglieder_vortragsort OWNER TO postgres;

--
-- Name: mitglieder_vortragsort_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitglieder_vortragsort_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitglieder_vortragsort_id_seq OWNER TO postgres;

--
-- Name: mitglieder_vortragsort_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitglieder_vortragsort_id_seq OWNED BY public.mitglieder_vortragsort.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: mitglieder_abonnent id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_abonnent ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_abonnent_id_seq'::regclass);


--
-- Name: mitglieder_adresse id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_adresse ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_adresse_id_seq'::regclass);


--
-- Name: mitglieder_anrede id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_anrede ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_anrede_id_seq'::regclass);


--
-- Name: mitglieder_beruf id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_beruf ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_beruf_id_seq'::regclass);


--
-- Name: mitglieder_emailid id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_emailid ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_emailid_id_seq'::regclass);


--
-- Name: mitglieder_emailid_offeneposten id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_emailid_offeneposten ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_emailid_offeneposten_id_seq'::regclass);


--
-- Name: mitglieder_institution id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_institution_id_seq'::regclass);


--
-- Name: mitglieder_institution_vortrag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution_vortrag ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_institution_vortrag_id_seq'::regclass);


--
-- Name: mitglieder_kosten id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_kosten ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_kosten_id_seq'::regclass);


--
-- Name: mitglieder_land id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_land ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_land_id_seq'::regclass);


--
-- Name: mitglieder_mitgliedsart id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_mitgliedsart ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_mitgliedsart_id_seq'::regclass);


--
-- Name: mitglieder_offeneposten id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_offeneposten ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_offeneposten_id_seq'::regclass);


--
-- Name: mitglieder_passwortlink id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_passwortlink ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_passwortlink_id_seq'::regclass);


--
-- Name: mitglieder_titel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_titel ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_titel_id_seq'::regclass);


--
-- Name: mitglieder_vereinsmitglied_vortrag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied_vortrag ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_vereinsmitglied_vortrag_id_seq'::regclass);


--
-- Name: mitglieder_versand id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_versand ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_versand_id_seq'::regclass);


--
-- Name: mitglieder_vortragold id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vortragold ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_vortragold_id_seq'::regclass);


--
-- Name: mitglieder_vortragsort id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vortragsort ALTER COLUMN id SET DEFAULT nextval('public.mitglieder_vortragsort_id_seq'::regclass);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: knox_authtoken knox_authtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knox_authtoken
    ADD CONSTRAINT knox_authtoken_pkey PRIMARY KEY (digest);


--
-- Name: knox_authtoken knox_authtoken_salt_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knox_authtoken
    ADD CONSTRAINT knox_authtoken_salt_key UNIQUE (salt);


--
-- Name: mitglieder_aboheft mitglieder_aboheft_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_aboheft
    ADD CONSTRAINT mitglieder_aboheft_pkey PRIMARY KEY (adresse_ptr_id);


--
-- Name: mitglieder_abonnent mitglieder_abonnent_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_abonnent
    ADD CONSTRAINT mitglieder_abonnent_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_adresse mitglieder_adresse_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_adresse
    ADD CONSTRAINT mitglieder_adresse_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_anrede mitglieder_anrede_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_anrede
    ADD CONSTRAINT mitglieder_anrede_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_beruf mitglieder_beruf_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_beruf
    ADD CONSTRAINT mitglieder_beruf_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_emailid_offeneposten mitglieder_emailid_offen_emailid_id_offeneposten__98724f6e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_emailid_offeneposten
    ADD CONSTRAINT mitglieder_emailid_offen_emailid_id_offeneposten__98724f6e_uniq UNIQUE (emailid_id, offeneposten_id);


--
-- Name: mitglieder_emailid_offeneposten mitglieder_emailid_offeneposten_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_emailid_offeneposten
    ADD CONSTRAINT mitglieder_emailid_offeneposten_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_emailid mitglieder_emailid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_emailid
    ADD CONSTRAINT mitglieder_emailid_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_institution mitglieder_institution_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution
    ADD CONSTRAINT mitglieder_institution_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_institution_vortrag mitglieder_institution_v_institution_id_vortragso_34b9d5e7_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution_vortrag
    ADD CONSTRAINT mitglieder_institution_v_institution_id_vortragso_34b9d5e7_uniq UNIQUE (institution_id, vortragsort_id);


--
-- Name: mitglieder_institution_vortrag mitglieder_institution_vortrag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution_vortrag
    ADD CONSTRAINT mitglieder_institution_vortrag_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_kosten mitglieder_kosten_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_kosten
    ADD CONSTRAINT mitglieder_kosten_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_land mitglieder_land_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_land
    ADD CONSTRAINT mitglieder_land_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_mitgliedsart mitglieder_mitgliedsart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_mitgliedsart
    ADD CONSTRAINT mitglieder_mitgliedsart_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_offeneposten mitglieder_offeneposten_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_offeneposten
    ADD CONSTRAINT mitglieder_offeneposten_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_passwortlink mitglieder_passwortlink_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_passwortlink
    ADD CONSTRAINT mitglieder_passwortlink_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_titel mitglieder_titel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_titel
    ADD CONSTRAINT mitglieder_titel_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_vereinsmitglied_vortrag mitglieder_vereinsmitgli_vereinsmitglied_id_vortr_2615641d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied_vortrag
    ADD CONSTRAINT mitglieder_vereinsmitgli_vereinsmitglied_id_vortr_2615641d_uniq UNIQUE (vereinsmitglied_id, vortragsort_id);


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmitglied_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmitglied_pkey PRIMARY KEY (user_ptr_id);


--
-- Name: mitglieder_vereinsmitglied_vortrag mitglieder_vereinsmitglied_vortrag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied_vortrag
    ADD CONSTRAINT mitglieder_vereinsmitglied_vortrag_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_versand mitglieder_versand_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_versand
    ADD CONSTRAINT mitglieder_versand_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_vortragold mitglieder_vortragold_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vortragold
    ADD CONSTRAINT mitglieder_vortragold_pkey PRIMARY KEY (id);


--
-- Name: mitglieder_vortragsort mitglieder_vortragsort_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vortragsort
    ADD CONSTRAINT mitglieder_vortragsort_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: knox_authtoken_digest_188c7e77_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_digest_188c7e77_like ON public.knox_authtoken USING btree (digest varchar_pattern_ops);


--
-- Name: knox_authtoken_salt_3d9f48ac_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_salt_3d9f48ac_like ON public.knox_authtoken USING btree (salt varchar_pattern_ops);


--
-- Name: knox_authtoken_token_key_8f4f7d47; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_token_key_8f4f7d47 ON public.knox_authtoken USING btree (token_key);


--
-- Name: knox_authtoken_token_key_8f4f7d47_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_token_key_8f4f7d47_like ON public.knox_authtoken USING btree (token_key varchar_pattern_ops);


--
-- Name: knox_authtoken_user_id_e5a5d899; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_user_id_e5a5d899 ON public.knox_authtoken USING btree (user_id);


--
-- Name: mitglieder_aboheft_kundennummer_id_58cf30d7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_aboheft_kundennummer_id_58cf30d7 ON public.mitglieder_aboheft USING btree (kundennummer_id);


--
-- Name: mitglieder_abonnent_rechnungsanschrift_id_0bc73e03; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_abonnent_rechnungsanschrift_id_0bc73e03 ON public.mitglieder_abonnent USING btree (rechnungsanschrift_id);


--
-- Name: mitglieder_adresse_country_id_774c90ba; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_adresse_country_id_774c90ba ON public.mitglieder_adresse USING btree (country_id);


--
-- Name: mitglieder_emailid_mitglied_id_5026d8f9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_emailid_mitglied_id_5026d8f9 ON public.mitglieder_emailid USING btree (mitglied_id);


--
-- Name: mitglieder_emailid_offeneposten_emailid_id_142a9111; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_emailid_offeneposten_emailid_id_142a9111 ON public.mitglieder_emailid_offeneposten USING btree (emailid_id);


--
-- Name: mitglieder_emailid_offeneposten_offeneposten_id_d039a210; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_emailid_offeneposten_offeneposten_id_d039a210 ON public.mitglieder_emailid_offeneposten USING btree (offeneposten_id);


--
-- Name: mitglieder_institution_berufsgruppe_id_9163a4ff; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_berufsgruppe_id_9163a4ff ON public.mitglieder_institution USING btree (berufsgruppe_id);


--
-- Name: mitglieder_institution_kostenart_id_39ec4afe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_kostenart_id_39ec4afe ON public.mitglieder_institution USING btree (kostenart_id);


--
-- Name: mitglieder_institution_lieferadresse_id_d394e878; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_lieferadresse_id_d394e878 ON public.mitglieder_institution USING btree (lieferadresse_id);


--
-- Name: mitglieder_institution_mitgliedsart_id_9e8e35a1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_mitgliedsart_id_9e8e35a1 ON public.mitglieder_institution USING btree (mitgliedsart_id);


--
-- Name: mitglieder_institution_rechnungsadresse_id_e9e381b1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_rechnungsadresse_id_e9e381b1 ON public.mitglieder_institution USING btree (rechnungsadresse_id);


--
-- Name: mitglieder_institution_vortrag_institution_id_0af3f998; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_vortrag_institution_id_0af3f998 ON public.mitglieder_institution_vortrag USING btree (institution_id);


--
-- Name: mitglieder_institution_vortrag_vortragsort_id_71fa2f7d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_vortrag_vortragsort_id_71fa2f7d ON public.mitglieder_institution_vortrag USING btree (vortragsort_id);


--
-- Name: mitglieder_institution_wohnadresse_id_18116694; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_institution_wohnadresse_id_18116694 ON public.mitglieder_institution USING btree (wohnadresse_id);


--
-- Name: mitglieder_offeneposten_mitglied_id_c830f6b0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_offeneposten_mitglied_id_c830f6b0 ON public.mitglieder_offeneposten USING btree (mitglied_id);


--
-- Name: mitglieder_passwortlink_user_id_a99bca03; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_passwortlink_user_id_a99bca03 ON public.mitglieder_passwortlink USING btree (user_id);


--
-- Name: mitglieder_vereinsmitglied_berufsgruppe_id_b09b37b5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_berufsgruppe_id_b09b37b5 ON public.mitglieder_vereinsmitglied USING btree (berufsgruppe_id);


--
-- Name: mitglieder_vereinsmitglied_kostenart_id_b9d1472c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_kostenart_id_b9d1472c ON public.mitglieder_vereinsmitglied USING btree (kostenart_id);


--
-- Name: mitglieder_vereinsmitglied_lieferadresse_id_31015a67; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_lieferadresse_id_31015a67 ON public.mitglieder_vereinsmitglied USING btree (lieferadresse_id);


--
-- Name: mitglieder_vereinsmitglied_mitgliedsart_id_ab366acb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_mitgliedsart_id_ab366acb ON public.mitglieder_vereinsmitglied USING btree (mitgliedsart_id);


--
-- Name: mitglieder_vereinsmitglied_rechnungsadresse_id_c4f6c5ca; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_rechnungsadresse_id_c4f6c5ca ON public.mitglieder_vereinsmitglied USING btree (rechnungsadresse_id);


--
-- Name: mitglieder_vereinsmitglied_vortrag_vereinsmitglied_id_9ae9d0ff; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_vortrag_vereinsmitglied_id_9ae9d0ff ON public.mitglieder_vereinsmitglied_vortrag USING btree (vereinsmitglied_id);


--
-- Name: mitglieder_vereinsmitglied_vortrag_vortragsort_id_5cef7dff; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_vortrag_vortragsort_id_5cef7dff ON public.mitglieder_vereinsmitglied_vortrag USING btree (vortragsort_id);


--
-- Name: mitglieder_vereinsmitglied_wohnadresse_id_3d02df13; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitglieder_vereinsmitglied_wohnadresse_id_3d02df13 ON public.mitglieder_vereinsmitglied USING btree (wohnadresse_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: knox_authtoken knox_authtoken_user_id_e5a5d899_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knox_authtoken
    ADD CONSTRAINT knox_authtoken_user_id_e5a5d899_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_aboheft mitglieder_aboheft_adresse_ptr_id_5a2fa644_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_aboheft
    ADD CONSTRAINT mitglieder_aboheft_adresse_ptr_id_5a2fa644_fk_mitgliede FOREIGN KEY (adresse_ptr_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_aboheft mitglieder_aboheft_kundennummer_id_58cf30d7_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_aboheft
    ADD CONSTRAINT mitglieder_aboheft_kundennummer_id_58cf30d7_fk_mitgliede FOREIGN KEY (kundennummer_id) REFERENCES public.mitglieder_abonnent(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_abonnent mitglieder_abonnent_rechnungsanschrift_i_0bc73e03_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_abonnent
    ADD CONSTRAINT mitglieder_abonnent_rechnungsanschrift_i_0bc73e03_fk_mitgliede FOREIGN KEY (rechnungsanschrift_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_adresse mitglieder_adresse_country_id_774c90ba_fk_mitglieder_land_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_adresse
    ADD CONSTRAINT mitglieder_adresse_country_id_774c90ba_fk_mitglieder_land_id FOREIGN KEY (country_id) REFERENCES public.mitglieder_land(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_emailid_offeneposten mitglieder_emailid_o_emailid_id_142a9111_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_emailid_offeneposten
    ADD CONSTRAINT mitglieder_emailid_o_emailid_id_142a9111_fk_mitgliede FOREIGN KEY (emailid_id) REFERENCES public.mitglieder_emailid(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_emailid_offeneposten mitglieder_emailid_o_offeneposten_id_d039a210_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_emailid_offeneposten
    ADD CONSTRAINT mitglieder_emailid_o_offeneposten_id_d039a210_fk_mitgliede FOREIGN KEY (offeneposten_id) REFERENCES public.mitglieder_offeneposten(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution mitglieder_instituti_berufsgruppe_id_9163a4ff_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution
    ADD CONSTRAINT mitglieder_instituti_berufsgruppe_id_9163a4ff_fk_mitgliede FOREIGN KEY (berufsgruppe_id) REFERENCES public.mitglieder_beruf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution_vortrag mitglieder_instituti_institution_id_0af3f998_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution_vortrag
    ADD CONSTRAINT mitglieder_instituti_institution_id_0af3f998_fk_mitgliede FOREIGN KEY (institution_id) REFERENCES public.mitglieder_institution(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution mitglieder_instituti_kostenart_id_39ec4afe_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution
    ADD CONSTRAINT mitglieder_instituti_kostenart_id_39ec4afe_fk_mitgliede FOREIGN KEY (kostenart_id) REFERENCES public.mitglieder_kosten(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution mitglieder_instituti_lieferadresse_id_d394e878_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution
    ADD CONSTRAINT mitglieder_instituti_lieferadresse_id_d394e878_fk_mitgliede FOREIGN KEY (lieferadresse_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution mitglieder_instituti_mitgliedsart_id_9e8e35a1_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution
    ADD CONSTRAINT mitglieder_instituti_mitgliedsart_id_9e8e35a1_fk_mitgliede FOREIGN KEY (mitgliedsart_id) REFERENCES public.mitglieder_mitgliedsart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution mitglieder_instituti_rechnungsadresse_id_e9e381b1_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution
    ADD CONSTRAINT mitglieder_instituti_rechnungsadresse_id_e9e381b1_fk_mitgliede FOREIGN KEY (rechnungsadresse_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution_vortrag mitglieder_instituti_vortragsort_id_71fa2f7d_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution_vortrag
    ADD CONSTRAINT mitglieder_instituti_vortragsort_id_71fa2f7d_fk_mitgliede FOREIGN KEY (vortragsort_id) REFERENCES public.mitglieder_vortragsort(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_institution mitglieder_instituti_wohnadresse_id_18116694_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_institution
    ADD CONSTRAINT mitglieder_instituti_wohnadresse_id_18116694_fk_mitgliede FOREIGN KEY (wohnadresse_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_passwortlink mitglieder_passwortlink_user_id_a99bca03_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_passwortlink
    ADD CONSTRAINT mitglieder_passwortlink_user_id_a99bca03_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmi_berufsgruppe_id_b09b37b5_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmi_berufsgruppe_id_b09b37b5_fk_mitgliede FOREIGN KEY (berufsgruppe_id) REFERENCES public.mitglieder_beruf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmi_kostenart_id_b9d1472c_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmi_kostenart_id_b9d1472c_fk_mitgliede FOREIGN KEY (kostenart_id) REFERENCES public.mitglieder_kosten(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmi_lieferadresse_id_31015a67_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmi_lieferadresse_id_31015a67_fk_mitgliede FOREIGN KEY (lieferadresse_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmi_mitgliedsart_id_ab366acb_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmi_mitgliedsart_id_ab366acb_fk_mitgliede FOREIGN KEY (mitgliedsart_id) REFERENCES public.mitglieder_mitgliedsart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmi_rechnungsadresse_id_c4f6c5ca_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmi_rechnungsadresse_id_c4f6c5ca_fk_mitgliede FOREIGN KEY (rechnungsadresse_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied_vortrag mitglieder_vereinsmi_vortragsort_id_5cef7dff_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied_vortrag
    ADD CONSTRAINT mitglieder_vereinsmi_vortragsort_id_5cef7dff_fk_mitgliede FOREIGN KEY (vortragsort_id) REFERENCES public.mitglieder_vortragsort(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmi_wohnadresse_id_3d02df13_fk_mitgliede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmi_wohnadresse_id_3d02df13_fk_mitgliede FOREIGN KEY (wohnadresse_id) REFERENCES public.mitglieder_adresse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitglieder_vereinsmitglied mitglieder_vereinsmitglied_user_ptr_id_88321a12_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitglieder_vereinsmitglied
    ADD CONSTRAINT mitglieder_vereinsmitglied_user_ptr_id_88321a12_fk_auth_user_id FOREIGN KEY (user_ptr_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

