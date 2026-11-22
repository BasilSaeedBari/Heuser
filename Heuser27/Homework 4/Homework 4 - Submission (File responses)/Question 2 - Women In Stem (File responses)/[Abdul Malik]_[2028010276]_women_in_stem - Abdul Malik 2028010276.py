import random

women = {
    "Ada Lovelace": "Pioneer of computer programming.",
    "Grace Hopper": "Helped develop compilers and COBOL.",
    "Katherine Johnson": "Calculated trajectories for NASA missions."
}

score = 0

def menu():
    print("\n=== WOMEN IN STEM ===")
    print("1. Read biographies")
    print("2. Guess Who?")
    print("3. View score")
    print("4. Quit")
    return input("Choose 1-4: ").strip()

def biographies():
    for name, fact in women.items():
        print("\n" + name + ":", fact)

def play():
    global score
    name = random.choice(list(women.keys()))
    print("\nGuess the woman:", women[name])
    print("A. Ada Lovelace")
    print("B. Grace Hopper")
    print("C. Katherine Johnson")

    answers = {
        "A": "Ada Lovelace",
        "B": "Grace Hopper",
        "C": "Katherine Johnson"
    }

    answer = input("Your answer (A/B/C): ").strip().upper()

    if answer not in answers:
        print("Invalid answer!")
    elif answers[answer] == name:
        print("Correct! Well done.")
        score += 1
    else:
        print("Incorrect. The answer was", name)

    print("Fact:", women[name])

def show_score():
    print("Your total score:", score)

while True:
    choice = menu()

    if choice == "1":
        biographies()
    elif choice == "2":
        play()
    elif choice == "3":
        show_score()
    elif choice == "4":
        print("Thanks for learning about women in STEM!")
        break
    else:
        print("Invalid choice. Enter 1, 2, 3 or 4.")

