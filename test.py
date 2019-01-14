import dbfunctions
import random

import Adafruit_BBIO.UART as UART
import serial


# TO DO
# Zastawianie ulic / kredyt od banku
# Pensja 200 zł, status blokady (Arduino)
# Bankructwo

spaceshipPositions = [4, 12, 20, 28]
extraMoney = 0
specialPositions = [0, 2, 8, 16, 24, 30]


def playerLost():
    return "[lost]"

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
        return "[info],Zaplaciles " + str(rent) + " graczowi " + str(player)
    else:
        # TO DO
        # Opcja zastaw
        return playerLost()


def payTicket(position, player, owner):
    playerMoney = dbfunctions.getAccountBalance(player)
    price = dbfunctions.getTicketPrice(position, owner)
    if(playerMoney > price):
        dbfunctions.updateAccountBalance(player, -price)
        dbfunctions.updateAccountBalance(owner, price)
        return "[info],Zaplaciles " + str(price) + " graczowi " + str(player)

    else:
        # TO DO
        # Opcja zastaw
        return playerLost()


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
    elif(position in specialPositions):
        print("spec")
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
        response = "[options]," + response + "[exit],Nic"
    return response


def newPosition(position, player):
    messeage = ""
    global extraMoney;
    if(position in specialPositions):
        if(position == 2):
            if(dbfunctions.updateAccountBalance(player, -200)):
                extraMoney += 200
                messeage = "[info],Zaplaciles za prace dyplomowa"
            else:
                print("Nie masz srodkow")
        elif(position == 8):
            messeage = "[info],Odwiedzasz spadochroniarzy"
        elif(position == 16):
            dbfunctions.updateAccountBalance(player, int(extraMoney))
            extraMoney = 0
            messeage = "[info],Dostales " + str(extraMoney) + "zl za stypendium"
        elif(position == 24):
            if(passExam):
                messeage = "[info],Zdałeś"
            else:
                messeage = "[blocked]"
        elif(position == 30):
            if(dbfunctions.updateAccountBalance(player, -200)):
                extraMoney = extraMoney + 200
                messeage = "[info],Zaplaciles za projekt zaliczeniowy"
            else:
                messeage = playerLost()
    elif (position in spaceshipPositions):
        owner = dbfunctions.getSpaceshipOwner(position)
        if(owner == player):
            messeage = generateOptions(position,player)
        elif(owner == 0):
            messeage = generateOptions(position,player)
        else:
            messeage = payTicket(position, player, owner)
    else:
        owner = dbfunctions.getOwner(position)
        if(int(owner) == int(player)):
            messeage =  generateOptions(position, player)
        elif (int(owner) == 0):
            messeage = generateOptions(position, player)
        else:
            messeage = payRent(position, player, owner)

    return messeage


def main():
    #
    # ser=serial.Serial(
    # port='/dev/ttyACM0',
    # baudrate=9600,
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    # timeout=1
    # )


    dbfunctions.setupPlayers(4)

     UART.setup("UART1")
     ser = serial.Serial(port="/dev/tty01", baudrate=9600)

#    ser=serial.Serial(
#    port='/dev/ttyACM0',
#    baudrate=9600,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,
#    bytesize=serial.EIGHTBITS,
#    timeout=1
#    )

    ser.close()
    ser.open()
    # ser.write("[options],[buyStreet],Kupic za 300,[exit],Nic")
    # ser.write("[info],Dostales 0zl za stypendium naukowe")

    while True:
        message = ser.readline()
        print(message)
        # message = input()
        message = message.decode().split(",")
        action = message[0]
        if(action == "[newPosition]"):
            answer = newPosition(int(message[1]), int(message[2]))
            ser.write(answer.encode())
            print(answer)
        elif(action == "[generateOptions]"):
            answer = generateOptions(int(message[1]), int(message[2]))
            ser.write(answer.encode())
            print(answer)
        elif(action == "[buyStreet]"):
            answer = buyStreet(int(message[1]), int(message[2]))
            ser.write(answer.encode())
            print(answer)
        elif (action == "[buySpaceship]"):
            answer = buySpaceship(int(message[1]), int(message[2]))
            ser.write(answer.encode())
            print(answer)
        elif (action == "[buyHousesOption]"):
            answer = getPositions(int(message[2]))
            ser.write(answer.encode())
            print(answer)
        elif (action == "[buyHouse]"):
            answer = buyHouse(int(message[1]), message[2])
            ser.write(answer.encode())
            print(answer)
        elif (action == "[exit]"):
            answer = "[exit]"
            ser.write(answer.encode())
            print(answer)


if __name__ == "__main__":
    main()