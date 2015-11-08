## About
This is an implementation of a psql database with python functions that supports tournaments with a swiss-pairing style.


## How to activate the database
1. From the command line in the home directory, enter "vagrant up" and "vagrant ssh".
2. Navigate to the tournament directory.
3. Enter "psql" to start Postgre SQL.
4. Enter "\i tournament.sql" to import the database schema.
5. Enter "\d" to see all tables and views and "\d [table name]" to see details regarding a specific table.

## How to run test cases
1. From the tournament directory, enter "python tournament_test.py" to run tests.
2. Enter "python tournament_test2.py" to run additional tests.

## Additional files
tournament_test2.py: More test cases for the additional features

## Additional features
1. Handles odd number of players. If odd number of players in a round, one player will be given a bye.
2. Byes are supported. A bye counts as a win, and one player may receive only one bye.
3. Draws are supported. Draw counts as 1 point to both players, while win counts as 2 points, and loss 0.
4. Opponent Match Wins supported. When even number of points, players are then ranked by their Opponent Match Wins.

## Features still in development
1. Supporting more than one tournament in the database.
