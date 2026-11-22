def display_ada_lovelace():
    print("\n" + "=" * 40)
    print("ADA LOVELACE")
    print("=" * 40)
    print("Ada Lovelace (1815-1852) was a mathematician.")
    print("She wrote notes describing how Charles Babbage's")
    print("Analytical Engine could follow a sequence of steps.")
    print("She is often remembered as an early computer programmer.")


def display_grace_hopper():
    print("\n" + "=" * 40)
    print("GRACE HOPPER")
    print("=" * 40)
    print("Grace Hopper (1906-1992) was a computer scientist")
    print("and U.S. Navy officer. She helped develop early")
    print("compiler technology and influenced the development")
    print("of programming languages such as COBOL.")


def display_katherine_johnson():
    print("\n" + "=" * 40)
    print("KATHERINE JOHNSON")
    print("=" * 40)
    print("Katherine Johnson (1918-2020) was a mathematician")
    print("whose calculations supported early NASA spaceflight.")
    print("Her work helped verify flight paths for important")
    print("missions, including John Glenn's orbital flight.")


def display_menu():
    print("\n" + "=" * 40)
    print("WOMEN IN STEM: DISCOVER THEIR STORIES")
    print("=" * 40)
    print("1. Take the STEM trivia quiz")
    print("2. Visit the virtual museum")
    print("3. Guess the scientist")
    print("4. Quit")


def run_quiz():
    questions = [
        {
            "question": "Who is often remembered as an early computer programmer?",
            "options": ["A. Ada Lovelace", "B. Grace Hopper", "C. Katherine Johnson"],
            "answer": "A",
            "fact": "Ada Lovelace wrote notes about how a machine could follow instructions."
        },
        {
            "question": "Who helped develop early compiler technology?",
            "options": ["A. Marie Curie", "B. Grace Hopper", "C. Katherine Johnson"],
            "answer": "B",
            "fact": "Grace Hopper helped make programming more accessible through compiler work."
        },
        {
            "question": "Whose calculations supported NASA spaceflight missions?",
            "options": ["A. Ada Lovelace", "B. Grace Hopper", "C. Katherine Johnson"],
            "answer": "C",
            "fact": "Katherine Johnson's mathematics helped NASA plan and check flight paths."
        }
    ]

    score = 0
    print("\nSTEM TRIVIA")
    for number, item in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {item['question']}")
        for option in item["options"]:
            print(option)

        answer = input("Your answer (A, B, or C): ").strip().upper()
        if answer not in ("A", "B", "C"):
            print("Please enter A, B, or C. This question will count as incorrect.")
        if answer == item["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Not quite. The correct answer is {item['answer']}.")
        print("Did you know? " + item["fact"])

    print(f"\nYour final score is {score}/{len(questions)}.")
    if score == len(questions):
        print("Excellent work! You got every question right.")
    elif score >= 2:
        print("Well done! You know quite a bit about women in STEM.")
    else:
        print("Good effort! Visit the museum and try again.")


def virtual_museum():
    while True:
        print("\nVIRTUAL MUSEUM")
        print("1. Ada Lovelace")
        print("2. Grace Hopper")
        print("3. Katherine Johnson")
        print("4. Return to main menu")
        choice = input("Choose a biography (1-4): ").strip()

        if choice == "1":
            display_ada_lovelace()
        elif choice == "2":
            display_grace_hopper()
        elif choice == "3":
            display_katherine_johnson()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


def guess_the_scientist():
    print("\nGUESS THE SCIENTIST")
    print("Clue: I was a mathematician whose calculations helped NASA")
    print("plan spaceflight paths. Who am I?")
    answer = input("Enter the scientist's name: ").strip().lower()

    # Accept a few reasonable ways of entering the name.
    if answer in ("katherine johnson", "katherine", "johnson"):
        print("Correct! It was Katherine Johnson.")
    else:
        print("Good try! The answer is Katherine Johnson.")
        print("Her mathematical work supported important NASA missions.")


def main():
    print("Welcome! Explore the achievements of women in STEM.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            run_quiz()
        elif choice == "2":
            virtual_museum()
        elif choice == "3":
            guess_the_scientist()
        elif choice == "4":
            print("Thanks for visiting Women in STEM. Keep learning!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
