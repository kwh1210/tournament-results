#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("error connecting to db")
#db is conn cursor is cursor


def deleteMatches():
    """Remove all the match records from the database."""

    #conn = psycopg2.connect("dbname=tournament")
    conn,cursor = connect()
    cursor.execute("truncate matches cascade")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn,cursor = connect()
    cursor.execute("truncate players cascade")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn,cursor = connect()
    cursor.execute("select count(*) as num from players")
    results = cursor.fetchall()
    conn.close()
    #print(results[0][0])
    return results[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn,cursor = connect()
    cursor.execute("insert into players(name) values(%s)",(str(name),))
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

    conn,cursor = connect()
    cursor.execute("select * from standing")
    results = cursor.fetchall()
    conn.close()

    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn,cursor = connect()
    cursor = conn.cursor()
    cursor.execute("insert into matches(winnerid,loserid) values(%s,%s)",(winner,loser))
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

    results = playerStandings()
    swisslist=[]

    for i in range(0,len(results))[::2]:
        tup = (results[i][0],results[i][1],results[i+1][0],results[i+1][1])
        swisslist.append(tup)

    return swisslist







