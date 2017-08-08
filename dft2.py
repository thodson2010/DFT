#DFT 2.0 Digging for Treasure
#4.26.17
#Tim Hodson
import random
import getpass
import math
from pygame import mixer
import sqlite3
import sys
sys.path.append('/home/tim/Documents/pyprojects')
from player import *

'''
Prerequesits: You must install pygame if you want the game to play music. You must also save your music file and assign its location in line 238.
If you don't not want to play music then you can comment out lines 237-239 below.
NOTICE! WHEN YOU ARE CHOOSING TO GO DEEPER OR STAY IN THE CAVE YOU WILL NOT SEE YOUR TEXT INPUT. I am using the getpass library to hide your choice from other players.
'''

def buildDeck(): #Builds a new quest deck. A new deck is used each day of the adventure.
    deckOptions = ["Spider", "Rock Slide", "Lava Flood", "Spike Pit", "Snake", "Treasure Chest", "Golden Idol"]
    deck = []
    for i in range(3):
        deck.append(deckOptions[0])
        deck.append(deckOptions[1])
        deck.append(deckOptions[2])
        deck.append(deckOptions[3])
        deck.append(deckOptions[4])
    for i in range(15):
        deck.append(deckOptions[5])
    for i in range(5):
        deck.append(deckOptions[6])
    random.shuffle(deck)
    return deck

def playersRemain(players):
    count = 0
    for i in range(len(players)):
        if players[i].inCave == True:
            count +=1
    return count

def getTreasure(): #returns a random number between 1 and 20 for treasure
    return random.randint(1,21)

def getQuest(players, deck, usedDeck): #Simulates flipping the next card in the deck to see what happens.
    remainingTreasure = 0
    while playersRemain(players) > 0:
        playersLeaving = []
        card = deck.pop(0) #cards are already shuffled
        usedDeck.append(card)
        print
        print "****************************************************************************"
        print "As you enter the cavern, you encounter a", card,
        if card == ("Treasure Chest"):
            treasure = getTreasure()
            print "with",treasure, "gold coins!"
            print "****************************************************************************"
            for i in range(treasure):
                print "0",
            print
            for i in range(len(players)):
                if (players[i].inCave == True):
                    addCoins(players[i], int(treasure/(playersRemain(players))))
                    print "" + str(players[i].name) + " "+  str(players[i].coins)
            remainingTreasure = remainingTreasure + treasure % playersRemain(players)
            print "The current bounty is", remainingTreasure, "gold coins!"
        elif card == "Golden Idol":
            remainingTreasure +=5
            print
            print "5 coins have been added to the bounty."
            print "The current bounty is", remainingTreasure, "gold coins!"
            print "****************************************************************************"
        else:
            numTrap = usedDeck.count(card)
            if numTrap < 3:
                print
                print "You have encountered", numTrap, card, "so far."
                print "****************************************************************************"
            else:
                print
                print "Oh no! That's 3 "+ str(card) + "s you have encountered! You lose all of your coins! "
                print
                print "                     ********      " #Prints a spooky skeleton.
                print "                    **********     "
                print "                   ***  **  ***     "
                print "                    **********     "
                print "                     ********       "
                print "                     ** ** **      "
                print "                     ** ** **      "
                print
                print "****************************************************************************"
                for i in range(len(players)):
                    if players[i].inCave == True:
                        resetCoins(players[i])
                        changeStatus(players[i])
                        return
        for i in range(len(players)):
            if players[i].inCave == True:
                if players[i].pType == "Human":
                    print
                    print players[i].name, "would you like to go deeper into the cave or leave?"
                    goDeeper(players[i])
                    if getStatus(players[i]) == False:
                        storeCoins(players[i])
                        playersLeaving.append(players[i])
                else:
                    if aiAlgor(deck, players[i]) == False:
                        storeCoins(players[i])
                        changeStatus(players[i])
        if len(playersLeaving) >0:
            pBounty = remainingTreasure / len(playersLeaving)
            remainder = remainingTreasure % len(playersLeaving)
            remainingTreasure = remainder
        for i in range(len(playersLeaving)):
            addBank(players[i], pBounty)
            print players[i].name, "picked up", str(pBounty), "coins on their way out!"

        if playersRemain(players) == 0:
            return

def goDeeper(player): #ATTENTION! This uses the getpass library which hides your text input from other players.
    choice = getpass.getpass("Type 'd' to go deeper, or 'l' to leave. You will not see your keystrokes.")
    print
    if choice in ["l", "L"]:
        player.inCave = False
    else:
        player.inCave = True
    return player.inCave

def aiAlgor(deck, aiPlayer): #Determines if the AI player will stay in the cave or leave.
    odds = getOdds(deck)
    threshold = 0.0
    if aiPlayer.name == "Simple Simon":
        threshold = 0.05 #Easy AI Player leaves earlier and doesn't press his luck as much as hard AI.
    else:
        threshold = 0.10
    if odds >= threshold:
        return False #if there is a 1 in 10 odds of losing, computer leaves the cave
    else:
        return True

def getOdds(deck): #calculates the odds of the remaining deck for the AI algorithm
    odds = 0.0
    spiderCount = deck.count("Spider")
    rockCount = deck.count("Rock Slide")
    lavaCount = deck.count("Lava Flood")
    spikeCount = deck.count("Spike Pit")
    snakeCount = deck.count("Snake")
    oddsDeck = [spiderCount, rockCount, lavaCount, spikeCount, snakeCount]
    for i in range(len(oddsDeck)):
        if oddsDeck[i] == 1:
            odds += (1.0/len(deck))
    return odds

def newDay(players, day): #Starts a new day. Switches the boolean inCave for each player and builds a new deck.
    deck = buildDeck()
    usedDeck = []
    for i in range(len(players)):
        changeStatus(players[i]) #resets each player inCave status to True
    getQuest(players, deck, usedDeck)
    print
    print "******************"
    print "** End of day", day, "**"
    print "******************"
    if day == 5: #game ends on day 5
        for i in range(len(players)):
            print players[i].name, players[i].bank

def addPlayers():
    players = []
    numPlayers = 0
    while numPlayers < 1:
        tempVariable = input('How many players? ')
        numPlayers = tempVariable
    print
    for i in range(numPlayers):
        name = raw_input("Enter the name of Player "+ str(i+1) +": ")
        players.append(new_player(name, 0, 0, False, "Human"))
        print name, "has entered the game."
    print
    aiP = raw_input("Would you like an AI Player? [Y/N] ")
    if aiP in ["y", "Y", "YES", "yes"]:
        aiDifficulty = raw_input("Easy or Hard Difficulty for AI? [E/H] ")
        if aiDifficulty in ["e", "E", "easy", "EASY", "Easy"]:
            players.append(new_player("Simple Simon", 0, 0, False, "AI"))
            print "Simple Simon has entered the game."
        else:
            players.append(new_player("AI-Tron-4000", 0, 0, False, "AI"))
            print "AI-Tron-4000 has entered the game."
    return players

def newGame(): #Creates a new game
    database_file = "score_db.db"
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    print "++ High Scores ++"
    print " Rank  Name  Score"
    counter = 1
    for row in c.execute("SELECT * FROM high_scores ORDER BY score DESC LIMIT 10"): #Displays the top 10 high scores in descending order
        if counter == 10: #print formatting to make things pretty
            print " ", counter, " ", row[1]," ", row[2]
        else:
            print " ", counter, "  ", row[1]," ", row[2]
        counter +=1
    print
    players = addPlayers()
    for i in range(1,6,1):
        newDay(players, i)
    mostCoins = 0
    windex = -1 #winning...index...get it... WINDEX
    for i in range(len(players)):
        if players[i].bank > mostCoins:
            mostCoins = players[i].bank
            windex = i
    if windex == -1:
        print "Tie Game"
    else:
        print "The winner is:", players[windex].name, "with", players[windex].bank, "gold coins!"
        winnerName = players[windex].name[:3]
        winnerScore = players[windex].bank
        winner = [(winnerName, winnerScore)]
        c.executemany("INSERT INTO high_scores(user, score) VALUES (?,?)", winner) #Stores the winner in the high score database
        print "Your score has been captured in the hall of fame!"
        conn.commit() #commits the changes to the db
        conn.close() #closes the db connection
    print

def playAgain(): #asks the player if they would like to play another game. Resets everything.
    print
    userInput = raw_input("Would you like to play again? [y/n] ")
    print
    if userInput in ['y','Y','Yes','YES']:
        return True
    else:
        return False

mixer.init()
mixer.music.load('/home/tim/Documents/Python/dft/ae2.mp3') #Put MP3 directory here!
mixer.music.play()
playagain = True
while playagain == True:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Welcome to a new game! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Behold the Caves of Allijada! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ The caves are deep and full of ancient treasures. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "~~~~~~~~ But be warned... the Caves of Allijada also hold ancient beasts and traps to protect it's bounty. ~~~~~~~~~"
    print "~~~ You have 5 days to recover the treasure, how much loot can you retrieve before falling victim to it's traps? ~~~"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print
    newGame()
    playagain = playAgain() #Calls the function to check if the user wants to play a new game.
print "~~~~Thanks for Playing!~~~~"
print #formatting
