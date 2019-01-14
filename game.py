import dbfunctions
import random

import Adafruit_BBIO.UART as UART
import serial


# TO DO
# Zastawianie ulic / kredyt od banku
# Pensja 200 zł, status blokady (Arduino)
# Bankructwo
# Nie ma oferty jak nie ma środków


spaceshipPositions = [4, 12, 20, 28]
specialPositions = [0, 2, 8, 16, 24, 30]
scholarship = 0


def getStreetOffer(position):
    price = dbfunctions.getPrice(position)
    return "[buyStreet],Kupic za " + str(price) + ","


def getSpaceshipOffer(position):
    name = dbfunctions.getSpaceshipName(position)
    return "[buySpaceship],Kupic " + str(name) + ","


def buyStreet(position, player):
    name = dbfunctions.getName(position)
    price = dbfunctions.getPrice(position)
    dbfunctions.updateAccountBalance(player, -price)
    dbfunctions.changeOwner(position, player)
    return "[info],Kupiles " + str(name)


def buyHouse(player, name):
    position = dbfunctions.getPosition(name)
    price = dbfunctions.getHousePrice(position)
    dbfunctions.updateAccountBalance(player, -price)
    dbfunctions.updateHouseCount(position)
    return "[info],Kupiles domek"


def payRent(position, player, owner):
    rent = dbfunctions.getRent(position)
    if(dbfunctions.monopolCheck(owner) and not dbfunctions.isBuildUp(position)):
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
    name = dbfunctions.getSpaceshipName(position)
    price = dbfunctions.getSpaceshipPrice(position)
    dbfunctions.updateAccountBalance(player, -price)
    dbfunctions.changeSpaceshipOwner(position, player)
    return "[info],Kupiles " + str(name)


def getPositions(player):
    positions = dbfunctions.getHouseAviliableStreets(player)
    return "[aviliablePositions]," + ",".join(str(position) for position in positions)


def passExam():
    note = random.randint(1, 5)
    if(note >= 3):
        return 1
    else:
        return 0


def generateOptions(position, player):
    response = ""
    if(position in spaceshipPositions):
        owner = dbfunctions.getSpaceshipOwner(position)
        if(owner == 0):
            response = response + getSpaceshipOffer(position)
    else:
        owner = dbfunctions.getOwner(position)
        if(owner == 0):
            response = response + getStreetOffer(position)
    kits = dbfunctions.getHouseAviliableStreets(player)
    if(kits != 0):
        response = response + "[buyHousesOption],Kupic domki?,"
    if(response == ""):
        response = "[exit]"
    else:
        response = "[options]" + response + "[exit],Nic"
    return response


def newPosition(position, player):
    messeage = ""
    if(position in specialPositions):
        if(position == 2):
            if(dbfunctions.updateAccountBalance(player, -200)):
                scholarship = scholarship + 200
                messeage = "[info],Zaplaciles za prace dyplomowa"
            else:
                print("Nie masz srodkow")
        elif(position == 8):
            messeage = "[info],Odwiedzasz spadochroniarzy"
        elif(position == 16):
            dbfunctions.updateAccountBalance(player, scholarship)
            scholarship = 0
            messeage = "[info],Dostales " + \
                str(scholarship) + "za stypendium naukowe"
        elif(position == 24):
            if(passExam):
                messeage = "[info],Zdałeś"
            else:
                messeage = "[blocked]"
        elif(position == 30):
            if(dbfunctions.updateAccountBalance(player, -200)):
                scholarship = scholarship + 200
                messeage = "[info],Zaplaciles za projekt zaliczeniowy"
            else:
                print('nie masz srodkow')
    elif (position in spaceshipPositions):
        owner = dbfunctions.getSpaceshipOwner(position)
        if(owner != player & owner != 0):
            messeage = payTicket(position, player, owner)
        else:
            messeage = generateOptions(position, player)
    else:
        owner = dbfunctions.getOwner(position)
        if(owner != player & owner != 0):
            messeage = payRent(position, player, owner)
        else:
            messeage = generateOptions(position, player)

    return messeage


def main():

    ser=serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )


    dbfunctions.setupPlayers(4)

    UART.setup("UART1")
    # ser = serial.Serial(port="/dev/ttyO1", baudrate=9600)
    ser.close()
    ser.open()

    while True:
        message = ser.read()

        # message = input()
        message = message.split(",")
        action = message[0]
        if(action == "[newPosition]"):
            answer = newPosition(int(message[1]), int(message[2]))
            ser.write(answer)
            print(answer)
        elif(action == "[generateOptions]"):
            answer = generateOptions(int(message[1]), int(message[2]))
            ser.write(answer)
            print(answer)
        elif(action == "[buyStreet]"):
            answer = buyStreet(int(message[1]), int(message[2]))
            ser.write(answer)
            print(answer)
        elif (action == "[buySpaceship]"):
            answer = buySpaceship(int(message[1]), int(message[2]))
            ser.write(answer)
            print(answer)
        elif (action == "[buyHousesOption]"):
            answer = getPositions(int(message[2]))
            ser.write(answer)
            print(answer)
        elif (action == "[buyHouse]"):
            answer = buyHouse(int(message[1]), message[2])
            ser.write(answer)
            print(answer)
        elif (action == "[exit]"):
            answer = "[exit]"
            ser.write(answer)
            print(answer)


if __name__ == "__main__":
    main()
