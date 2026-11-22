import random

# (question, [accepted answers], fun fact shown afterwards)
questions = [
    (
        "Who is considered the world's first computer programmer, "
        "after writing an algorithm for Charles Babbage's Analytical Engine?",
        ["ada lovelace", "lovelace", "ada"],
        "Ada Lovelace published her notes on the Analytical Engine in 1843, "
        "including what is often called the first computer program.",
    ),
    (
        "Which US Navy rear admiral created the first compiler "
        "and helped develop the COBOL language?",
        ["grace hopper", "hopper", "grace"],
        "Grace Hopper's compiler let programmers write in English-like "
        "words instead of machine code.",
    ),
    (
        "Which NASA mathematician's orbital calculations helped send "
        "John Glenn around the Earth in 1962?",
        ["katherine johnson", "johnson", "katherine"],
        "Glenn asked for her to personally check the computer's numbers "
        "before his flight.",
    ),
    (
        "Which scientist won Nobel Prizes in both Physics and Chemistry "
        "and discovered the elements polonium and radium?",
        ["marie curie", "curie", "marie"],
        "Marie Curie remains the only person to win Nobel Prizes "
        "in two different sciences.",
    ),
]


def check_answer(user_input, valid_answers):
    return user_input.strip().lower() in valid_answers


def ask_question(question, valid_answers, fact):
    print()
    print(question)
    guess = input("Your answer: ")
    if check_answer(guess, valid_answers):
        print("Correct!")
        result = True
    else:
        print("Not quite. The answer was:", valid_answers[0].title())
        result = False
    print("Did you know?", fact)
    return result


def play_round():
    score = 0
    shuffled = questions[:]
    random.shuffle(shuffled)

    print()
    print("-" * 30)
    print("WOMEN IN STEM TRIVIA")
    print("-" * 30)

    for question, answers, fact in shuffled:
        if ask_question(question, answers, fact):
            score += 1

    print()
    print("-" * 30)
    print("You scored", score, "out of", len(questions))
    print("-" * 30)
    return score


def show_menu():
    print()
    print("1. Play a round")
    print("2. Quit")


def main():
    total_score = 0
    rounds = 0
    print("Welcome to the Women in STEM Trivia Game!")

    while True:
        show_menu()
        choice = input("> ").strip().lower()

        match choice:
            case "1":
                total_score += play_round()
                rounds += 1
            case "2" | "quit" | "exit":
                print()
                print("Rounds played:", rounds, "| Total score:", total_score)
                print("Goodbye!")
                break
            case _:
                print("Invalid choice, try again.")


main()