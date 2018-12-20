import dbfunctions

spaceshipPositions = [4, 12, 20, 28]
specialPositions = [0, 2, 8, 16, 24, 30]


def getStreetOffer(position, player):
    name = dbfunctions.getName(position)
    price = dbfunctions.getPrice(position)
    return "Czy chcesz kupic " + str(name) + " za " + str(price) + "?/Tak/Nie"


def getHouseOffer(position, player):
    price, count, hotel_price = dbfunctions.getHousesData(position)
    if(count < 5):
        message = "Ile domków chcesz postawić? Stan konta: " + \
            str(dbfunctions.getAccountBalance(player)) + "/"
        for house in range(0, 4 - count):
            if(house*price < dbfunctions.getAccountBalance(player)):
                message = message + str(house) + \
                    " (" + str(house*price) + " pln)/"
        if(count*price < dbfunctions.getAccountBalance(player)):
            message = message + \
                "hotel (" + str((count*price) + hotel_price) + " pln)"
        return message


def getSpaceshipOffer(position):
    name = dbfunctions.getSpaceshipName(position)
    price = dbfunctions.getSpaceshipPrice(position)
    return "Czy chcesz kupic " + str(name) + " za " + str(price) + "?/Tak/Nie"


def buyStreet(position, player):
    price = dbfunctions.getPrice(position)
    dbfunctions.updateAccountBalance(player, -price)
    dbfunctions.changeOwner(position, player)


def buyHouse(position, player, count):
    price = dbfunctions.getHousePrice(position)
    print(price)
    print(dbfunctions.getAccountBalance(player))
    dbfunctions.updateAccountBalance(player, count*(-price))
    dbfunctions.changeOwner(position, player)


def payRent(position, player, owner):
    playerMoney = dbfunctions.getAccountBalance(player)
    rent = dbfunctions.getRent(position)

    if(playerMoney > rent):
        dbfunctions.updateAccountBalance(player, -rent)
        dbfunctions.updateAccountBalance(owner, rent)
        return "Zaplaciles " + str(rent) + " graczowi " + str(player)

    else:
        # TO DO
        # Opcja zastaw
        return "Nie masz wystarczajacych srodkow"


def payTicket(position, player, owner):
    playerMoney = dbfunctions.getAccountBalance(player)
    price = dbfunctions.getTicketPrice(position, owner)
    if(playerMoney > price):
        dbfunctions.updateAccountBalance(player, -price)
        dbfunctions.updateAccountBalance(owner, price)
        return "Zaplaciles " + str(price) + " graczowi " + str(player)

    else:
        # TO DO
        # Opcja zastaw
        return "Nie masz wystarczajacych srodkow"


def buySpaceship(position, player):
    price = dbfunctions.getSpaceshipPrice(position)
    dbfunctions.updateAccountBalance(player, -price)
    dbfunctions.changeSpaceshipOwner(position, player)


def newPosition(position, player):
    messeage = ""
    if(position in specialPositions):
        # TO DO
        print("Pole specjalne")
    else:
        owner = dbfunctions.getOwner(position)
        if(owner == 0):
            if(position in spaceshipPositions):
                messeage = getSpaceshipOffer(position)
            else:
                messeage = getStreetOffer(position, player)
            # dbfunctions.changeOwner(position, player)
        elif(owner == player):
            if(position in spaceshipPositions):
                messeage = "next"
            else:
                messeage = getHouseOffer(position, player)
        elif(owner != player):
            if(position in spaceshipPositions):
                messeage = payTicket(position, player, owner)
            else:
                messeage = payRent(position, player, owner)

        print(messeage)


def main():

    dbfunctions.setupPlayers(4)
    while True:

        message = input()
        message = message.split(",")
        action = message[0]
        if(action == "newPosition"):
            newPosition(int(message[1]), int(message[2]))
        elif (action == "decision"):
            print('sdfsd')


if __name__ == "__main__":
    main()
