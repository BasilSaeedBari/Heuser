def ada_lovelace():
    print()
    print("ADA LOVELACE")
    print()

    print("STEM Field: Computer Science & Mathematics")
    print()

    print("General Facts:")
    print("She was the daughter of the famous poet Lord Byron, though her mother encouraged her to study mathematics and science.")
    print("She is widely recognized as the world's first computer programmer for her extensive notes on Charles Babbage's Analytical Engine.")
    print()

    print("Major Achievements:")
    print("She published the first algorithm intended to be carried out by a machine in 1843.")
    print("She conceptualized that computers could do much more than pure mathematical calculations.")
    print()

    print("Interesting Fact:")
    print("Ada Lovelace was fascinated by the idea of 'poetical science' and believed intuition and imagination were important to scientific discovery.")
    print()
    input("Press Enter to return to the menu...")


def marie_curie():
    print()
    print("MARIE CURIE")
    print()

    print("STEM Field: Physics & Chemistry")
    print()

    print("General Facts:")
    print("She was the first woman to win a Nobel Prize.")
    print("She remains the only person in history to win Nobel Prizes in two different scientific fields.")
    print()

    print("Major Achievements:")
    print("She developed mobile radiography units during World War I, known as 'Little Curies'.")
    print("She formulated the theory of radioactivity, laying groundwork for modern nuclear physics and oncology treatments.")
    print()

    print("Interesting Fact:")
    print("Her personal notebooks from the 1890s are still radioactive and are safely stored in lead-lined boxes.")
    print()
    input("Press Enter to return to the menu...")


def katherine_johnson():
    print()
    print("KATHERINE JOHNSON")
    print()

    print("STEM Field: Mathematics & Aerospace Engineering")
    print()

    print("General Facts:")
    print("She was a child prodigy who started high school at the age of 10 and graduated from college at 18.")
    print("She worked as a 'human computer' at NASA's precursor agency, NACA, before electronic computers became standard.")
    print()

    print("Major Achievements:")
    print("She calculated flight trajectories and orbital mechanics for critical space missions, including Alan Shepard's first American spaceflight and John Glenn's orbital flight.")
    print("She provided backup manual calculations that helped ensure the safe return of the Apollo 11 lunar module from the Moon.")
    print()

    print("Interesting Fact:")
    print("John Glenn famously trusted her calculations before his orbital flight and asked engineers to have her check the numbers.")
    print()
    input("Press Enter to return to the menu...")


while True:
    print()
    print("WOMEN IN STEM")
    print()
    print("1. Ada Lovelace")
    print("2. Marie Curie")
    print("3. Katherine Johnson")
    print("4. Quit")
    print()

    choice = input("Enter your choice: ")

    if choice == "1":
        ada_lovelace()

    elif choice == "2":
        marie_curie()

    elif choice == "3":
        katherine_johnson()

    elif choice == "4":
        print()
        print("Goodbye!")
        break

    else:
        print()
        print("Invalid choice. Please try again.")