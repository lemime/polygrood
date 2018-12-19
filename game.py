import sqlite3
import databaseSetup

databaseSetup.setup()
cardsConn = sqlite3.connect('cards.db')
cardsDB = cardsConn.cursor()


def setupPlayers(count):
    for i in range(count):
        cardsDB.execute(
            "INSERT INTO players VALUES (?, 1500, 0)", (i, ))
    cardsConn.commit()

# Database pure functions


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


# Database update functions

def updateAccountBalance(player, amount):
    cardsDB.execute(
        'UPDATE players SET money = money + ? WHERE id=?', (amount, player, ))
    cardsConn.commit()


def changeOwner(position, player):
    cardsDB.execute(
        "UPDATE streets SET owner = ? WHERE position=?", (player, position, ))
    cardsConn.commit()

# Game actions
# returns messege for arduino lcd


def buyOffer(position, player):
    cardsDB.execute(
        'SELECT name, price FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    name = value[0]
    price = value[1]
    return "Czy chcesz kupic " + str(name) + " za " + str(price) + "?/Tak/Nie"


def buyHouseOffer(position, player):
    cardsDB.execute(
        'SELECT house_price, houses_count, hotel_price FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    price = value[0]
    count = value[1]
    hotel_price = value[2]

    if(count < 5):
        message = "Ile domków chcesz postawić? Stan konta: " + \
            str(getAccountBalance(player)) + "/"
        for house in range(0, 4 - count):
            if(house*price < getAccountBalance(player)):
                message = message + str(house) + \
                    " (" + str(house*price) + " pln)/"
        if(count*price < getAccountBalance(player)):
            message = message + \
                "hotel (" + str((count*price) + hotel_price) + " pln)"
        return message


def buy(position, player):
    cardsDB.execute(
        'SELECT price FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    price = value[0]
    updateAccountBalance(player, -price)
    changeOwner(position, player)


def buyHouse(position, player, count):
    cardsDB.execute(
        'SELECT house_price FROM streets WHERE position=?', (position, ))
    value = cardsDB.fetchone()
    price = value[0]
    print(price)
    print(getAccountBalance(player))
    updateAccountBalance(player, count*(-price))
    changeOwner(position, player)


def pay(position, player, owner):
    playerMoney = getAccountBalance(player)
    rent = getRent(position)

    if(int(playerMoney) > int(rent)):
        updateAccountBalance(player, -rent)
        updateAccountBalance(owner, rent)
        return "Zaplaciles " + str(rent) + " graczowi " + str(player)

    else:
        # TO DO
        # Opcja zastaw
        return "Nie masz wystarczajacych srodkow"


def main():
    shipPositions = [4, 12, 20, 28]
    specialPositions = [0, 2, 8, 16, 24, 30]
    setupPlayers(4)
    while True:

        message = input()
        message = message.split(",")

        if(message[0] == "position"):
            position = int(message[1])
            player = int(message[2])
            if(int(position) in shipPositions):
                # TO DO
                # kup statek
                print("Kup statek")
            elif(int(position) in specialPositions):
                # TO DO
                print("Pole specjalne")
            else:
                owner = getOwner(position)
                answer = ""
                if(owner == 0):
                    answer = buyOffer(position, player)
                    # changeOwner(position, player)
                elif(owner == player):
                    answer = buyHouseOffer(position, player)
                elif(owner != player):
                    answer = pay(position, player, owner)

                print(answer)
        elif (message[0] == "decision"):
            print('sdfsd')

    cardsConn.close()


if __name__ == "__main__":
    main()
