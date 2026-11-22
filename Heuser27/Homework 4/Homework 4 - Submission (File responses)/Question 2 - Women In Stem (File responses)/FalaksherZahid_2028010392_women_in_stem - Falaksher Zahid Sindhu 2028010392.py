LINE = "-" * 50
def print_header(title):
    print()
    print(LINE)
    print(title.center(50))
    print(LINE)
def show_menu():
    print_header("WOMEN IN STEM")
    print("1. Visit the virtual museum")
    print("2. Play the trivia game")
    print("3. Quit")
    print()
def check_answer(user_input, correct_answer):
    return user_input.strip().lower() == correct_answer
def display_ada_lovelace():
    print_header("Ada Lovelace")
    print("Years:  1815-1852")
    print("Field:  Mathematics and Computing")
    print()
    print("Ada Lovelace was an English mathematician and the daughter")
    print("of the poet Lord Byron. In 1843 she published notes on")
    print("Charles Babbage's Analytical Engine that included an")
    print("algorithm to calculate Bernoulli numbers. It is widely")
    print("considered the first published computer program.")
    print()
    print("Fun fact: She imagined that computers could one day go")
    print("beyond numbers and work with music and art.")
    print(LINE)
def display_grace_hopper():
    print_header("Grace Hopper")
    print("Years:  1906-1992")
    print("Field:  Computer Science and Naval Service")
    print()
    print("Grace Hopper was a U.S. Navy rear admiral and computer")
    print("scientist. Around 1952 she developed the A-0 system, an")
    print("early compiler, and she helped shape COBOL, one of the")
    print("first programming languages designed to read like English.")
    print()
    print("Fun fact: She helped popularize the word 'debugging' after")
    print("a moth was found in the Harvard Mark II computer in 1947.")
    print(LINE)
def display_katherine_johnson():
    print_header("Katherine Johnson")
    print("Years:  1918-2020")
    print("Field:  Mathematics and Space Flight")
    print()
    print("Katherine Johnson was a NASA mathematician whose trajectory")
    print("calculations were vital to early U.S. human spaceflight,")
    print("including Alan Shepard's 1961 flight. Before his 1962")
    print("orbital mission, astronaut John Glenn asked her to")
    print("personally verify the computer's numbers.")
    print()
    print("Fun fact: She received the Presidential Medal of Freedom")
    print("in 2015.")
    print(LINE)
def display_marie_curie():
    print_header("Marie Curie")
    print("Years:  1867-1934")
    print("Field:  Physics and Chemistry")
    print()
    print("Marie Curie pioneered research on radioactivity and")
    print("discovered the elements polonium and radium. She was the")
    print("first woman to win a Nobel Prize, and remains the only")
    print("person to win Nobel Prizes in two different sciences")
    print("(Physics in 1903 and Chemistry in 1911).")
    print()
    print("Fun fact: She coined the term 'radioactivity'.")
    print(LINE)
def display_hedy_lamarr():
    print_header("Hedy Lamarr")
    print("Years:  1914-2000")
    print("Field:  Film and Engineering")
    print()
    print("Hedy Lamarr was a famous film actress and also an")
    print("inventor. In 1942 she and composer George Antheil received")
    print("a patent for a frequency-hopping communication system.")
    print("The idea later influenced wireless technologies such as")
    print("Wi-Fi and Bluetooth.")
    print()
    print("Fun fact: She is honored in the National Inventors Hall")
    print("of Fame.")
    print(LINE)
def show_exhibits():
    """Print the names the user can type to open a profile."""
    print("Exhibits:")
    print("  ada        -> Ada Lovelace")
    print("  grace      -> Grace Hopper")
    print("  katherine  -> Katherine Johnson")
    print("  marie      -> Marie Curie")
    print("  hedy       -> Hedy Lamarr")
    print("  back       -> return to main menu")
def run_museum():
    print_header("VIRTUAL MUSEUM")
    while True:
        print()
        show_exhibits()
        choice = input("\nWho would you like to learn about? ").strip().lower()

        if choice == "back":
            break
        elif choice == "ada":
            display_ada_lovelace()
        elif choice == "grace":
            display_grace_hopper()
        elif choice == "katherine":
            display_katherine_johnson()
        elif choice == "marie":
            display_marie_curie()
        elif choice == "hedy":
            display_hedy_lamarr()
        else:
            print("Sorry, that exhibit doesn't exist. Try one of the names above.")
def ask_question(number, question, choice_a, choice_b, choice_c, correct):
    print()
    print("Question " + str(number) + ": " + question)
    print("  a) " + choice_a)
    print("  b) " + choice_b)
    print("  c) " + choice_c)
    answer = input("Your answer (a/b/c): ")
    if check_answer(answer, correct):
        print("Correct!")
        return 1
    else:
        print("Not quite. The correct answer was " + correct + ".")
        return 0
def show_score(score, total):
    print()
    print(LINE)
    print("Final score: " + str(score) + " / " + str(total))
    if score == total:
        print("Perfect! You really know your STEM pioneers!")
    elif score >= 3:
        print("Great job! Visit the museum to learn even more.")
    else:
        print("Good try! The museum has all the answers.")
    print(LINE)
def run_quiz():
    print_header("TRIVIA GAME")
    score = 0

    score += ask_question(
        1, "Who wrote what is considered the first computer program?",
        "Grace Hopper", "Ada Lovelace", "Marie Curie", "b")

    score += ask_question(
        2, "Who developed an early compiler called the A-0 system?",
        "Grace Hopper", "Katherine Johnson", "Hedy Lamarr", "a")

    score += ask_question(
        3, "Whose calculations helped verify John Glenn's orbital flight?",
        "Ada Lovelace", "Marie Curie", "Katherine Johnson", "c")

    score += ask_question(
        4, "Who won Nobel Prizes in both Physics and Chemistry?",
        "Marie Curie", "Hedy Lamarr", "Grace Hopper", "a")

    score += ask_question(
        5, "Whose frequency-hopping patent influenced Wi-Fi and Bluetooth?",
        "Katherine Johnson", "Hedy Lamarr", "Ada Lovelace", "b")

    show_score(score, 5)
def main():
    print_header("Welcome to the Women in STEM Hall of Fame!")
    while True:
        show_menu()
        choice = input("Choose an option (1-3): ").strip().lower()

        if choice == "1" or choice == "museum":
            run_museum()
        elif choice == "2" or choice == "quiz":
            run_quiz()
        elif choice == "3" or choice == "quit" or choice == "exit":
            print("\nThanks for visiting! Keep exploring STEM!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


main()