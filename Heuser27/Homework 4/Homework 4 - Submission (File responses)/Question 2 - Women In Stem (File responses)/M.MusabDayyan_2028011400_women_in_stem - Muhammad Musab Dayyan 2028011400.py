# women_in_stem.py
# Part 2: Open-Ended Problem Solving - Women in STEM
#
# A text-based "Virtual Museum" that celebrates pioneering women in computing
# and science. The user can read biographies and take a short trivia quiz.
#
# Structural elements required by the assignment:
#   - A Main Loop: a while loop that runs until the user types "quit"/"exit".
#   - Conditionals: if/elif/else statements handle the user's menu choices.
#   - Custom Functions: the program is broken into small, reusable functions.


# ---------------------------------------------------------------------------
# Helper function: print a clean divider line (clean formatting, reusability)
# ---------------------------------------------------------------------------
def line():
    print("-" * 50)


# ---------------------------------------------------------------------------
# Biography display functions - one per historical figure
# ---------------------------------------------------------------------------
def display_ada_lovelace():
    line()
    print("ADA LOVELACE  (1815 - 1852)")
    line()
    print("Known as the world's first computer programmer.")
    print("While writing notes on Charles Babbage's proposed")
    print("Analytical Engine, she described an algorithm for the")
    print("machine to compute Bernoulli numbers - the first")
    print("published algorithm intended for a machine. She also")
    print("foresaw that computers could do far more than crunch")
    print("numbers, imagining them creating music and art.")
    print()


def display_grace_hopper():
    line()
    print("GRACE HOPPER  (1906 - 1992)")
    line()
    print("A U.S. Navy rear admiral and computing pioneer who")
    print("invented one of the first compilers, translating")
    print("human-readable code into machine code. Her work led")
    print("to COBOL, a language still used in banking today.")
    print("She also popularized the term 'debugging' after a")
    print("real moth was found stuck in an early computer.")
    print()


def display_katherine_johnson():
    line()
    print("KATHERINE JOHNSON  (1918 - 2020)")
    line()
    print("A NASA mathematician whose orbital mechanics")
    print("calculations were critical to the success of the")
    print("first U.S. crewed spaceflights. John Glenn famously")
    print("asked her to personally verify the computer's math")
    print("before his 1962 orbit. Her accuracy helped bring")
    print("astronauts home safely and reach the Moon.")
    print()


def display_hedy_lamarr():
    line()
    print("HEDY LAMARR  (1914 - 2000)")
    line()
    print("A Hollywood actress and self-taught inventor who")
    print("co-developed a 'frequency-hopping' communication")
    print("system during World War II to stop enemies from")
    print("jamming radio-guided torpedoes. The same idea now")
    print("underpins modern Wi-Fi, Bluetooth, and GPS.")
    print()


# ---------------------------------------------------------------------------
# Trivia quiz
# ---------------------------------------------------------------------------
def check_answer(user_input, correct_answer):
    # Reusable checker: returns True if the answer matches (ignoring case/spaces).
    return user_input.strip().lower() == correct_answer.strip().lower()


def run_quiz():
    line()
    print("WELCOME TO THE TRIVIA QUIZ!")
    line()
    score = 0

    # Question 1
    print("Q1: Who is considered the first computer programmer?")
    a1 = input("Your answer: ")
    if check_answer(a1, "ada lovelace") or check_answer(a1, "ada"):
        print(">> Correct!\n")
        score = score + 1
    else:
        print(">> The answer was Ada Lovelace.\n")

    # Question 2
    print("Q2: Who invented one of the first compilers?")
    a2 = input("Your answer: ")
    if check_answer(a2, "grace hopper") or check_answer(a2, "grace"):
        print(">> Correct!\n")
        score = score + 1
    else:
        print(">> The answer was Grace Hopper.\n")

    # Question 3
    print("Q3: Whose calculations helped send John Glenn into orbit?")
    a3 = input("Your answer: ")
    if check_answer(a3, "katherine johnson") or check_answer(a3, "katherine"):
        print(">> Correct!\n")
        score = score + 1
    else:
        print(">> The answer was Katherine Johnson.\n")

    line()
    print("You scored " + str(score) + " out of 3!")
    line()
    print()


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
def show_menu():
    line()
    print("   THE VIRTUAL MUSEUM OF WOMEN IN STEM")
    line()
    print("Type a number to explore an exhibit:")
    print("  1 - Ada Lovelace")
    print("  2 - Grace Hopper")
    print("  3 - Katherine Johnson")
    print("  4 - Hedy Lamarr")
    print("  5 - Take the trivia quiz")
    print("  quit - Exit the museum")
    line()


# ---------------------------------------------------------------------------
# Main program (the Main Loop)
# ---------------------------------------------------------------------------
def main():
    print()
    print("Welcome! This museum celebrates brilliant women in STEM.")
    print()

    # The main loop keeps running until the user chooses to quit or exit.
    while True:
        show_menu()
        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            display_ada_lovelace()
        elif choice == "2":
            display_grace_hopper()
        elif choice == "3":
            display_katherine_johnson()
        elif choice == "4":
            display_hedy_lamarr()
        elif choice == "5":
            run_quiz()
        elif choice == "quit" or choice == "exit":
            print()
            print("Thanks for visiting. Keep exploring!")
            break
        else:
            print(">> Sorry, I didn't understand that. Please try again.\n")


# Start the program.
main()