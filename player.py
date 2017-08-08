#Class to hold player information

class Player(object):
    name = ""
    coins = 0
    bank = 0
    inCave = False

    def __init__(self, name, coins, bank, inCave, pType):
        self.name = name
        self.coins = coins
        self.bank = bank
        self.inCave = inCave
        self.pType = pType

    def __help__():
        '''
        This class creates a new player object. Each player has a name, coins on hand(coins), bank, a boolean called inCave, and a player Type (Human or AI).
        '''

def new_player(name, coins, bank, inCave, pType): #creates a new player object
    newPlayer = Player(name, coins, bank, inCave, pType)
    return newPlayer

def addCoins(self, coins): #adds coins to a players inventory
    self.coins += coins

def resetCoins(self): #resets a player's coins to 0
    self.coins = 0

def storeCoins(self): #adds coins from players inventory to bank, and returns 0 (current inventory)
    self.bank = self.bank+self.coins
    self.coins = 0

def addBank(self, amount): #adds coins from leaving cave. Used when there is a remaining bounty
    self.bank = self.bank+amount

def getStatus(self): #checks to see if the current player is in the cave
    return self.inCave

def changeStatus(self): #flips the inCave boolean.
    self.inCave = not(self.inCave)
