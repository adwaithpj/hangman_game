import random
from tabulate import tabulate
import sqlite3
# import subprocess
#
# # Install required modules
# subprocess.run(["pip", "install", "tabulate", "sqlite3"])


# Data set using dictionary!
set_list = ["animal", "Shapes", "Place"]
word_list = {
    "animal": ['ant', 'baboon', 'badger', 'bat', 'bear', 'beaver', 'camel', 'cat', 'clam', 'cobra'],
    "Shapes": ['square', 'triangle', 'rectangle', 'circle', 'ellipse', 'rhombus', 'trapezoid'],
    "Place": ['Cairo', 'London', 'Paris', 'Baghdad', 'Istanbul', 'Riyadh']
}
# Creating and updating  Database
conn = sqlite3.connect('hangman.db')
cursor = conn.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            Level TEXT NOT NULL,
            Winner_name TEXT NOT NULL,
            Remaining_lives INTEGER NOT NULL            
)''')

#checking if table exit to execute to add default values
cursor.execute('SELECT COUNT(*) FROM high_scores')
count_of_table = cursor.fetchone()[0]

# Default insertion of values if table doesn't exist
if count_of_table == 0:
    cursor.execute('''
        INSERT OR IGNORE INTO high_scores (Level, Winner_name, Remaining_lives) 
        VALUES ('easy', " ", 0),('moderate', " ", 0),('hard', " ", 0);
    ''')
    print(" Default execution complete")

conn.commit()
conn.close()

# if cursor.connection:
#      print("Connected")


# Database Updating Function
def update_record(player_name, level, remaining_lives):
    conn = sqlite3.connect('hangman.db')
    c = conn.cursor()
    # cursor.execute('''
    # SELECT * FROM high_scores
    # WHERE Level = ? AND Remaining_lives <?
    # ''', (level, remaining_lives))
    c.execute(f'SELECT * FROM high_scores WHERE Level=?',(level.lower(),))
    existing_records = c.fetchall()
    # print(existing_records)

    if existing_records:
        # updating the winner name and the lives here
        c.execute('''
            UPDATE high_scores
            SET Winner_name = ?, Remaining_lives = ?
            WHERE Level = ? AND Remaining_lives < ?
        ''', (player_name, remaining_lives, level, remaining_lives))
    # else:
    #     # create a new record
    #     c.execute('''
    #         INSERT INTO high_scores (Winner_name,Level,Remaining_lives)
    #         VALUES (?, ? ,?)
    #     ''', (player_name, level, remaining_lives))

    conn.commit()


def show_table():
    conn = sqlite3.connect('hangman.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM high_scores AS "HALL OF FAME "')
    records = cursor.fetchall()

    table_data = []
    table_data.append([" ","HALL OF FAME", " "])
    table_data.append(["Level:" ,"Winner Name:","Health:"])
    for record in records:
        table_data.append([
            # "HALL OF FAME": None,
            record[0],
            record[1],
            record[2]
        ])
    print(tabulate(table_data,tablefmt="fancy_grid",colalign=('center',)))
    print("\n")
    conn.close()


# Function that automatically chooses a word from the word_list dict
def guess(set_name="NULL"):
    if set_name == "NULL":
        word_name = random.choice(set_list)
    else:
        word_name = set_name

    the_word = word_list[word_name][random.randint(0, len(word_list[word_name]) - 1)]
    choice_list1 = list(the_word)
    # print(choice_list)
    guess_list = ["_" for _ in choice_list1]

    return guess_list, choice_list1


# Health or Lives - Default Health Given in the documentation

# Function that display's the Menu
def show_menu(name_player):
    menu_data = [
        ["PLAY THE GAME\nEasy level 1     Moderate level 2     Hard level 3 "],
        ["Hall of Fame 4"],
        ["About the game 5"],
        ["Quit 6"]
    ]
    print(tabulate(menu_data, headers=[f'Hi "{name_player}"\nWelcome to HANGMAN'], tablefmt="fancy_grid",
                   colalign=('center',)))


# Function to display About the game
def about_game():
    # Creating a dataframe to display the about the game
    about_data = [
        [
            "Easy: the user will be given the chance to select the list from which the random word will be selected ("
            "Animal, Shape, Place). This will make it easier to guess the secret word. Also, the number of trails "
            "will be increased from 6 to 8."],
        [
            "Moderate: similar to Easy, the user will be given the chance to select the set from which the random "
            "word will be selected (Animal, Plant, Place) but the number of trails will be reduced to 6. The last two "
            "graphics will not be used or displayed."],
        [
            "Hard: The code will randomly select a set of words. From this set, the code will randomly select a word. "
            "The user will have no clue about the secret word. Also, the number of trails will remain at 6."]
    ]
    table_width = 100
    print(
        tabulate(about_data, headers=["                                         About the Game"], tablefmt="fancy_grid",
                 colalign=("left",), maxcolwidths=table_width))


# Secret list showing
def secret_word():
    secret_data = [
        ["Animals 1     Shapes 2     Places 3"]
    ]
    print(tabulate(secret_data, headers=[f"SELECT FROM THE FOLLOWING SETS OF SECRET WORDS"], tablefmt="fancy_grid",
                   colalign=('center',)))


# main Game function
def main_game(secret_select, menu_select, name_player):
    if menu_select.lower() == 'easy':
        health = 8
        guess_word, choice_list = guess(secret_select)
    elif menu_select.lower() == 'moderate':
        health = 6
        guess_word, choice_list = guess(secret_select)
    elif menu_select.lower() == 'hard':
        health = 6
        guess_word, choice_list = guess()

    while health > 0:
        print(" ".join(guess_word))
        letter = input("Guess a letter: ").lower()

        if not letter.isalpha():
            print("\nEnter a single digit:")
            continue
        if letter in guess_word:
            print('\nLetter already guessed!')
            continue
        found = False
        for i, j in enumerate(choice_list):
            
            if j.lower() == letter:
                guess_word[i] = letter
                found = True
            

        # Checks
        if secret_select == "Place":
            guess_word[0] = guess_word[0].capitalize()
        if choice_list == guess_word:
            print("You guessed the correct letter!")
            break
        if not found:
            health -= 1
            print(f"Your guess was wrong. {health} is remaining")
        if health == 0:
            print(f"Out of attempts , The word was : {''.join(choice_list)}")

    update_record(player_name=name_player, level=menu_select, remaining_lives=health)
    quit_game = input("Do you want to play again? (y/n").lower()
    if quit_game == "n":
        print("Thanks for playing!")
        game_is_on = False
        return game_is_on


# Program Start
if __name__ == "__main__":

    print("HANGMAN GAME")
    name_of_player = input("Enter your name to continue : ")
    game_is_on = True
    while game_is_on:
        show_menu(name_of_player)

        # Menu number choice from 1-5, repeats the input if input is a alphabet / negative number / more than 5
        while True:
            try:
                menu_choice = int(input("Enter your choice : "))
                if menu_choice > 6 or menu_choice <= 0:
                    print("\nEnter a choice between 1 to 6 as shown in the menu!")
                    continue
                else:
                    break
            except ValueError:
                print("\nInvalid input! Please input a Number!")

        if menu_choice == 1:
            secret_word()
            while True:
                try:
                    secret_choice = int(input("Enter your choice : "))
                    if secret_choice > 5 or secret_choice <= 0:
                        print("\nEnter a choice between 1 to 5 as shown in the menu!")
                        continue
                    else:
                        break
                except ValueError:
                    print("\nInvalid input! Please input a Number!")
            if secret_choice == 1:
                easy_return = main_game(secret_select='animal', menu_select='easy', name_player=name_of_player)
            elif secret_choice == 2:
                easy_return = main_game(secret_select='Shapes', menu_select='easy', name_player=name_of_player)
            elif secret_choice == 3:
                easy_return = main_game(secret_select='Place', menu_select='easy', name_player=name_of_player)

            if easy_return == False:
                game_is_on = False
        elif menu_choice == 2:
            secret_word()
            while True:
                try:
                    secret_choice = int(input("Enter your choice : "))
                    if secret_choice > 5 or secret_choice <= 0:
                        print("\nEnter a choice between 1 to 5 as shown in the menu!")
                        continue
                    else:
                        break
                except ValueError:
                    print("\nInvalid input! Please input a Number!")
            if secret_choice == 1:
                moderate_return = main_game(secret_select='animal', menu_select='moderate', name_player=name_of_player)
            elif secret_choice == 2:
                moderate_return = main_game(secret_select='Shapes', menu_select='moderate', name_player=name_of_player)
            elif secret_choice == 3:
                moderate_return = main_game(secret_select='Place', menu_select='moderate', name_player=name_of_player)

            if moderate_return == False:
                game_is_on = False
        elif menu_choice == 3:
            hard_return = main_game(menu_select='hard', secret_select=None, name_player=name_of_player)
            if hard_return == False:
                game_is_on = False

        elif menu_choice == 4:
            show_table()
        elif menu_choice == 5:
            about_game()
        elif menu_choice== 6:
            exit()
        else:
            print("Enter correct option")