-- coding: utf-8 --

begin transaction;

-- Ta tabela będzie zawierała dane o obserwatorach
create table observers (
	id integer not null,
	created timestamp,
	modified timestamp,
	name varchar(60),
	lastname varchar(60),
	nickname varchar(60),
	email varchar(255),
	anonymous boolean default 0,
	openid varchar(255),
	openid_identity varchar(255),
	openid_server varchar(255),
	primary key (id),
	unique (email),
	unique (openid)
);

-- Miejscówki obserwacyjne.
create table locations (
	id integer not null,
	created timestamp,
	modified timestamp,
	name varchar(200),
	latitude float,
	longitude float,
	altitude float,
	googlecode varchar(45),
	lettercode varchar(12),
	primary key (id)
);

-- Recenzje miejscówek.
create table reviews (
	id integer not null,
	created timestamp,
	modified timestamp,
	has_current varchar(12),
	has_caraccess varchar(12),
	has_sleeping varchar(12),
	has_horizon varchar(12),
	comment varchar,
	location_id integer,
	observer_id integer,
	published boolean default 1,
	primary key (id),
	check (has_current in ('free', 'limited', 'none')),
	check (has_caraccess in ('free', 'limited', 'none')),
	check (has_sleeping in ('free', 'limited', 'none')),
	check (has_horizon in ('visible', 'southonly', 'none')),
	foreign key(location_id) references locations (id),
	foreign key(observer_id) references observers (id)
);

-- Obserwacje.
create table observations (
	id integer not null,
	created timestamp,
	modified timestamp,
	date_start datetime,
	date_end datetime,
	cond_clouds_octants integer default -1,
	cond_milkyway varchar(12) default 'unknown',
	location_id integer not null,
	observer_id integer not null,
	published boolean default 1,
	primary key (id),
	check (cond_clouds_octants >= -1 and cond_clouds_octants <= 8),
	check (cond_milkyway in ('yes','no','unknown')),
	foreign key(location_id) references locations (id),
	foreign key(observer_id) references observers (id)
);

-- W dalszej części są tabelki do poszczególnych rodzajów pomiarów.

-- Oceny metodą Bortla.
create table bortle_data (
	id integer not null,
	created timestamp,
	modified timestamp,
	degrees integer,
	comment varchar,
	observation_id integer,
	primary key (id),
	foreign key(observation_id) references observations (id)
);

-- Pomiary z tuby.
create table tube_data (
	id integer not null,
	created timestamp,
	modified timestamp,
	tube_diam float,
	tube_length float,
	tube_type varchar(6),
	tube_glasses boolean,
	data varchar(500),
	num_stars integer,
	comment varchar,
	observation_id integer,
	primary key (id),
	check (tube_glasses in (0, 1)),
	foreign key(observation_id) references observations (id)
);

-- Pomiary z sqm
create table sqm_data (
	id integer not null,
	created timestamp,
	modified timestamp,
	sqm_model varchar(45),
	sqm_serial varchar(45),
	data varchar(500),
	magnitude_z float,
	magnitude_n float,
	magnitude_e float,
	magnitude_s float,
	magnitude_w float,
	comment varchar,
	observation_id integer,
	primary key (id),
	foreign key(observation_id) references observations (id)
);

-- Pomiary z metody meteorowej.
create table meteor_data (
	id integer not null,
	field_nr integer,
	num_stars integer,
	magnitude float,
	comment varchar,
	observation_id integer,
	primary key (id),
	foreign key(observation_id) references observations (id)
);

-- Pomiary z lustrzanek.
create table dslr_data (
	id integer not null,
	created timestamp,
	modified timestamp,
	info_camera varchar(200),
	info_lens varchar(200),
	field_nr integer,
	data varchar(400),
	magnitude float,
	comment varchar,
	observation_id integer,
	primary key (id),
	foreign key(observation_id) references observations (id)
);

commit;
