def display_ada():
    print("\n" + "=" * 40)
    print("ADA LOVELACE")
    print("=" * 40)
    print("Ada Lovelace was an English mathematician.")
    print("She worked on Charles Babbage's Analytical Engine.")
    print("She is often described as the first computer programmer.")
    print("She wrote an algorithm designed for a machine.")
    print("=" * 40)


def display_grace():
    print("\n" + "=" * 40)
    print("GRACE HOPPER")
    print("=" * 40)
    print("Grace Hopper was an American computer scientist.")
    print("She was a pioneer in computer programming.")
    print("She helped develop early programming languages.")
    print("She was an important figure in the development of COBOL.")
    print("=" * 40)


def display_katherine():
    print("\n" + "=" * 40)
    print("KATHERINE JOHNSON")
    print("=" * 40)
    print("Katherine Johnson was an American mathematician.")
    print("She worked for NASA and calculated orbital trajectories.")
    print("Her calculations helped support important early space missions.")
    print("She became an important figure in NASA's history.")
    print("=" * 40)


def display_marie():
    print("\n" + "=" * 40)
    print("MARIE CURIE")
    print("=" * 40)
    print("Marie Curie was a physicist and chemist.")
    print("She conducted pioneering research on radioactivity.")
    print("She discovered the elements polonium and radium.")
    print("She was the first woman to win a Nobel Prize.")
    print("=" * 40)


def show_menu():
    print("\n")
    print("=" * 40)
    print(" WOMEN IN STEM VIRTUAL MUSEUM")
    print("=" * 40)
    print("1. Ada Lovelace")
    print("2. Grace Hopper")
    print("3. Katherine Johnson")
    print("4. Marie Curie")
    print("5. Quit")
    print("=" * 40)


# Main loop
while True:

    show_menu()

    choice = input("Choose a person (1-5): ").strip()

    if choice == "1":
        display_ada()

    elif choice == "2":
        display_grace()

    elif choice == "3":
        display_katherine()

    elif choice == "4":
        display_marie()

    elif choice == "5":
        print("\nThank you for visiting the Women in STEM Museum!")
        print("Goodbye!")
        break

    else:
        print("\nInvalid choice. Please choose a number from 1 to 5.")