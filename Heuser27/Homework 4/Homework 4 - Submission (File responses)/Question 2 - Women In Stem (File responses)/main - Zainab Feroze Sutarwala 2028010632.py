def show_woman(name):
    if name == "ada":
        print("\nAda Lovelace")
        print("She is known as the first computer programmer.")
        print("She worked on Charles Babbage's Analytical Engine.")

    elif name == "grace":
        print("\nGrace Hopper")
        print("She was a computer scientist and US Navy officer.")
        print("She helped develop one of the first compilers.")

    elif name == "katherine":
        print("\nKatherine Johnson")
        print("She was a mathematician who worked at NASA.")
        print("Her calculations helped with important space missions.")

    else:
        print("Woman not found.")


def check_answer(user_input, correct_answer):
    if user_input == correct_answer:
        print("Correct!")
        return True
    else:
        print("Incorrect!")
        print("The correct answer was:", correct_answer)
        return False


while True:

    print("\n--- WOMEN IN STEM ---")
    print("1. Play Who Am I?")
    print("2. Read a biography")
    print("3. Quit")

    choice = input("Choose an option: ")

    if choice == "1":

        print("\nWho am I?")
        print("Clue 1: I am known as the first computer programmer.")
        print("Clue 2: I worked on the Analytical Engine.")

        answer = input("Who am I? ").lower()

        check_answer(answer, "ada")

    elif choice == "2":

        print("\nChoose a woman:")
        print("ada")
        print("grace")
        print("katherine")

        name = input("Enter a name: ").lower()

        show_woman(name)

    elif choice == "3":
        print("Thank you for learning about women in STEM!")
        break

    else:
        print("Invalid choice. Please try again.")