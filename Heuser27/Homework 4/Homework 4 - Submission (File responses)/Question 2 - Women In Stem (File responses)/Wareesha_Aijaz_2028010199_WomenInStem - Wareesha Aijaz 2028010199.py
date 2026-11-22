
# Women in STEM Virtual Museum

def show_ada_lovelace():
    print("\n" + "=" * 45)
    print("ADA LOVELACE - PIONEER OF PROGRAMMING")
    print("=" * 45)
    print("Born: 1815 | Died: 1852")
    print("Field: Mathematics and Computer Science")
    print()
    print("Ada Lovelace was a British mathematician.")
    print("She studied Charles Babbage's proposed")
    print("Analytical Engine, an early mechanical")
    print("general-purpose computing machine.")
    print()
    print("Her notes included an algorithm intended")
    print("for the Analytical Engine. She is widely")
    print("recognised as the first computer programmer.")
    print("Her ideas helped people imagine computers")
    print("doing more than performing calculations.")
    print("=" * 45)


def show_grace_hopper():
    print("\n" + "=" * 45)
    print("GRACE HOPPER - COMPUTER SCIENCE PIONEER")
    print("=" * 45)
    print("Born: 1906 | Died: 1992")
    print("Field: Computer Science")
    print()
    print("Grace Hopper was an American mathematician")
    print("and computer scientist who served in the")
    print("United States Navy.")
    print()
    print("She helped develop early compiler technology,")
    print("which translates programming instructions")
    print("into forms a computer can process.")
    print("Her work helped make programming languages")
    print("more accessible to programmers.")
    print("=" * 45)


def show_katherine_johnson():
    print("\n" + "=" * 45)
    print("KATHERINE JOHNSON - NASA MATHEMATICIAN")
    print("=" * 45)
    print("Born: 1918 | Died: 2020")
    print("Field: Mathematics and Space Science")
    print()
    print("Katherine Johnson was an American mathematician")
    print("who worked for NASA and its predecessor, NACA.")
    print()
    print("She calculated spacecraft trajectories and")
    print("contributed to America's early human spaceflight")
    print("missions, including John Glenn's 1962 orbit")
    print("around Earth.")
    print()
    print("Her mathematical work also contributed to")
    print("the Apollo space programme.")
    print("=" * 45)


def play_quiz():
    score = 0

    print("\n" + "=" * 35)
    print("WOMEN IN STEM KNOWLEDGE QUIZ")
    print("=" * 35)

    print("\nQuestion 1:")
    print("Who is widely recognised as the first")
    print("computer programmer?")
    print("A. Grace Hopper")
    print("B. Ada Lovelace")
    print("C. Katherine Johnson")

    answer = input("Enter A, B or C: ").strip().lower()

    if answer == "b":
        print("Correct! Ada Lovelace.")
        score += 1
    elif answer == "a" or answer == "c":
        print("Not quite! The correct answer is Ada Lovelace.")
    else:
        print("Invalid option. This question was not scored.")

    print("\nQuestion 2:")
    print("Who helped develop early compiler technology?")
    print("A. Grace Hopper")
    print("B. Ada Lovelace")
    print("C. Katherine Johnson")

    answer = input("Enter A, B or C: ").strip().lower()

    if answer == "a":
        print("Correct! Grace Hopper.")
        score += 1
    elif answer == "b" or answer == "c":
        print("Not quite! The correct answer is Grace Hopper.")
    else:
        print("Invalid option. This question was not scored.")

    print("\nQuestion 3:")
    print("Whose calculations helped NASA's early")
    print("human spaceflight missions?")
    print("A. Ada Lovelace")
    print("B. Grace Hopper")
    print("C. Katherine Johnson")

    answer = input("Enter A, B or C: ").strip().lower()

    if answer == "c":
        print("Correct! Katherine Johnson.")
        score += 1
    elif answer == "a" or answer == "b":
        print("Not quite! The correct answer is Katherine Johnson.")
    else:
        print("Invalid option. This question was not scored.")

    print("\n" + "-" * 35)
    print("QUIZ COMPLETE!")
    print("Your score:", score, "out of 3")

    if score == 3:
        print("Excellent! You know your STEM history.")
    elif score == 2:
        print("Well done! You are learning.")
    else:
        print("Keep exploring the museum and try again!")

    print("-" * 35)


def main():
    while True:
        print("\n" + "=" * 45)
        print("       WOMEN IN STEM VIRTUAL MUSEUM")
        print("=" * 45)
        print("1. Explore Ada Lovelace")
        print("2. Explore Grace Hopper")
        print("3. Explore Katherine Johnson")
        print("4. Take the knowledge quiz")
        print("5. Quit")
        print("-" * 45)

        choice = input(
            "Choose an option (1-5), or type quit/exit: "
        ).strip().lower()

        if choice == "1":
            show_ada_lovelace()
        elif choice == "2":
            show_grace_hopper()
        elif choice == "3":
            show_katherine_johnson()
        elif choice == "4":
            play_quiz()
        elif choice == "5" or choice == "quit" or choice == "exit":
            print("\nThank you for visiting the museum!")
            print("Keep learning and celebrating women in STEM.")
            break
        else:
            print("Invalid choice. Please enter 1-5 or quit/exit.")


main()
