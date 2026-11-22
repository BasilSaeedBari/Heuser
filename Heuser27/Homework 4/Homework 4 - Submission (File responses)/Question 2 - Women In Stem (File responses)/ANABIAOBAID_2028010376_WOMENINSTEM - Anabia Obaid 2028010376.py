def display_marie_curie():
    print("\n===== MARIE CURIE =====")
    print("Field: Physics and Chemistry")
    print("1. She was the first woman to win a Nobel Prize.")
    print("2. She won Nobel Prizes in Physics and Chemistry.")
    print("3. She discovered the elements polonium and radium.")
    print("4. She pioneered research into radioactivity.")
    print("5. She became a professor at the University of Paris.")
    print("6. During World War I, she helped develop mobile X-ray units.")
    print("7. She shared the 1903 Nobel Prize in Physics.")
    print("8. She won the 1911 Nobel Prize in Chemistry.")
    print("9. She named the element polonium after Poland.")
    print("10. Her research helped advance medical and scientific knowledge.")


def display_ada_lovelace():
    print("\n===== ADA LOVELACE =====")
    print("Field: Mathematics and Computer Science")
    print("1. She was born in 1815 in London.")
    print("2. Her father was the poet Lord Byron.")
    print("3. She worked with Charles Babbage's ideas for a mechanical computer.")
    print("4. The machine was called the Analytical Engine.")
    print("5. She wrote a published algorithm intended for the machine.")
    print("6. She is widely regarded as the first computer programmer.")
    print("7. Her notes described how a machine could manipulate symbols.")
    print("8. She recognized that computers could do more than calculations.")
    print("9. She was interested in mathematics from a young age.")
    print("10. Her ideas influenced the history of computing.")


def display_katherine_johnson():
    print("\n===== KATHERINE JOHNSON =====")
    print("Field: Mathematics and Aerospace")
    print("1. She was an American mathematician.")
    print("2. She worked for NASA and its predecessor, NACA.")
    print("3. She calculated flight paths for early space missions.")
    print("4. Her calculations supported Project Mercury.")
    print("5. John Glenn requested that her calculations be checked")
    print("   before his orbital flight in 1962.")
    print("6. She contributed to calculations for the Apollo program.")
    print("7. She studied mathematics at West Virginia State College.")
    print("8. She graduated from college at age 18.")
    print("9. She received the Presidential Medal of Freedom in 2015.")
    print("10. Her work helped advance human spaceflight.")


def run_quiz():
    score = 0

    questions = [
        [
            "Who discovered radium and polonium?",
            "1. Ada Lovelace",
            "2. Marie Curie",
            "3. Katherine Johnson",
            "2"
        ],
        [
            "Who is widely regarded as the first computer programmer?",
            "1. Marie Curie",
            "2. Katherine Johnson",
            "3. Ada Lovelace",
            "3"
        ],
        [
            "Who worked as a mathematician for NASA?",
            "1. Katherine Johnson",
            "2. Marie Curie",
            "3. Ada Lovelace",
            "1"
        ],
        [
            "Which scientist pioneered research into radioactivity?",
            "1. Ada Lovelace",
            "2. Marie Curie",
            "3. Katherine Johnson",
            "2"
        ],
        [
            "What was the name of Babbage's proposed mechanical computer?",
            "1. Analytical Engine",
            "2. Space Engine",
            "3. Difference Calculator",
            "1"
        ],
        [
            "Which scientist contributed to early spaceflight calculations?",
            "1. Marie Curie",
            "2. Ada Lovelace",
            "3. Katherine Johnson",
            "3"
        ],
        [
            "In which two fields did Marie Curie win Nobel Prizes?",
            "1. Literature and Peace",
            "2. Physics and Chemistry",
            "3. Mathematics and Medicine",
            "2"
        ],
        [
            "Who was the father of Ada Lovelace?",
            "1. Charles Babbage",
            "2. John Glenn",
            "3. Lord Byron",
            "3"
        ],
        [
            "Which award did Katherine Johnson receive in 2015?",
            "1. Presidential Medal of Freedom",
            "2. Nobel Prize in Physics",
            "3. Turing Award",
            "1"
        ],
        [
            "What did Marie Curie help develop during World War I?",
            "1. Mechanical computers",
            "2. Mobile X-ray units",
            "3. Space rockets",
            "2"
        ]
    ]

    print("\n===== WOMEN IN STEM QUIZ =====")
    print("Enter 1, 2, or 3 for each answer.")

    for question in questions:
        print("\n" + question[0])
        print(question[1])
        print(question[2])
        print(question[3])

        answer = input("Your answer: ")

        if answer == question[4]:
            print("Correct!")
            score = score + 1
        else:
            print("Not quite. The correct option is", question[4] + ".")

    print("\n===== QUIZ RESULTS =====")
    print("Your score:", score, "out of", len(questions))

    if score >= 8:
        print("Excellent work!")
    elif score >= 5:
        print("Good effort! Keep learning.")
    else:
        print("Keep practising. You can try again!")


def main():
    choice = ""

    while choice != "5":
        print("\n===== WOMEN IN STEM MUSEUM =====")
        print("1. Learn about Marie Curie")
        print("2. Learn about Ada Lovelace")
        print("3. Learn about Katherine Johnson")
        print("4. Take the 10-question quiz")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            display_marie_curie()
        elif choice == "2":
            display_ada_lovelace()
        elif choice == "3":
            display_katherine_johnson()
        elif choice == "4":
            run_quiz()
        elif choice == "5":
            print("Thank you for visiting the Women in STEM Museum!")
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


main()