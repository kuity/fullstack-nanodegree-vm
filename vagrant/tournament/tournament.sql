-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;
CREATE TABLE players (
    id serial NOT NULL,
    name varchar(50) NOT NULL,
    wins int DEFAULT 0,
    losses int DEFAULT 0,
    PRIMARY KEY(id)
);
CREATE TABLE matches (
    winner int NOT NULL,
    loser int NOT NULL,
    FOREIGN KEY(winner) REFERENCES players (id),
    FOREIGN KEY(loser) REFERENCES players (id),
    CHECK (loser!=winner)
);
ALTER SEQUENCE players_id_seq RESTART WITH 1;