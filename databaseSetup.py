import sqlite3


def setup():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()

    c.execute('''DROP TABLE if exists streets''')
    c.execute('''DROP TABLE if exists spaceships''')
    c.execute('''DROP TABLE if exists players''')
    c.execute('''CREATE TABLE streets
                (name text, position integer, price integer, house_0 integer,  house_1 integer, house_2 integer, house_3 integer, house_4 integer, house_5 integer, house_price integer, hotel_price integer, mortgage_value integer, owner integer, houses_count integer, pledge integer, kit text)''')

    c.execute("INSERT INTO streets VALUES ('Elektronika i telek.', 1, 60, 2, 10, 30, 90, 160, 250, 50, 250, 30, 0, 0, 0, 'braz')")
    c.execute("INSERT INTO streets VALUES ('Teleinformatyka', 3, 60, 4, 20, 60, 180, 320, 450, 50, 250, 30, 0, 0, 0, 'braz')")
    c.execute("INSERT INTO streets VALUES ('Inz. bezpieczenstwa', 5, 100, 6, 30, 90, 270, 400, 550, 50, 250, 50, 0, 0, 0, 'blekit')")
    c.execute("INSERT INTO streets VALUES ('Logistyka', 6, 100, 6, 30, 90, 270, 400, 550, 50, 250, 50, 0, 0, 0, 'blekit')")
    c.execute("INSERT INTO streets VALUES ('Inz. zarzadzania', 7, 120, 8, 40, 100, 300, 450, 500, 50, 250, 60, 0, 0, 0, 'blekit')")

    c.execute("INSERT INTO streets VALUES ('Mechanika i bud.', 9, 140, 10, 50, 150, 450, 625, 750, 100, 600, 70, 0, 0, 0, 'roz')")
    c.execute("INSERT INTO streets VALUES ('Lotnictwo', 10, 140, 14, 70, 200, 550, 750, 950, 100, 600, 90, 0, 0, 0, 'roz')")
    c.execute("INSERT INTO streets VALUES ('Transport', 11, 160, 12, 60, 180, 500, 700, 900, 100, 600, 80, 0, 0, 0, 'roz')")
    c.execute("INSERT INTO streets VALUES ('Matematyka', 13, 180, 14, 70, 200, 550, 750, 950, 100, 600, 90, 0, 0, 0, 'pomarancz')")
    c.execute("INSERT INTO streets VALUES ('Energetyka', 14, 180, 14, 70, 200, 550, 750, 950, 100, 600, 90, 0, 0, 0, 'pomarancz')")
    c.execute("INSERT INTO streets VALUES ('Elektrotechnika', 15, 200, 16, 80, 220, 600, 800, 1000, 100, 600, 100, 0, 0, 0, 'pomarancz')")

    c.execute("INSERT INTO streets VALUES ('Inz. procesowa', 17, 220, 18, 90, 250, 700, 875, 1050, 150, 750, 110, 0, 0, 0, 'czerwony')")
    c.execute("INSERT INTO streets VALUES ('Inz. farmaceutyczna', 18, 220, 18, 90, 250, 700, 875, 1050, 150, 750, 110, 0, 0, 0, 'czerwony')")
    c.execute("INSERT INTO streets VALUES ('Inz.chemiczna', 19, 240, 20, 100, 300, 750, 925, 1100, 150, 750, 120, 0, 0, 0, 'czerwony')")
    c.execute("INSERT INTO streets VALUES ('Budownictwo', 21, 260, 22, 110, 330, 800, 975, 1150, 150, 750, 130, 0, 0, 0, 'zolty')")
    c.execute("INSERT INTO streets VALUES ('Inz. srodowiska', 22, 260, 22, 110, 330, 800, 975, 1150, 150, 750, 130, 0, 0, 0, 'zolty')")
    c.execute("INSERT INTO streets VALUES ('Budownictwo zrow.', 23, 280, 24, 120, 360, 850, 1025, 1200, 150, 750, 140, 0, 0, 0, 'zolty')")

    c.execute("INSERT INTO streets VALUES ('Mechatronika', 25, 300, 26, 130, 390, 900, 1100, 1275, 200, 1000, 150, 0, 0, 0, 'zielony')")
    c.execute("INSERT INTO streets VALUES ('Inz. materialowa', 26, 300, 26, 130, 390, 900, 1100, 1275, 200, 1000, 150, 0, 0, 0, 'zielony')")
    c.execute("INSERT INTO streets VALUES ('Inz. biomedyczna', 27, 320, 28, 150, 450, 2000, 1200, 1400, 200, 1000, 160, 0, 0, 0, 'zielony')")
    c.execute("INSERT INTO streets VALUES ('AIR', 29, 350, 35, 175, 500, 1100, 1300, 1500, 200, 1000, 175, 0, 0, 0, 'granat')")
    c.execute("INSERT INTO streets VALUES ('Informatyka', 31, 400, 50, 200, 600, 1400, 1700, 2000, 200, 1000, 200, 0, 0, 0, 'granat')")

    c.execute('''CREATE TABLE spaceships
                (name text, position integer, price integer, spaceship_1 integer, spaceship_2  integer, spaceship_3  integer, spaceship_4  integer, mortgage_value integer, owner integer, pledge integer)''')

    c.execute(
        "INSERT INTO spaceships VALUES ('Carbon X-20', 4, 200, 25, 50, 100, 200, 100, 0, 0)")
    c.execute(
        "INSERT INTO spaceships VALUES ('Santa C-40', 12, 200, 25, 50, 100, 200, 100, 0, 0)")
    c.execute(
        "INSERT INTO spaceships VALUES ('Grant R-10', 20, 200, 25, 50, 100, 200, 100, 0, 0)")
    c.execute(
        "INSERT INTO spaceships VALUES ('AZERSTAF', 28, 200, 25, 50, 100, 200, 100, 0, 0)")

    c.execute('''CREATE TABLE players (id integer, money integer, status integer)''')

    conn.commit()
    conn.close()
