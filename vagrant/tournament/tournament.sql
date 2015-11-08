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
    draws int DEFAULT 0,
    points int DEFAULT 0,
    bye boolean DEFAULT FALSE,
    registration varchar(30) DEFAULT 'current',
    PRIMARY KEY(id)
);

CREATE TABLE matches (
    winner int NOT NULL,
    loser int,
    draw boolean DEFAULT FALSE,
    bye boolean DEFAULT FALSE,
    registration varchar(30) DEFAULT 'current',
    FOREIGN KEY(winner) REFERENCES players (id),
    FOREIGN KEY(loser) REFERENCES players (id),
    CHECK ((loser != winner AND loser > 0 AND winner > 0) OR loser = -1)
);

CREATE VIEW standings AS
SELECT id, name, points, wins+losses+draws, bye
FROM players
WHERE registration = 'current'
ORDER by points;

ALTER SEQUENCE players_id_seq RESTART WITH 1;