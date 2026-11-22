def start_quiz():
    score = 0

    # Question 1 - Ada Lovelace
    print("What is Ada Lovelace famous for?")
    print("A. Being an early computer programmer")
    print("B. Inventing the telephone")
    print("C. Discovering gravity")

    answer = input("Your answer: ")

    if answer.upper() == "A":
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is A.")

    # Question 2 - Grace Hopper
    print("What did Grace Hopper help pioneer?")
    print("A. Modern rockets")
    print("B. Computer programming languages")
    print("C. Electricity")

    answer = input("Your answer: ")

    if answer.upper() == "B":
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is B.")

    # Question 3 - Katherine Johnson
    print("Where did Katherine Johnson work?")
    print("A. NASA")
    print("B. Microsoft")
    print("C. Apple")

    answer = input("Your answer: ")

    if answer.upper() == "A":
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is A.")

    print("==============================")
    print("Quiz finished!")
    print("Your score:", score, "/ 3")
    print("==============================")


def learn_about_women():
    print("==============================")
    print("       WOMEN IN STEM")
    print("==============================")

    print("Ada Lovelace")
    print("Ada Lovelace is known for her early work on")
    print("Charles Babbage's Analytical Engine.")

    print("Grace Hopper")
    print("Grace Hopper was a computer scientist who")
    print("helped pioneer computer programming languages.")

    print("Katherine Johnson")
    print("Katherine Johnson was a mathematician whose")
    print("calculations supported NASA space missions.")


while True:
    print("================================")
    print("       WOMEN IN STEM QUIZ")
    print("================================")
    print("1. Start Quiz")
    print("2. Learn About the Women")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        start_quiz()

    elif choice == "2":
        learn_about_women()

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")