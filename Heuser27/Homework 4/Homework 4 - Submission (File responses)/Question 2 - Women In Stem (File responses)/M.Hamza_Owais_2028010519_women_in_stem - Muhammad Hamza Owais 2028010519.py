
import random

LINE = "-" * 40


def show_menu():
    print()
    print(LINE)
    print("  WOMEN IN STEM - VIRTUAL MUSEUM")
    print(LINE)
    print("  1. Ada Lovelace")
    print("  2. Grace Hopper")
    print("  3. Katherine Johnson")
    print("  4. Marie Curie")
    print("  5. Hedy Lamarr")
    print("  6. Play the quiz")
    print("  7. Play Guess Who?")
    print("  Type 'quit' to exit")
    print(LINE)


def display_ada_lovelace():
    print()
    print("ADA LOVELACE (1815 - 1852)")
    print(LINE)
    print("Ada was an English mathematician who worked with Charles")
    print("Babbage on his Analytical Engine, a design for an early")
    print("computer. In her notes she wrote what is often called the")
    print("first computer program, an algorithm to calculate Bernoulli")
    print("numbers. She also imagined machines doing more than maths.")


def display_grace_hopper():
    print()
    print("GRACE HOPPER (1906 - 1992)")
    print(LINE)
    print("Grace was a US Navy rear admiral and computer scientist.")
    print("She created one of the first compilers (the A-0 system, 1952),")
    print("which turned human-readable code into machine code. Her work")
    print("led to COBOL, a language made to be readable like English.")
    print("She also helped popularise the word 'debugging'.")


def display_katherine_johnson():
    print()
    print("KATHERINE JOHNSON (1918 - 2020)")
    print(LINE)
    print("Katherine was a NASA mathematician who calculated flight")
    print("paths by hand. She worked on the trajectory for Alan Shepard's")
    print("1961 flight, and astronaut John Glenn asked for her to check")
    print("the computer's numbers before his 1962 orbit. She received the")
    print("Presidential Medal of Freedom in 2015.")


def display_marie_curie():
    print()
    print("MARIE CURIE (1867 - 1934)")
    print(LINE)
    print("Marie was a physicist and chemist who researched radioactivity.")
    print("She discovered the elements polonium and radium, and she is the")
    print("first person to win Nobel Prizes in two different sciences")
    print("(Physics in 1903 and Chemistry in 1911).")


def display_hedy_lamarr():
    print()
    print("HEDY LAMARR (1914 - 2000)")
    print(LINE)
    print("Hedy was a famous film actress and also an inventor. During")
    print("World War II she and composer George Antheil patented a")
    print("'frequency hopping' idea to stop radio signals being jammed.")
    print("Ideas like it are used today in technologies such as Wi-Fi")
    print("and Bluetooth.")


def check_answer(user_input, correct_answer):
    """Return True if the user's answer matches (ignoring case/spaces)."""
    return user_input.strip().lower() == correct_answer.lower()


def ask_question(question, options, correct_letter, explanation):
    """Ask one multiple-choice question. Returns 1 if right, 0 if wrong."""
    print()
    print(question)
    print("  " + options)
    answer = input("Your answer: ")
    if check_answer(answer, correct_letter):
        print("Correct!")
        return 1
    print("Not quite. " + explanation)
    return 0


def play_quiz():
    print()
    print("QUIZ TIME! Type the letter of your answer.")
    print(LINE)
    score = 0
    score += ask_question(
        "Q1. Who is often called the first computer programmer?",
        "a) Grace Hopper  b) Ada Lovelace  c) Marie Curie",
        "b", "It was Ada Lovelace.")
    score += ask_question(
        "Q2. Grace Hopper helped create one of the first...",
        "a) Compilers  b) Telescopes  c) Rockets",
        "a", "It was a compiler.")
    score += ask_question(
        "Q3. Which agency did Katherine Johnson work for?",
        "a) NASA  b) CERN  c) Google",
        "a", "It was NASA.")
    score += ask_question(
        "Q4. Marie Curie won Nobel Prizes in how many different sciences?",
        "a) One  b) Two  c) Three",
        "b", "It was two (Physics and Chemistry).")
    score += ask_question(
        "Q5. Hedy Lamarr's invention is linked to which modern tech?",
        "a) Microwaves  b) Wi-Fi and Bluetooth  c) Televisions",
        "b", "Frequency hopping is used in Wi-Fi and Bluetooth.")

    print()
    print(LINE)
    print("You scored " + str(score) + " out of 5.")
    if score == 5:
        print("Amazing, you're a STEM history expert!")
    elif score >= 3:
        print("Nice work! Visit the museum to learn more.")
    else:
        print("Have a look around the museum and try again!")


def play_guess_who():
    people = [
        ("ada lovelace", [
            "I was born in 1815 in England.",
            "I worked with Charles Babbage.",
            "I wrote notes with an early computer algorithm."]),
        ("grace hopper", [
            "I served in the US Navy.",
            "I helped make the first compilers.",
            "I influenced the language COBOL."]),
        ("katherine johnson", [
            "I was a mathematician at NASA.",
            "I calculated flight paths by hand.",
            "John Glenn trusted my numbers."]),
        ("marie curie", [
            "I discovered polonium and radium.",
            "I studied radioactivity.",
            "I won two Nobel Prizes."]),
        ("hedy lamarr", [
            "I was a film star in Hollywood.",
            "I also worked as an inventor.",
            "My frequency hopping idea is used in Wi-Fi."]),
    ]

    name, clues = random.choice(people)
    print()
    print("GUESS WHO? I'll give you up to 3 clues.")
    print(LINE)

    for number in range(len(clues)):
        print("Clue " + str(number + 1) + ": " + clues[number])
        guess = input("Who am I? ")
        if guess.strip().lower() == name:
            print("Yes! I'm " + name.title() + ". You got it in " + str(number + 1) + " clue(s)!")
            return
        print("Nope, try again.")

    print("The answer was " + name.title() + ". Check the museum to learn more!")



print("Welcome to the Women in STEM museum!")
running = True

while running:
    show_menu()
    choice = input("What would you like to do? ").strip().lower()

    if choice == "1":
        display_ada_lovelace()
    elif choice == "2":
        display_grace_hopper()
    elif choice == "3":
        display_katherine_johnson()
    elif choice == "4":
        display_marie_curie()
    elif choice == "5":
        display_hedy_lamarr()
    elif choice == "6":
        play_quiz()
    elif choice == "7":
        play_guess_who()
    elif choice == "quit" or choice == "exit":
        running = False
    else:
        print("Sorry, I didn't understand that. Try 1-7 or 'quit'.")

print()
print("Thanks for visiting! Keep learning about the women who shaped STEM.")
