DELETE from matches *;
DELETE from players *;
ALTER SEQUENCE players_id_seq RESTART WITH 1;

INSERT into players(name) VALUES ('John');
INSERT into players(name) VALUES ('Nancy');
INSERT into players(name) VALUES ('Jack');
INSERT into players(name) VALUES ('Anne');

INSERT into matches VALUES (1, 2, 1, 2);
INSERT into matches VALUES (3, 4, 4, 3);
