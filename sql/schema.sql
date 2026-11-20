CREATE DATABASE coletas;

------------------------
CREATE EXTENSION postgis;

--------------------------
CREATE TABLE IF NOT EXISTS public.focos_incendios
(
    id serial NOT NULL,
    geom geometry(Point,4674),
    fid bigint,
    datahora character varying(80) COLLATE pg_catalog."default",
    satelite character varying(100) COLLATE pg_catalog."default",
    pais character varying(100) COLLATE pg_catalog."default",
    estado character varying(100) COLLATE pg_catalog."default",
    municipio character varying(100) COLLATE pg_catalog."default",
    bioma character varying(100) COLLATE pg_catalog."default",
    diasemchuv integer,
    precipitac numeric,
    riscofogo numeric,
    frp numeric,
    latitude numeric,
    longitude numeric,
    bioma_id integer,
    municipio_id integer,
    CONSTRAINT focos_incendios_pkey PRIMARY KEY (id)
    )

    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.focos_incendios
    OWNER to postgres;


-- Table: public.municipios

-- DROP TABLE IF EXISTS public.municipios;

CREATE TABLE IF NOT EXISTS public.municipios
(
    id serial NOT NULL,
    geom geometry(MultiPolygon,4674),
    fid bigint,
    cd_mun character varying(7) COLLATE pg_catalog."default",
    nm_mun character varying(100) COLLATE pg_catalog."default",
    cd_rgi character varying(6) COLLATE pg_catalog."default",
    nm_rgi character varying(100) COLLATE pg_catalog."default",
    cd_rgint character varying(4) COLLATE pg_catalog."default",
    nm_rgint character varying(100) COLLATE pg_catalog."default",
    cd_uf character varying(2) COLLATE pg_catalog."default",
    nm_uf character varying(50) COLLATE pg_catalog."default",
    sigla_uf character varying(2) COLLATE pg_catalog."default",
    cd_regiao character varying(1) COLLATE pg_catalog."default",
    nm_regiao character varying(20) COLLATE pg_catalog."default",
    sigla_rg character varying(2) COLLATE pg_catalog."default",
    cd_concurb character varying(7) COLLATE pg_catalog."default",
    nm_concurb character varying(100) COLLATE pg_catalog."default",
    area_km2 double precision,
    CONSTRAINT municipios_pkey PRIMARY KEY (id)
    )

    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.municipios
    OWNER to postgres;


-- Table: public.biomas

-- DROP TABLE IF EXISTS public.biomas;

CREATE TABLE IF NOT EXISTS public.biomas
(
    id serial NOT NULL,
    geom geometry(MultiPolygon,4674),
    fid bigint,
    "CD_BIOMA" character varying(1) COLLATE pg_catalog."default",
    "NM_BIOMA" character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT biomas_pkey PRIMARY KEY (id)
    )

    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.biomas
    OWNER to postgres;

ALTER TABLE IF EXISTS public.focos_incendios
    ADD CONSTRAINT fk_focos_bioma FOREIGN KEY (bioma_id)
    REFERENCES public.biomas (id) MATCH SIMPLE
    ON UPDATE NO ACTION
       ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.focos_incendios
    ADD CONSTRAINT fk_focos_municipio FOREIGN KEY (municipio_id)
    REFERENCES public.municipios (id) MATCH SIMPLE
    ON UPDATE NO ACTION
       ON DELETE NO ACTION;

CREATE INDEX IF NOT EXISTS idx_focos_incendios_geom
    ON public.focos_incendios USING gist
    (geom)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_municipios_geom
    ON public.municipios USING gist
    (geom)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_biomas_geom
    ON public.biomas USING gist
    (geom)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_focos_incendios_bioma_id
    ON public.focos_incendios USING btree
    (bioma_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_focos_incendios_municipio_id
    ON public.focos_incendios USING btree
    (municipio_id ASC NULLS LAST)
    TABLESPACE pg_default;


--- SELECT * FROM biomas;
--- SELECT * FROM municipios;
--- SELECT * FROM focos_incendios;
--- SELECT * FROM public.spatial_ref_sys;



