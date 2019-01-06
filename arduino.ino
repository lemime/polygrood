#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Streaming.h>

struct Option
{
    String designation;
    String content;
};

struct Player
{
    int id;
    int position;
    bool statusBlocked;
};

Player players[4] = {{1, 0, 0}, {2, 0, 0}, {3, 0, 0}, {4, 0, 0}};
int currentPlayerId = 1;
Player *currentPlayer = &players[currentPlayerId - 1];
int playersCount = 4;

int nbts = 4;
int startpin = 2;
int bts[4];
boolean btgs[4];
String lines[4];

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

int roll()
{
    int diceValue = 0;
    while (1)
    {
        if (!btgs[3])
        {
            if (digitalRead(bts[3]) == LOW)
            {
                diceValue = random(2, 12);
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

void showOptions(Option *options, int firstOptionId)
{
    lcd.setCursor(0, 0);
    lcd.clear();
    for (int i = 1; i <= 3; i++)
    {
        lcd.setCursor(1, i);
        lcd.print(options[firstOptionId + i - 1].content);
    }
}

int buttonUp(int currentLine, int optionsCount, Option *options)
{
    if (currentLine > 3)
    {
        currentLine = currentLine - 1;
        showOptions(options, currentLine - 3);
        lcd.setCursor(0, 4);
        lcd.write(126);
    }
    else
    {
        if (currentLine > 1)
        {
            currentLine = currentLine - 1;
            showOptions(options, 0);
            lcd.setCursor(0, currentLine);
            lcd.write(126);
        }
    }
    return currentLine;
}

int buttonDown(int currentLine, int optionsCount, Option *options)
{

    if (currentLine < 3)
    {
        showOptions(options, 0);
        currentLine = currentLine + 1;
        lcd.setCursor(0, currentLine);
        lcd.write(126);
    }
    else
    {
        if (optionsCount > 3 && currentLine < optionsCount)
        {
            currentLine = currentLine + 1;
            showOptions(options, currentLine - 3);
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

    return options[currentLine - 1].designation;
}

void confirmWait()
{
    while (digitalRead(bts[2]) == HIGH)
    {
    }
}

void showInfo(String content)
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
    lcd.print("Wcisnij [OK]");
    confirmWait();
    Serial.print("[generateOptions]," + String(currentPlayer->position) + ',' + String(currentPlayerId));
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

    char *cstr = new char[content.length() + 1];
    strcpy(cstr, content.c_str());

    char *frag = strtok(cstr, ",");
    option.designation = frag;
    frag = strtok(NULL, ",");
    option.content = frag;
    options[counter] = option;
    counter++;

    while (frag != NULL)
    {
        frag = strtok(NULL, ",");
        option.designation = frag;
        frag = strtok(NULL, ",");
        option.content = frag;
        options[counter] = option;
        counter++;
    }
    showOptions(options, 0);
    lcd.setCursor(0, 1);
    lcd.write(126);
    Serial.print(chooseOption(counter - 1, options) + ',' + currentPlayer->position + "," + currentPlayerId + ',');
}

void nextPlayer()
{
    currentPlayerId++;
    currentPlayerId % playersCount;
    currentPlayer = &players[currentPlayerId - 1];
    currentPlayer->position = currentPlayer->position + roll();
    Serial.print("[newPosition]," + String(currentPlayer->position) + "," + String(currentPlayerId));
}

void chooseAction(String str)
{
    String action = "";
    int i = 1;
    while (str[i] != 93 || str[i] != 44)
    {
        action = action + str[i];
        i++;
    }
    i++;

    if (action == "info")
    {
        showInfo(str.substring(i));
    }
    else if (action == "options")
    {
        getOptions(str.substring(i));
    }
    else if (action == "exit")
    {
        nextPlayer();
    }
}

void setup()
{
    Serial.begin(9600);
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

    currentPlayer->position = currentPlayer->position + roll();
    Serial.print("[newPosition]," + String(currentPlayer->position) + "," + String(currentPlayerId));
}

void loop()
{

    while (Serial.available() > 0)
    {
        String str = Serial.readString();
        chooseAction(str);
    }

    delay(15);
}