#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    conn = connect()
    c = conn.cursor()

    query = 'DELETE from matches *;'

    c.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    c = conn.cursor()

    query = 'DELETE from players *;'

    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()

    query = 'SELECT COUNT(id) from players;'
    c.execute(query)
    numPlayers = c.fetchone()[0]
    conn.close()

    # print(numPlayers[0])
    return numPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()

    query = 'INSERT into players(name) VALUES (%s);'    
    c.execute(query, [name])
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()

    query = 'SELECT id, name, wins, wins+losses from players \
            ORDER by wins desc'
    c.execute(query)
    
    standings = c.fetchall()
    conn.close()

    return standings



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()

    query = 'INSERT into matches VALUES (%s, %s);'
    c.execute(query, [winner, loser])
    query = 'UPDATE players SET wins = wins+1 WHERE id=%s'
    c.execute(query, [winner,])
    query = 'UPDATE players SET losses = losses+1 WHERE id=%s'
    c.execute(query, [loser,])
    
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    pairings = []
    i = 0
    while i < len(standings):
        pairings.append((standings[i][0], standings[i][1],
                         standings[i+1][0], standings[i+1][1]));
        i += 2
    
    return pairings