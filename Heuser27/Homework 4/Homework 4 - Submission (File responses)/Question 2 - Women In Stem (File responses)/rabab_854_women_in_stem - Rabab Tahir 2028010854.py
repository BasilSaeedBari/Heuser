def ada_lovelace():
    print()
    print("Ada Lovelace")
    print("She is known as the first computer programmer.")
    print("She worked on Charles Babbage's Analytical Engine.")
    print()


def grace_hopper():
    print()
    print("Grace Hopper")
    print("She was a computer scientist and US Navy officer.")
    print("She helped develop one of the first compilers.")
    print()


def katherine_johnson():
    print()
    print("Katherine Johnson")
    print("She was a mathematician who worked for NASA.")
    print("Her calculations helped support early space missions.")
    print()


choice = ""

while choice != "4":
    print("----------------------------")
    print("       WOMEN IN STEM")
    print("----------------------------")
    print("1. Ada Lovelace")
    print("2. Grace Hopper")
    print("3. Katherine Johnson")
    print("4. Quit")

    choice = input("Choose a woman to learn about: ")

    if choice == "1":
        ada_lovelace()

    elif choice == "2":
        grace_hopper()

    elif choice == "3":
        katherine_johnson()

    elif choice == "4":
        print("Thank you for visiting!")

    else:
        print("Invalid choice. Please try again.")