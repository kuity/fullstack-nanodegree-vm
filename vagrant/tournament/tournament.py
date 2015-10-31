#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(registration=None):
    """Remove all the match records FROM the database."""

    conn = connect()
    c = conn.cursor()

    if registration==None:
        query = 'DELETE FROM matches *;'
        c.execute(query)
    else:
        query = 'DELETE FROM matches * WHERE registration=%s'
        c.execute(query, [registration,])

    conn.commit()
    conn.close()


def deletePlayers(registration=None):
    """By default, this removes all the player records FROM the database.
    If registration is specified, player records pertaining to a particular
    tournament will be removed instead
    """

    conn = connect()
    c = conn.cursor()

    if registration==None:
        query = 'DELETE FROM players *;'
        c.execute(query)
    else:
        query = 'DELETE FROM players * WHERE registration=%s'
        c.execute(query, [registration,])

    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()

    query = 'SELECT COUNT(id) FROM players WHERE registration=%s;'
    c.execute(query, ['current',])
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
    """Returns a list of the players and their win records, sorted by points.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains 
        (id, name, points, matches, OMW, bye):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the number of points the player has, based on the ranking method
        below
        matches: the number of matches the player has played
        bye: has player received a bye before (T/F)
        OMW: opponent match wins = sum of the defeated opponents' points to
        enable higher-granularity ranking

    Ranking method:
    1. Award 2 points for a win, 1 point for a draw, 0 points for a loss
    2. Group players with the same overall points together
    3. Rank them again, for groups with more than 1 player, calculate the OMW
    """

    conn = connect()
    c = conn.cursor()

    query = 'SELECT id, name, points, wins+losses+draws, bye \
                FROM players \
                WHERE registration=%s \
                ORDER by points desc;'
                
    c.execute(query, ['current',])
    
    # Players are grouped by the total points they have earned so far
    standings = c.fetchall()
    values = set(map(lambda x:x[2], standings))
    groupByPoints = [[y for y in standings if y[2]==x] for x in values]

    standings = []
    for group in groupByPoints:
        groupSorted = []
        print("group is %s") % group
        for player in group:
            query = 'SELECT sum(players.points) \
                        FROM players, matches \
                        WHERE players.id=matches.loser \
                            AND matches.winner=%s \
                            AND matches.draw=FALSE \
                            AND matches.bye=FALSE'
            c.execute(query, [player[0],])
            points = c.fetchone()[0]
            if points == None:
                points = long(0)
            modPlayer = (player[0], player[1], player[2], player[3], player[4],
                         points)
            groupSorted.append(modPlayer)

        print("Before sorting, group is %s") % groupSorted
        groupSorted.sort(key=lambda tup: tup[5], reverse=True)
        print("After sorting, group is %s") % groupSorted
        standings.extend(groupSorted)

    conn.close()

    print("standings are %s") % groupSorted
    return standings



def reportMatch(winner, loser, draw=False, bye=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      bye: if bye is true, player id=winner=loser
      draw: if draw is true, 'winner' and 'loser' actually got a draw
    """

    conn = connect()
    c = conn.cursor()

    if bye == True:
        assert winner == loser, "Only one player can receive a bye in a single match"
        assert draw == false, "There can't be a bye and a draw in the same match"
        query = 'SELECT bye FROM players where id=%s;'
        c.execute(query, [winner,])
        assert c.fetchone() == false, "Each player can only receive one bye in one tournament"
        query = 'INSERT into matches VALUES (%s, -1, FALSE, TRUE);'
        c.execute(query, [winner,])
        query = 'UPDATE players \
                    SET wins=wins+1, points=points+2 \
                    WHERE id=%s;'
        c.execute(query, [winner,])

    elif draw == True:
        assert winner != loser, "Two distinct players are required for a draw"
        query = 'INSERT into matches VALUES (%s, %s, TRUE);'
        c.execute(query, [winner, loser])
        query = 'UPDATE players \
                    SET draws=draws+1, points=points+1 \
                    WHERE id=%s OR id=%s;'
        c.execute(query, [winner, loser])

    else:
        assert winner != loser, "Two distinct players are required for a normal match"
        query = 'INSERT into matches VALUES (%s, %s);'
        c.execute(query, [winner, loser])
        query = 'UPDATE players \
                    SET wins=wins+1, points=points+2 \
                    WHERE id=%s;'
        c.execute(query, [winner,])
        query = 'UPDATE players \
                    SET losses=losses+1 \
                    WHERE id=%s;'
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

    Additional:
    If there are an odd number of players in a given round, award a bye to the
    lowest-ranked player without a bye.
    To award a bye, simply set id1=id2 and name1=name2
    """

    standings = playerStandings()
    pairings = []

    # Determine if there's odd number of players; if there is, find someone to
    # give a bye to
    if len(standings)%2 != 0:
        for i in range(len(standings)):
            player = standings[i]
            if player[4] == False:
                pairings.append(player[0], player[1], player[0], player[1])
            standings.pop(i)
            break
    
    # At this point there must be an even number of players left
    # Simply pair them as per usual
    i = 0
    while i < len(standings):
        pairings.append((standings[i][0], standings[i][1],
                         standings[i+1][0], standings[i+1][1]));
        i += 2
    
    return pairings

def completeTournament(tournyName):
    """Updates database accordingly when a tournament has been completed, 
    setting the 'registration' field of each player to 
    """

    conn = connect()
    c = conn.cursor()

    query = 'UPDATE matches SET registration=%s WHERE registration=%s;'
    c.execute(query, [tournyName, 'current'])
    query = 'UPDATE players SET registration=%s WHERE registration=%s;'
    c.execute(query, [tournyName, 'current'])
    