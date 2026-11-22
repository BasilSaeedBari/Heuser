
def display_ada_lovelace():
    print("\n" + "=" * 45)
    print("ADA LOVELACE")
    print("=" * 45)
    print("Born: 1815")
    print("Field: Mathematics and Computer Science")
    print()
    print("Ada Lovelace was an English mathematician who")
    print("worked with Charles Babbage on his proposed")
    print("Analytical Engine.")
    print()
    print("She wrote a detailed algorithm intended for")
    print("the machine, which is why she is often regarded")
    print("as the first computer programmer.")
    print()
    print("Her work helped people imagine that computers")
    print("could do more than perform calculations.")


def display_grace_hopper():
    print("\n" + "=" * 45)
    print("GRACE HOPPER")
    print("=" * 45)
    print("Born: 1906")
    print("Field: Computer Science")
    print()
    print("Grace Hopper was an American computer scientist")
    print("and a rear admiral in the United States Navy.")
    print()
    print("She helped develop early compilers, which")
    print("translate programming instructions into forms")
    print("that computers can process.")
    print()
    print("She also contributed to the development of COBOL,")
    print("a programming language designed for business")
    print("data processing.")
    print()
    print("Her work helped make programming more accessible.")


def display_katherine_johnson():
    print("\n" + "=" * 45)
    print("KATHERINE JOHNSON")
    print("=" * 45)
    print("Born: 1918")
    print("Field: Mathematics and Space Science")
    print()
    print("Katherine Johnson was an American mathematician")
    print("who worked for NASA.")
    print()
    print("Her calculations helped determine the trajectories")
    print("of early American crewed spaceflight missions.")
    print()
    print("She contributed to the calculations supporting")
    print("John Glenn's orbital flight in 1962.")
    print()
    print("Her achievements helped demonstrate the importance")
    print("of mathematics in space exploration.")


def show_menu():
    print("\n" + "=" * 45)
    print("       WOMEN IN STEM VIRTUAL MUSEUM")
    print("=" * 45)
    print("Explore the achievements of brilliant women.")
    print()
    print("1. Ada Lovelace")
    print("2. Grace Hopper")
    print("3. Katherine Johnson")
    print("4. Quit the museum")
    print("-" * 45)


def main():
    running = True

    print("Welcome to the Women in STEM Virtual Museum!")

    while running:
        show_menu()

        choice = input("Enter your choice (1-4): ").strip().lower()

        if choice == "1" or choice == "ada lovelace":
            display_ada_lovelace()

        elif choice == "2" or choice == "grace hopper":
            display_grace_hopper()

        elif choice == "3" or choice == "katherine johnson":
            display_katherine_johnson()

        elif choice == "4" or choice == "quit" or choice == "exit":
            print("\nThank you for visiting the museum!")
            print("Keep celebrating women in STEM.")
            running = False

        else:
            print("\nInvalid choice. Please select an option from 1 to 4.")

        if running:
            input("\nPress Enter to return to the main menu...")


main()
