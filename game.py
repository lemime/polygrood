import dbfunctions
import random


spaceshipPositions = [4, 12, 20, 28]
specialPositions = [0, 2, 8, 16, 24, 30]
scholarship = 0


def getStreetOffer(position, player):
    name = dbfunctions.getName(position)
    price = dbfunctions.getPrice(position)
    return "Czy chcesz kupic " + str(name) + " za " + str(price) + "?/Tak/Nie"


def getHouseOffer(position, player):
    price, count, hotel_price = dbfunctions.getHousesData(position)
    if(count < 5):
        message = "Ile domków chcesz postawić? Stan konta: " + \
            str(dbfunctions.getAccountBalance(player)) + "/"
        for house in range(0, 5 - count):
            if(house*price < dbfunctions.getAccountBalance(player)):
                message = message + str(house) + \
                    " (" + str(house*price) + " pln)/"
        if(count*price < dbfunctions.getAccountBalance(player)):
            message = message + \
                "hotel (" + str((count*price) + hotel_price) + " pln)"
        return message
    else:
        return "next"


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
    dbfunctions.updateAccountBalance(player, count*(-price))
    dbfunctions.updateHouseCount(position, count)


def payRent(position, player, owner):
    rent = dbfunctions.getRent(position)
    if(dbfunctions.monopolCheck(position, owner) and not dbfunctions.isBuildUp(position)):
        rent = rent * 2
    dbfunctions.updateAccountBalance(owner, rent)

    if(dbfunctions.updateAccountBalance(player, -rent)):
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


def passExam():
    note = random.randint(1, 5)
    if(note >= 3):
        return 1
    else:
        return 0


def newPosition(position, player):
    messeage = ""
    if(position in specialPositions):
        if(position == 2):
            if(dbfunctions.updateAccountBalance(player, -200)):
                scholarship = scholarship + 200
                messeage = "next/Zaplaciles za prace dyplomowa"
            else:
                print("Nie masz srodkow")
        elif(position == 8):
            messeage = "next/Odwiedzasz spadochroniarzy"
        elif(position == 16):
            dbfunctions.updateAccountBalance(player, scholarship)
            scholarship = 0
            messeage = "next/Dostales " + \
                str(scholarship) + "za stypendium naukowe."
        elif(position == 24):
            if(passExam):
                messeage = "next/Zdałeś"
            else:
                messeage = "statusBlocked"
        elif(position == 30):
            messeage = "next"
    elif (position in spaceshipPositions):
        owner = dbfunctions.getSpaceshipOwner(position)
        if(owner == 0):
            messeage = getSpaceshipOffer(position)
        elif(owner == player):
            messeage = "next"
        elif(owner != player):
            messeage = payTicket(position, player, owner)
    else:
        owner = dbfunctions.getOwner(position)
        if(owner == 0):
            messeage = getStreetOffer(position, player)
        elif(owner == player):
            messeage = getHouseOffer(position, player)
        elif(owner != player):
            messeage = payRent(position, player, owner)

    return messeage


def main():

    dbfunctions.setupPlayers(4)
    while True:

        message = input()
        message = message.split(",")
        action = message[0]
        if(action == "newPosition"):
            answer = newPosition(int(message[1]), int(message[2]))
            # serial.print("lcd/"+messeage)
            print(answer)
        elif(action == "buyStreet"):
            buyStreet(int(message[1]), int(message[2]))
        elif (action == "buyHouse"):
            buyHouse(int(message[1]), int(message[2]), int(message[3]))
        elif (action == "buySpaceship"):
            buySpaceship(int(message[1]), int(message[2]))


if __name__ == "__main__":
    main()
