# Additional test cases

from tournament import *

def testOddPlayers():
    """
    Tests a generic scenario where there are odd number of players in a match.
    Correct behavior: Pairing should award bye to one of the players.
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
    pairings = swissPairings()

    # Each pair is mapped to 1 when a bye is given and 0 if it was not.
    # Check the sum to confirm that exactly one bye was given
    checkpairs = sum(map(lambda (x, x1, y, y1): 1 if x==y else 0, pairings))
    if checkpairs!=1:
        raise ValueError(
            "swissPairings() should give 1 player a bye when there is an odd number"
            " of players.")
    print "1. Bye is given to one player when there are odd number of players."


def testOddPlayersWithBye():
    """
    Tests a scenario where there are odd number of players in a match.
    Some of them already have byes.
    Correct behavior: Pairing should not award bye to a players who already
    has a bye.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Alien 1")
    registerPlayer("Alien 2")
    registerPlayer("Alien 3")
    standings = playerStandings()
    [id1, id2, id3] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id3, False, True)
    reportMatch(id2, id3)
    reportMatch(id1, id1, False, True)

    # id1 and id3 have one bye each. In this round, bye should be given to id2
    pairings = swissPairings()
    for pairing in pairings:
        if pairing[0]!=id2 and pairing[0]==pairing[2]:
            raise ValueError(
                "swissPairings() should not award bye to a player who already"
                "has a bye."
                )
        if pairing[0]==id2 and pairing[2]!=id2:
            raise ValueError(
                "swissPairings() has to award a bye when there is an odd number"
                "of players."
                )
    print "2. Bye is not given to a player who already has a bye."

def testDraw():
    """
    Tests a draw scenario. Assume 4 players, both matches draw
    Correct behavior: Each player should have the same number of points
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Pikachu")
    registerPlayer("Charmander")
    registerPlayer("Bulbasaur")
    registerPlayer("Squirtle")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, True)
    reportMatch(id3, id4, True)
    standings = playerStandings()
    if not (standings[0][2]==standings[1][2]==standings[2][2]==standings[3][2]):
        raise ValueError(
            "Players should have the same number of points after drawing"
            )

    print "3. Draw is recorded properly."

def testPointSystem():
    """
    Tests whether points are being added up properly after matches are recorded.
    Round 1: A win B lose. C draw D draw. E bye.
    Round 2: A win E lose. C win D lose. B bye.
    Round 3: A win C lose. E win B lose. D bye.
    Correct behavior: A-6 points. B-2 points. C-3 points. D-3 points. E-4 points
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Pikachu")
    registerPlayer("Charmander")
    registerPlayer("Bulbasaur")
    registerPlayer("Squirtle")
    registerPlayer("MewTwo")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4, True)
    reportMatch(id5, id5, False, True)
    reportMatch(id1, id5)
    reportMatch(id3, id4)
    reportMatch(id2, id2, False, True)
    reportMatch(id1, id3)
    reportMatch(id5, id2)
    reportMatch(id4, id4, False, True)
    standings = playerStandings()
    if not (standings[0][0]==id2 and standings[0][2]==2 and
            standings[1][0]==id4 and standings[0][2]==2 and
            standings[2][0]==id3 and standings[0][2]==2 and
            standings[3][0]==id5 and standings[0][2]==2 and
            standings[4][0]==id1 and standings[0][2]==2):
        raise ValueError(
            "Points are not tallied correctly."
            )

    print "4. Points are tallied correctly."

def testOMW():
    """
    Test that OMW(opponent match wins) are tallied correctly and players are
    ranked in the order of OMW in the case that they have equal points.
    Round 1: A lose B win. C lose D win.
    Round 2: B draw D draw. A win C lose.
    Points: A-2, B-3, C-0, D-3.
    OMW: B-2, D-0
    Correct behavior: B should be ranked higher with more OMW than D even though
    they have the same points. 
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Pikachu")
    registerPlayer("Charmander")
    registerPlayer("Bulbasaur")
    registerPlayer("Squirtle")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id2, id1)
    reportMatch(id4, id3)
    reportMatch(id2, id4, True)
    reportMatch(id1, id3)
    standings = playerStandings()
    if not (standings[2][0]==id4 and standings[2][5]==0 and
            standings[3][0]==id2 and standings[3][5]==2):
        raise ValueError(
            "OMWs are not tallied and accounted for correctly."
            )

    print "5. OMWs are tallied and accounted for correctly."

def testRegistration():
    """
    Test that tournaments can be archived correctly upon completion.
    Correct behavior:
    1. Player registration status set correctly when tournament completed
    2. Match registration status set correctly when tournament completed
    3. Registration for a new tournament when there are existing tournaments
    in the database works
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Red Ranger")
    registerPlayer("Blue Ranger")
    registerPlayer("Yellow Ranger")
    registerPlayer("Pink Ranger")
    registerPlayer("Green Ranger")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    completeTournament('Battle Royale')
    currentPlayers = countPlayers()
    oldPlayers = countPlayers('Battle Royale')
    if not (currentPlayers==0 and oldPlayers==5):
        raise ValueError(
            "Players' status were not updated correctly when tournament"
            " completes"
            )

    print "6. Keeping of completed tournaments in database is checked."


if __name__ == '__main__':
    testOddPlayers()
    testOddPlayersWithBye()
    testDraw()
    testPointSystem()
    testOMW()
    testRegistration()
    print "Success!  All tests pass!"


