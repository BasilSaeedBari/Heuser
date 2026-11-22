def display_ada_lovelace():
    print()
    print("-" * 45)
    print("ADA LOVELACE")
    print("-" * 45)
    print("Ada Lovelace was an English mathematician.")
    print("She is widely regarded as the first computer")
    print("programmer.")
    print()
    print("She worked on Charles Babbage's Analytical Engine")
    print("and wrote an algorithm designed for the machine.")
    print()
    print("Her work showed that computers could be used")
    print("for more than just calculations.")
    print("-" * 45)


def display_grace_hopper():
    print()
    print("-" * 45)
    print("GRACE HOPPER")
    print("-" * 45)
    print("Grace Hopper was an American computer scientist")
    print("and United States Navy officer.")
    print()
    print("She helped develop one of the first compilers,")
    print("which helped make programming languages easier")
    print("for people to use.")
    print()
    print("She also played an important role in the")
    print("development of COBOL.")
    print("-" * 45)


def display_katherine_johnson():
    print()
    print("-" * 45)
    print("KATHERINE JOHNSON")
    print("-" * 45)
    print("Katherine Johnson was an American mathematician")
    print("who worked at NASA.")
    print()
    print("Her calculations helped determine the flight")
    print("paths of important early space missions.")
    print()
    print("She calculated the trajectory for John Glenn's")
    print("1962 orbital mission.")
    print()
    print("Her mathematical work contributed to the success")
    print("of early American human spaceflight.")
    print("-" * 45)


def display_all():
    display_ada_lovelace()
    display_grace_hopper()
    display_katherine_johnson()


def main():
    running = True 
    while running:
        print()
        print("=" * 45)
        print("       WOMEN IN STEM VIRTUAL MUSEUM")
        print("=" * 45)
        print("1. Ada Lovelace")
        print("2. Grace Hopper")
        print("3. Katherine Johnson")
        print("4. View all women")
        print("5. Exit")
        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            display_ada_lovelace()

        elif choice == "2":
            display_grace_hopper()

        elif choice == "3":
            display_katherine_johnson()

        elif choice == "4":
            display_all()
            running = False

        elif choice == "5":
            print()
            print("Thank you for visiting the Women in STEM Museum!")
            print("Goodbye!")
            exit = False

        else:
            print()
            print("Invalid choice. Please enter a number from 1 to 5.")

main()