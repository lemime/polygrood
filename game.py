import dbfunctions


def buyOffer(position, player):
    name = dbfunctions.getName(position)
    price = dbfunctions.getPrice(position)
    return "Czy chcesz kupic " + str(name) + " za " + str(price) + "?/Tak/Nie"


def buyHouseOffer(position, player):
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


def buy(position, player):
    price = dbfunctions.getPrice(position)
    dbfunctions.updateAccountBalance(player, -price)
    dbfunctions.changeOwner(position, player)


def buyHouse(position, player, count):
    price = dbfunctions.getHousePrice(position)
    print(price)
    print(dbfunctions.getAccountBalance(player))
    dbfunctions.updateAccountBalance(player, count*(-price))
    dbfunctions.changeOwner(position, player)


def pay(position, player, owner):
    playerMoney = dbfunctions.getAccountBalance(player)
    rent = dbfunctions.getRent(position)

    if(int(playerMoney) > int(rent)):
        dbfunctions.updateAccountBalance(player, -rent)
        dbfunctions.updateAccountBalance(owner, rent)
        return "Zaplaciles " + str(rent) + " graczowi " + str(player)

    else:
        # TO DO
        # Opcja zastaw
        return "Nie masz wystarczajacych srodkow"


def main():
    shipPositions = [4, 12, 20, 28]
    specialPositions = [0, 2, 8, 16, 24, 30]
    dbfunctions.setupPlayers(4)
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
                owner = dbfunctions.getOwner(position)
                answer = ""
                if(owner == 0):
                    answer = buyOffer(position, player)
                    # dbfunctions.changeOwner(position, player)
                elif(owner == player):
                    answer = buyHouseOffer(position, player)
                elif(owner != player):
                    answer = pay(position, player, owner)

                print(answer)
        elif (message[0] == "decision"):
            print('sdfsd')


if __name__ == "__main__":
    main()
