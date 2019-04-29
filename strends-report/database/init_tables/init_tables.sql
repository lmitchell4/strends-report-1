CREATE DATABASE rivers;
\c rivers
CREATE SCHEMA cd;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = cd, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE test_rivers (
    id integer NOT NULL,
    rivername character varying(200) NOT NULL,
    region character varying(200) NOT NULL
);

INSERT INTO test_rivers (id, rivername, region) VALUES
(0, 'Sample1', 'A'),
(1, 'Sample2', 'B'),
(2, 'Sample3', 'C'),
(3, 'Sample4', 'D');
