import atexit
import sqlite3
import databaseSetup


databaseSetup.setup()
cardsConn = sqlite3.connect('cards.db')
cardsDB = cardsConn.cursor()

# DB setup


def setupPlayers(count):
    for i in range(count):
        cardsDB.execute(
            "INSERT INTO players VALUES (?, 1500, 0)", (i, ))
    cardsConn.commit()

# Getters


def getName(position):
    cardsDB.execute(
        'SELECT name FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    return value[0]


def getPrice(position):
    cardsDB.execute(
        'SELECT price FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    return value[0]


def getHousePrice(position):
    cardsDB.execute(
        'SELECT house_price FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    return value[0]


def getOwner(position):
    cardsDB.execute(
        'SELECT owner FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    return value[0]


def getAccountBalance(player):
    cardsDB.execute(
        'SELECT money FROM players WHERE id=?', (player, ))
    value = cardsDB.fetchone()
    return value[0]


def isBuildUp(position):
    cardsDB.execute(
        'SELECT houses_count FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    count = value[0]
    if(count > 0):
        return 1
    else:
        return 0


def getRent(position):
    cardsDB.execute(
        'SELECT houses_count FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    count = value[0]
    houses = "house_" + str(value[0])

    if(count < 5):
        cardsDB.execute(
            "SELECT "+houses+" FROM streets WHERE position=?", (position, ))
        value = cardsDB.fetchone()
        return value[0]
    elif(count == 5):
        cardsDB.execute(
            "SELECT hotel_price FROM streets WHERE position=?", (position, ))
        value = cardsDB.fetchone()
        return value[0]


def getHousesData(position):
    cardsDB.execute(
        'SELECT house_price, houses_count, hotel_price FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    price = value[0]
    count = value[1]
    hotel_price = value[2]
    return price, count, hotel_price


def getSpaceshipName(position):
    cardsDB.execute(
        'SELECT name FROM spaceships WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    return value[0]


def getSpaceshipOwner(position):
    cardsDB.execute(
        'SELECT owner FROM spaceships WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    return value[0]


def getSpaceshipPrice(position):
    cardsDB.execute(
        'SELECT price FROM spaceships WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    return value[0]


def getTicketPrice(position, owner):
    cardsDB.execute(
        'SELECT count(*) FROM spaceships WHERE owner=?', (owner, ))
    value = cardsDB.fetchone()
    cardsOwned = "spaceship_" + str(value[0])
    cardsDB.execute(
        "SELECT "+cardsOwned+" FROM spaceships WHERE position=?", (position, ))
    value = cardsDB.fetchone()
    return value[0]


def monopolCheck(position, player):
    cardsDB.execute(
        'SELECT kit FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    kit = value[0]
    cardsDB.execute(
        'SELECT count(*) FROM streets WHERE kit=?', (kit, ))
    value = cardsDB.fetchone()
    kitSize = value[0]
    cardsDB.execute(
        'SELECT count(*) FROM streets WHERE kit=? and owner=?', (kit, player, ))
    value = cardsDB.fetchone()
    playerKitCardsCount = value[0]
    if(kitSize == playerKitCardsCount):
        return 1
    else:
        return 0


# DB update functions


def updateAccountBalance(player, amount):
    cardsDB.execute(
        'SELECT money FROM players WHERE id=?', (player, ))
    value = cardsDB.fetchone()
    if(value[0] > amount):
        cardsDB.execute(
            'UPDATE players SET money = money + ? WHERE id=?', (amount, player, ))
        cardsConn.commit()
        return 1
    else:
        return 0


def changeOwner(position, player):
    cardsDB.execute(
        "UPDATE streets SET owner = ? WHERE position=?", (player, position, ))
    cardsConn.commit()


def changeSpaceshipOwner(position, player):
    cardsDB.execute(
        "UPDATE spaceships SET owner = ? WHERE position=?", (player, position, ))
    cardsConn.commit()


def updateHouseCount(position, houses_bought):
    cardsDB.execute(
        "UPDATE streets SET houses_count = houses_count + ? WHERE position=?", (houses_bought, position, ))
    cardsConn.commit()


def clean():
    cardsConn.close()


atexit.register(clean)
