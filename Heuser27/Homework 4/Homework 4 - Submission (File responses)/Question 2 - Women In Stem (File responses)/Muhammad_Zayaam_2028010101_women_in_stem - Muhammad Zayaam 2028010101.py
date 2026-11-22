LINE = "-" * 40

PROFILES = {
    "ada lovelace": (
        "Ada Lovelace (1815-1852)\n"
        "Wrote the first published algorithm intended for a machine, Charles\n"
        "Babbage's Analytical Engine, in 1843. She is often called the first\n"
        "computer programmer and saw that computers could go beyond arithmetic."
    ),
    "grace hopper": (
        "Grace Hopper (1906-1992)\n"
        "US Navy rear admiral who created the first compiler (A-0, 1952) and\n"
        "helped develop COBOL. She championed writing code in English-like\n"
        "language instead of machine code."
    ),
    "katherine johnson": (
        "Katherine Johnson (1918-2020)\n"
        "NASA mathematician whose orbital mechanics calculations were critical\n"
        "to the Mercury and Apollo missions. John Glenn asked her to verify the\n"
        "computer's numbers before his 1962 orbital flight."
    ),
    "marie curie": (
        "Marie Curie (1867-1934)\n"
        "Pioneer of radioactivity research. She discovered polonium and radium\n"
        "and is the only person to win Nobel Prizes in two different sciences\n"
        "(Physics 1903, Chemistry 1911)."
    ),
}

QUESTIONS = [
    ("Who created the first compiler?",
     ["ada lovelace", "grace hopper", "katherine johnson"], "grace hopper"),
    ("Whose calculations helped John Glenn's 1962 orbital flight?",
     ["marie curie", "ada lovelace", "katherine johnson"], "katherine johnson"),
    ("Who wrote the first algorithm for Babbage's Analytical Engine?",
     ["ada lovelace", "grace hopper", "marie curie"], "ada lovelace"),
    ("Who won Nobel Prizes in both Physics and Chemistry?",
     ["katherine johnson", "marie curie", "grace hopper"], "marie curie"),
]


def print_header(title):
    print()
    print(LINE)
    print(title.center(40))
    print(LINE)


def show_menu():
    print_header("WOMEN IN STEM")
    print("1. Virtual Museum (read a biography)")
    print("2. Trivia Game")
    print("3. Quit")


def display_profile(name):
    name = name.strip().lower()
    if name in PROFILES:
        print()
        print(PROFILES[name])
    else:
        print("Sorry, no profile found for that name.")


def virtual_museum():
    print_header("VIRTUAL MUSEUM")
    print("Available:", ", ".join(n.title() for n in PROFILES))
    name = input("Type a name (or 'back'): ")
    if name.strip().lower() != "back":
        display_profile(name)


def check_answer(user_input, correct_answer):
    return user_input.strip().lower() == correct_answer.lower()


def trivia_game():
    print_header("TRIVIA GAME")
    score = 0
    for question, options, correct in QUESTIONS:
        print()
        print(question)
        for number, option in enumerate(options, start=1):
            print(f"  {number}. {option.title()}")
        answer = input("Your answer (type the name): ")
        if check_answer(answer, correct):
            print("Correct!")
            score += 1
        else:
            print(f"Not quite. The answer is {correct.title()}.")
    print(f"\nYou scored {score}/{len(QUESTIONS)}.")


def main():
    print("Welcome! Let's celebrate women who shaped science and technology.")
    running = True
    while running:
        show_menu()
        choice = input("Choose an option: ").strip().lower()

        if choice == "1":
            virtual_museum()
        elif choice == "2":
            trivia_game()
        elif choice in ("3", "quit", "exit"):
            print("Thanks for visiting. Keep exploring!")
            running = False
        else:
            print("Invalid choice, please try again.")


main()
