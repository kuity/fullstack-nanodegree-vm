# Additional test cases

from tournament import *

def testOddPlayers():
    """
    Tests a scenario where there are odd number of players in a match.

    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Alien 1")
    registerPlayer("Alien 2")
    registerPlayer("Alien 3")
    registerPlayer("Alien 4")
    registerPlayer("Alien 5")
    registerPlayer("Alien 6")
    registerPlayer("Alien 7")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id7, False, True)
