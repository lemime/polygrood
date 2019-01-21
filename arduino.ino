#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Streaming.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define LICZBAPOL 32

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(LICZBAPOL, PIN, NEO_GRB + NEO_KHZ800);

struct Option
{
    String designation;
    String content;
};

struct rgb
{
    int r;
    int g;
    int b;
};

struct Player
{
    int id;
    int position;
    bool statusBlocked;
    rgb color;
};

rgb fieldColors[32] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}};

Player players[4] = {{1, 0, 0, {1, 1, 0}}, {2, 0, 0, {1, 0, 1}}, {3, 0, 0, {0, 1, 1}}, {4, 0, 0, {0, 1, 0}}};
int currentPlayerId = 1;
Player *currentPlayer = &players[currentPlayerId - 1];
int playersCount = 4;

int nbts = 4;
int startpin = 2;
int bts[4];
boolean btgs[4];
String lines[4];

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void showOptions(Option *options, int firstOptionId, int optionsCount)
{
    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print("Co chcesz zrobic?");
    for (int i = 1; i <= 3; i++)
    {
        if (i <= optionsCount + 1)
        {
            lcd.setCursor(1, i);
            lcd.print(options[firstOptionId + i - 1].content);
        }
    }
}

unsigned long newrandom(unsigned long howsmall, unsigned long howbig)
{
    return howsmall + random() % (howbig - howsmall);
}

int buttonUp(int currentLine, int optionsCount, Option *options)
{
    if (currentLine > 3)
    {
        currentLine = currentLine - 1;
        showOptions(options, currentLine - 3, optionsCount);
        lcd.setCursor(0, 4);
        lcd.write(126);
    }
    else
    {
        if (currentLine > 1)
        {
            currentLine = currentLine - 1;
            showOptions(options, 0, optionsCount);
            lcd.setCursor(0, currentLine);
            lcd.write(126);
        }
    }
    return currentLine;
}

int buttonDown(int currentLine, int optionsCount, Option *options)
{

    if (currentLine < 3 && currentLine <= optionsCount)
    {   
          showOptions(options, 0, optionsCount);
          currentLine = currentLine + 1;
          lcd.setCursor(0, currentLine);
          lcd.write(126);

    }
    else
    {
        if (optionsCount > 3 && currentLine < optionsCount)
        {
            currentLine = currentLine + 1;
            showOptions(options, currentLine - 3, optionsCount);
            lcd.setCursor(0, 4);
            lcd.write(126);
        }
    }
    return currentLine;
}

String chooseOption(int optionsCount, Option *options)
{
    int currentLine = 1;
    while (1)
    {
        if (!btgs[0])
        {
            if (digitalRead(bts[0]) == LOW)
            {
                currentLine = buttonUp(currentLine, optionsCount, options);
                btgs[0] = true;
            }
        }
        else
        {
            if (digitalRead(bts[0]) == HIGH)
            {
                btgs[0] = false;
            }
        }

        if (!btgs[1])
        {
            if (digitalRead(bts[1]) == LOW)
            {
                currentLine = buttonDown(currentLine, optionsCount, options);
                btgs[1] = true;
            }
        }
        else
        {
            if (digitalRead(bts[1]) == HIGH)
            {
                btgs[1] = false;
            }
        }

        if (!btgs[2])
        {
            if (digitalRead(bts[2]) == LOW)
            {
                break;
                btgs[2] = true;
            }
        }
        else
        {
            if (digitalRead(bts[2]) == HIGH)
            {
                btgs[3] = false;
            }
        }
    }

    if (options[currentLine - 1].designation == "[buyStreet]" || options[currentLine - 1].designation == "[buySpaceship]")
    {
        changeFieldColors(currentPlayer->position, {currentPlayer->color.r, currentPlayer->color.g, currentPlayer->color.b});
    }
    return options[currentLine - 1].designation;
}

void confirmWait()
{
    while (digitalRead(bts[2]) == HIGH)
    {
    }
}

void showInfo(String content, String click = "OK")
{
    lcd.setCursor(0, 0);
    lcd.clear();

    for (int i = 0; i < content.length() / 20 + 1; i++)
    {
        lcd.setCursor(0, i);
        for (int j = 0; j < 20; j++)
        {
            if (content[(i * 20) + j])
            {
                lcd.print(content[(i * 20) + j]);
            }
        }
    }

    lcd.setCursor(4, 4);
    lcd.print("Wcisnij [" + click + "]");
    confirmWait();
    Serial.print("[generateOptions]," + String(currentPlayer->position) + "," + String(currentPlayerId));
}

void playerLost()
{
    showInfo("Gracz " + String(currentPlayerId) + " przegrywa.");
}

void changeFieldColors(int id, rgb color)
{

    fieldColors[id].r = fieldColors[id].r + color.r;
    fieldColors[id].g = fieldColors[id].g + color.g;
    fieldColors[id].b = fieldColors[id].b + color.b;

    if (fieldColors[id].r < 0)
    {
        fieldColors[id].r = 0;
    }
    if (fieldColors[id].g < 0)
    {
        fieldColors[id].g = 0;
    }
    if (fieldColors[id].b < 0)
    {
        fieldColors[id].b = 0;
    }
}

void dothetrick(int prev, int curr)
{

    changeFieldColors(prev, {-currentPlayer->color.r * 200, -currentPlayer->color.g * 200, -currentPlayer->color.b * 200});
    pixels.setPixelColor(prev, fieldColors[prev].r, fieldColors[prev].g, fieldColors[prev].b);
    pixels.show();

    for (int i = prev + 1; i <= curr; i++)
    {
        pixels.setPixelColor(i, currentPlayer->color.r * 200, currentPlayer->color.g * 200, currentPlayer->color.b * 200);
        pixels.show();
        delay(150);
        pixels.setPixelColor(i, fieldColors[i].r, fieldColors[i].g, fieldColors[i].b);
        pixels.show();
    }

    changeFieldColors(curr, {currentPlayer->color.r * 200, currentPlayer->color.g * 200, currentPlayer->color.b * 200});
    pixels.setPixelColor(curr, fieldColors[curr].r, fieldColors[curr].g, fieldColors[curr].b);

    pixels.setPixelColor(curr, 0, 0, 0);
    pixels.show();
    delay(300);
    pixels.setPixelColor(curr, fieldColors[curr].r, fieldColors[curr].g, fieldColors[curr].b);
    pixels.show();
}

int roll()
{
    int diceValue = 0;
    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print("Gracz " + String(currentPlayerId) + " rzuca kostka");
    lcd.setCursor(2, 4);
    lcd.print("Wcisnij [ROLL]");
    while (1)
    {
        if (!btgs[3])
        {
            if (digitalRead(bts[3]) == LOW)
            {
                diceValue = newrandom(2, 12);
                break;
                btgs[3] = true;
            }
        }
        else
        {
            if (digitalRead(bts[3]) == HIGH)
            {
                btgs[3] = false;
            }
        }
    }

    return diceValue;
}

int count_commas(String s)
{
    int count = 0;

    for (int i = 0; i < s.length(); i++)
        if (s[i] == ',')
            count++;

    return count;
}

void getOptions(String content)
{
    int optionsCount = (count_commas(content) + 1) / 2;
    Option options[optionsCount];
    Option option;
    int counter = 0;

    String delimiter = ",";

    while (counter < optionsCount)
    {
        option.designation = content.substring(0, content.indexOf(delimiter));
        content.remove(0, content.indexOf(delimiter) + delimiter.length());
        option.content = content.substring(0, content.indexOf(delimiter));
        content.remove(0, content.indexOf(delimiter) + delimiter.length());
        options[counter] = option;
        counter++;
    }
    showOptions(options, 0, optionsCount - 1);
    lcd.setCursor(0, 1);
    lcd.write(126);
    Serial.print(String(chooseOption(counter - 1, options)) + ',' + String(currentPlayer->position) + "," + String(currentPlayerId));
}

void nextPlayer()
{
    currentPlayerId++;
    if (currentPlayerId > playersCount)
    {
        currentPlayerId = 1;
    }
    currentPlayer = &players[currentPlayerId - 1];
    int prevPos = currentPlayer->position;
    currentPlayer->position = currentPlayer->position + roll();
    if (currentPlayer->position >= 32)
    {
        currentPlayer->position = currentPlayer->position - 32;
    }
    dothetrick(prevPos, currentPlayer->position);
    Serial.print("[newPosition]," + String(currentPlayer->position) + "," + String(currentPlayerId));
}

void chooseAction(String str)
{

    String delimiter = ",";
    String action = str.substring(0, str.indexOf(delimiter));
    str.remove(0, str.indexOf(delimiter) + delimiter.length());

    if (action == "[info]")
    {
        showInfo(str);
    }
    else if (action == "[options]")
    {
        getOptions(str);
    }
    else if (action == "[lost]")
    {
        playerLost();
    }
    else if (action == "[exit]")
    {
        nextPlayer();
    }
    else if (action == "[aviliablePositions]")
    {
        getOptions(str);
    }
}

void setup()
{
    Serial.begin(9600);
    pixels.begin();
    for (int i = 0; i < nbts; i++)
        bts[i] = i + startpin;
    for (int i = 0; i < nbts; i++)
        btgs[i] = false;
    for (int i = 0; i < nbts; i++)
        pinMode(bts[i], INPUT_PULLUP);
    for (int i = 0; i < 4; i++)
        lines[i] = "";

    lcd.begin(20, 4);
    lcd.backlight();
    randomSeed(analogRead(0));

    for (int i = 0; i < 32; i++)
    {
        pixels.setPixelColor(i, 0, 0, 0);
    }
    pixels.show();

    int prev = currentPlayer->position;
    currentPlayer->position = currentPlayer->position + roll();
    dothetrick(prev, currentPlayer->position);
    Serial.print("[newPosition]," + String(currentPlayer->position) + "," + String(currentPlayerId));
}

void loop()
{

    while (Serial.available() > 0)
    {
        String str = Serial.readString();
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("Kokos");
        delay(1000);
        lcd.print(str);
        delay(1000);
        chooseAction(str);
    }

    delay(15);
}
