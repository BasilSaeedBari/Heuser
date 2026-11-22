def show_menu():
    print("\n" + "=" * 35)
    print("       WOMEN IN STEM")
    print("=" * 35)
    print("1. Ada Lovelace")
    print("2. Grace Hopper")
    print("3. Katherine Johnson")
    print("4. Marie Curie")
    print("5. Play a quiz")
    print("6. Quit")
    print("=" * 35)


def show_profile(choice):
    if choice == "1":
        print("\nADA LOVELACE")
        print("Ada Lovelace was a mathematician.")
        print("She wrote an algorithm for Charles Babbage's")
        print("proposed Analytical Engine in the 1840s.")
        print("She is often regarded as the first computer programmer.")

    elif choice == "2":
        print("\nGRACE HOPPER")
        print("Grace Hopper was an American computer scientist.")
        print("She helped develop early computer programming languages.")
        print("She also helped popularize the term 'debugging'.")

    elif choice == "3":
        print("\nKATHERINE JOHNSON")
        print("Katherine Johnson was an American mathematician.")
        print("Her calculations helped NASA plan spaceflight missions.")
        print("Her work contributed to the success of early US spaceflight.")

    elif choice == "4":
        print("\nMARIE CURIE")
        print("Marie Curie was a physicist and chemist.")
        print("She conducted pioneering research on radioactivity.")
        print("She won Nobel Prizes in Physics and Chemistry.")

    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")


def check_answer(user_answer, correct_answer):
    if user_answer.lower() == correct_answer.lower():
        print("Correct! Well done!")
        return True
    else:
        print("Not quite. The correct answer is", correct_answer)
        return False


def play_quiz():
    score = 0

    print("\nWELCOME TO THE WOMEN IN STEM QUIZ!")
    print("Answer these four questions.\n")

    print("1. Who is often regarded as the first computer programmer?")
    answer = input("Your answer: ")
    if check_answer(answer, "Ada Lovelace"):
        score = score + 1

    print("\n2. Who helped develop early programming languages?")
    answer = input("Your answer: ")
    if check_answer(answer, "Grace Hopper"):
        score = score + 1

    print("\n3. Whose calculations helped NASA's space missions?")
    answer = input("Your answer: ")
    if check_answer(answer, "Katherine Johnson"):
        score = score + 1

    print("\n4. Who won Nobel Prizes in Physics and Chemistry?")
    answer = input("Your answer: ")
    if check_answer(answer, "Marie Curie"):
        score = score + 1

    print("\nYour final score is", score, "out of 4.")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            show_profile("1")
        elif choice == "2":
            show_profile("2")
        elif choice == "3":
            show_profile("3")
        elif choice == "4":
            show_profile("4")
        elif choice == "5":
            play_quiz()
        elif choice == "6":
            print("Thank you for learning about Women in STEM!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


main()