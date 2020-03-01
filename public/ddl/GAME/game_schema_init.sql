---------------------
-- SCHEMA GAME DDL --
---------------------


-- ************************************** game.world_parameter
drop table if exists game.world_parameter;

CREATE TABLE game.world_parameter
(
 world_parameter_id    integer NOT NULL GENERATED ALWAYS AS IDENTITY,
 parameter_name        varchar(50) NOT NULL,
 parameter_value       varchar(50) NULL,
 parameter_description varchar(300) NULL,
 CONSTRAINT PK_parameter PRIMARY KEY ( world_parameter_id ),
 CONSTRAINT AK_parameter_name UNIQUE ( parameter_name )
);


-- ************************************** game.entity_status
drop table if exists game.entity_status;

CREATE TABLE game.entity_status
(
 entity_status_id   integer NOT NULL GENERATED BY DEFAULT AS IDENTITY (
 start 1
 ),
 created_date       timestamp NOT NULL,
 modified_date      timestamp NOT NULL,
 status_name        varchar(100) NOT NULL,
 status_description varchar(500) NULL,
 status_type        varchar(100) NULL,
 CONSTRAINT PK_user_status PRIMARY KEY ( entity_status_id ),
 CONSTRAINT AK_entity_status UNIQUE ( status_name )
);

COMMENT ON TABLE game.entity_status IS 'A comprehensive list of statuses that can be applied to users. Includes occupations';


-- ************************************** game.action_type
drop table if exists game.action_type;

CREATE TABLE game.action_type
(
 action_type_id        integer NOT NULL GENERATED ALWAYS AS IDENTITY,
 created_date          timestamp NOT NULL,
 modified_date         timestamp NOT NULL,
 action_name           varchar(100) NOT NULL,
 action_description    varchar(1000) NULL,
 current_action_cost   integer NULL,
 action_scope_modifier integer NULL,
 CONSTRAINT PK_action_type PRIMARY KEY ( action_type_id ),
 CONSTRAINT AK_action_type UNIQUE ( action_name )
);

COMMENT ON TABLE game.action_type IS 'This table records the types of actions that users can do. This is what displays in twitch. It also records the current cost of said action.';

COMMENT ON COLUMN game.action_type.action_scope_modifier IS 'When the action is picked, it uses the modifier number as the weight. And anything with a higher value is a N out of P situation. So a scope of 10 will have a 10 out of 500 chance of activating a vocation change';


-- ************************************** game.bot_registration
drop table if exists game.bot_registration;

CREATE TABLE game.bot_registration
(
 bot_registration_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
 created_date        timestamp NOT NULL,
 modified_date       timestamp NOT NULL,
 bot_status_id       integer NOT NULL,
 bot_name            varchar(200) NOT NULL,
 bot_description     varchar(500) NULL,
 CONSTRAINT PK_bot_registration PRIMARY KEY ( bot_registration_id ),
 CONSTRAINT AK_bot_registraton UNIQUE ( bot_name )
 --CONSTRAINT FK_bot_registration_bot_status_id FOREIGN KEY ( bot_status_id ) REFERENCES game.entity_status ( entity_status_id )
);

CREATE INDEX FKidx_bot_registration_bot_status_id ON game.bot_registration
(
 bot_status_id
);


-- ************************************** game.effect
drop table if exists game.effect;

CREATE TABLE game.effect
(
 effect_id           integer NOT NULL GENERATED ALWAYS AS IDENTITY (
 start 1
 ),
 created_date        timestamp NOT NULL,
 modified_date       timestamp NOT NULL,
 effect_status_id    integer NOT NULL,
 effect_name         varchar(100) NOT NULL,
 effect_type         varchar(50) NULL,
 effect_description  varchar(500) NULL,
 effect_readout_text varchar(500) NULL,
 is_order_aligned    integer NULL,
 effect_rarity       integer NULL,
 population_min      integer NULL,
 population_max      integer NULL,
 effect_base_amount  integer NULL,
 effect_modifier     integer NULL,
 CONSTRAINT PK_effect PRIMARY KEY ( effect_id )
 --CONSTRAINT FK_effect_effect_status_id FOREIGN KEY ( effect_status_id ) REFERENCES game.entity_status ( entity_status_id )
);

CREATE INDEX FKidx_effect_effect_status_id ON game.effect
(
 effect_status_id
);

COMMENT ON TABLE game.effect IS 'Table of effects to be implemented. Largely flavor text, this table is used to track all the different effects.';

COMMENT ON COLUMN game.effect.effect_rarity IS 'An inverse weight given to all actions that meet the criteria. more weight = more rare';
COMMENT ON COLUMN game.effect.effect_modifier IS 'Effect will randomly do plus or minus this amount, but will always stay at 1 or higher.';


-- ************************************** game.effect_type
drop table if exists game.effect_type;

CREATE TABLE game.effect_type
(
 effect_type_id          integer NOT NULL GENERATED ALWAYS AS IDENTITY (
 start 1
 ),
 created_date            timestamp NOT NULL,
 modified_date           timestamp NOT NULL,
 effect_type_name        varchar(100) NOT NULL,
 effect_type_description varchar(500) NULL,
 effect_type_status_id   integer NOT NULL,
 CONSTRAINT PK_effect_type PRIMARY KEY ( effect_type_id )
-- CONSTRAINT FK_effect_type_effect_type_status_id FOREIGN KEY ( effect_type_status_id ) REFERENCES game.entity_status ( entity_status_id )
);

CREATE INDEX FKidx_effect_type_effect_type_status_id ON game.effect_type
(
 effect_type_status_id
);


-- ************************************** game.channel_registration
drop table if exists game.channel_registration;

CREATE TABLE game.channel_registration
(
 channel_registration_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (
 start 1
 ),
 created_date            timestamp NOT NULL,
 modified_date           timestamp NOT NULL,
 channel_status_id       integer NOT NULL,
 channel_name            varchar(50) NOT NULL,
 channel_description     varchar(1000) NULL,
 channel_url             varchar(150) NULL,
 CONSTRAINT PK_channel_registration PRIMARY KEY ( channel_registration_id ),
 CONSTRAINT AK_channel_registration UNIQUE ( channel_name )
 --CONSTRAINT FK_channel_registration_channel_status_id FOREIGN KEY ( channel_status_id ) REFERENCES game.entity_status ( entity_status_id )
);

CREATE INDEX FKidx_channel_registration_channel_status_id ON game.channel_registration
(
 channel_status_id
);


-- ************************************** population_threshold
drop table if exists game.population_threshold;

CREATE TABLE game.population_threshold
(
 population_threshold_id    integer NOT NULL GENERATED ALWAYS AS IDENTITY (
 start 1
 ),
 created_date               timestamp NOT NULL,
 modified_date              timestamp NOT NULL,
 threshold_name             varchar(100) NOT NULL,
 population_threshold       bigint NULL,
 cumulative_value_threshold bigint NULL,
 cumulative_chaos_threshold bigint NULL,
 cumulative_order_threshold bigint NULL,
 CONSTRAINT PK_population_hierarchy PRIMARY KEY ( population_threshold_id )
);


-- ************************************** vocation
drop table if exists game.vocation;

CREATE TABLE game.vocation
(
 vocation_id                  integer NOT NULL GENERATED ALWAYS AS IDENTITY (
 start 1
 ),
 created_date                 timestamp NOT NULL,
 modified_date                timestamp NOT NULL,
 vocation_status_id           integer NOT NULL,
 vocation_name                varchar(100) NOT NULL,
 vocation_category            varchar(100) NULL,
 vocation_base_chaos_modifier integer NULL,
 vocation_base_order_modifier integer NULL,
 vocation_description         varchar(300) NULL,
 vocation_enrolment_text      varchar(300) NULL,
 minimum_population           integer NULL,
 maximum_population           integer NULL,
 minimum_global_value         integer NULL,
 maximum_global_value         integer NULL,
 CONSTRAINT PK_player_vocation PRIMARY KEY ( vocation_id )
 --CONSTRAINT FK_vocation_vocation_status_id FOREIGN KEY ( vocation_status_id ) REFERENCES game.entity_status ( entity_status_id )
);

CREATE INDEX FKidx_vocation_vocation_status_id ON game.vocation
(
 vocation_status_id
);


-- ************************************** game.player_registration
drop table if exists game.player_registration;

CREATE TABLE game.player_registration
(
 player_registration_id     integer NOT NULL GENERATED ALWAYS AS IDENTITY,
 created_date               timestamp NOT NULL,
 modified_date              timestamp NOT NULL,
 player_current_status_id   integer NOT NULL,
 registered_by_bot_id       integer NOT NULL,
 registered_via_channel_id  integer NOT NULL,
 player_current_vocation_id integer NOT NULL,
 player_name                varchar(200) NOT NULL,
 is_deleted                 integer NULL,
 deleted_date               timestamp NULL,
 current_occupation_count   integer NULL,
 active_chaos_modifier      integer NULL,
 active_order_modifier      integer NULL,
 current_player_chaos       bigint NULL,
 current_player_order       bigint NULL,
 CONSTRAINT PK_user_registration PRIMARY KEY ( player_registration_id )
 --CONSTRAINT FK_player_registration_player_current_status_id FOREIGN KEY ( player_current_status_id ) REFERENCES game.entity_status ( entity_status_id ),
 --CONSTRAINT FK_player_registration_player_current_vocation_id FOREIGN KEY ( player_current_vocation_id ) REFERENCES vocation ( vocation_id ),
 --CONSTRAINT FK_player_registration_registered_by_bot_id FOREIGN KEY ( registered_by_bot_id ) REFERENCES game.bot_registration ( bot_registration_id ),
 --CONSTRAINT FK_player_registration_registered_via_channel_id FOREIGN KEY ( registered_via_channel_id ) REFERENCES game.channel_registration ( channel_registration_id )
);

CREATE INDEX FKidx_player_registration_player_current_status_id ON game.player_registration
(
 player_current_status_id
);

CREATE INDEX FKidx_player_registration_player_current_vocation_id ON game.player_registration
(
 player_current_vocation_id
);

CREATE INDEX FKidx_player_registration_registered_by_bot_id ON game.player_registration
(
 registered_by_bot_id
);

CREATE INDEX FKidx_player_registration_registered_via_channel_id ON game.player_registration
(
 registered_via_channel_id
);

COMMENT ON TABLE game.player_registration IS 'Users are registered here. One record per unique user, sort of. Only one active player per user. There can be N deleted ones. deleted and killed are synonymous.';


-- ************************************** game.entity_action
drop table if exists game.entity_action;

CREATE TABLE game.entity_action
(
 entity_action_id        integer NOT NULL GENERATED ALWAYS AS IDENTITY (
 start 1
 ),
 created_date            timestamp NOT NULL,
 modified_date           timestamp NOT NULL,
 channel_registration_id integer NOT NULL,
 action_type_id          integer NOT NULL,
 initiating_player_id    integer NOT NULL,
 effect_id               integer NOT NULL,
 action_status_id        integer NOT NULL,
 executed_by_bot_id      integer NOT NULL,
 action_cost             bigint NULL,
 action_order_value      bigint NULL,
 action_chaos_value      bigint NULL,
 CONSTRAINT PK_user_action PRIMARY KEY ( entity_action_id )
 --CONSTRAINT FK_entity_action_action_status_id FOREIGN KEY ( action_status_id ) REFERENCES game.entity_status ( entity_status_id ),
 --CONSTRAINT FK_entity_action_action_type_id FOREIGN KEY ( action_type_id ) REFERENCES game.action_type ( action_type_id ),
 --CONSTRAINT FK_entity_action_channel_registration_id FOREIGN KEY ( channel_registration_id ) REFERENCES game.channel_registration ( channel_registration_id ),
 --CONSTRAINT FK_entity_action_effect_id FOREIGN KEY ( effect_id ) REFERENCES game.effect ( effect_id ),
 --CONSTRAINT FK_entity_action_executed_by_bot_id FOREIGN KEY ( executed_by_bot_id ) REFERENCES game.bot_registration ( bot_registration_id ),
 --CONSTRAINT FK_entity_action_initiating_player_id FOREIGN KEY ( initiating_player_id ) REFERENCES game.player_registration ( player_registration_id )
);

CREATE INDEX FKidx_entity_action_action_status_id ON game.entity_action
(
 action_status_id
);

CREATE INDEX FKidx_entity_action_action_type_id ON game.entity_action
(
 action_type_id
);

CREATE INDEX FKidx_entity_action_channel_registration_id ON game.entity_action
(
 channel_registration_id
);

CREATE INDEX FKidx_entity_action_effect_id ON game.entity_action
(
 effect_id
);

CREATE INDEX FKidx_entity_action_executed_by_bot_id ON game.entity_action
(
 executed_by_bot_id
);

CREATE INDEX FKidx_entity_action_initiating_player_id ON game.entity_action
(
 initiating_player_id
);

COMMENT ON TABLE game.entity_action IS 'user actions are recorded here. As an insert-only table, an action will be recorded here indicating its successful implementation. Actions may be marked as deleted or statuses altered as necessary.';

