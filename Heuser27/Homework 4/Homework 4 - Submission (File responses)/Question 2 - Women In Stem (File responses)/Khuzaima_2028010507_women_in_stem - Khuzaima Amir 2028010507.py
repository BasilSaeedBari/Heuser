import random

LINE = "--------------------------------------------------------------------------------"

WOMEN = {
    "ada lovelace": {
        "name": "Ada Lovelace",
        "clues": [
            "I was born in 1815 and was the daughter of the poet Lord Byron.",
            "I worked with Charles Babbage on his Analytical Engine.",
            "I wrote the first published algorithm meant for a machine.",
        ],
    },
    "grace hopper": {
        "name": "Grace Hopper",
        "clues": [
            "I served in the US Navy and became a Rear Admiral.",
            "I helped create COBOL, an early business programming language.",
            "I developed the first compiler in 1952.",
        ],
    },
    "katherine johnson": {
        "name": "Katherine Johnson",
        "clues": [
            "I worked as a 'human computer' at NASA.",
            "John Glenn asked me to double-check the computer's numbers before his flight.",
            "My orbital mechanics calculations were critical to NASA's success.",
        ],
    },
}


def show_women_list():
    print("The woman is one of these:")
    for i in WOMEN:
        print("  -", WOMEN[i]["name"])


def show_menu():
    print()
    print(LINE)
    print("   GUESS WHO? - WOMEN IN STEM")
    print(LINE)
    print("1. Play a Round")
    print("2. Quit")
    print(LINE)


def check_answer(user_input, correct_answer):
    return user_input.strip().lower() == correct_answer.lower()


def play_round(key):
    woman = WOMEN[key]
    print()
    show_women_list()
    print()
    print("Who am I?")
    for number, clue in enumerate(woman["clues"], start=1):
        print("Clue " + str(number) + ": " + clue)
        guess = input("Your guess: ")
        if check_answer(guess, key):
            points = 4 - number
            print("Correct! It's " + woman["name"] +
                  ". (+" + str(points) + " points)")
            return points
        print("Wrong answer")
    print("The correct answer was " + woman["name"] + ".")
    return 0


def main():
    print("Welcome to Guess Who? - Women in STEM!")
    print("Guess the woman from the clues. The less the clues used = the more points you get.")
    total = 0
    running = True
    while running:
        show_menu()
        choice = input("Choose an option: ").strip().lower()
        if choice == "1":
            total += play_round(random.choice(list(WOMEN)))
            print("Total score:", total)
        elif choice in ("2", "quit", "exit", "EXIT", "QUIT", "Quit", "Exit"):
            running = False
        else:
            print("Invalid option, please try again.")
    print("\nFinal score: " + str(total) + ".")


main()
