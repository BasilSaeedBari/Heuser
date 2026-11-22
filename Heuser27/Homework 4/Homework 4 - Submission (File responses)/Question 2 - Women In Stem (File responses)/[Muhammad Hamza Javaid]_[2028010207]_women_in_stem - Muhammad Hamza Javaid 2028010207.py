QuesNo = 1
correct_answer = 0
exit = False
    
Ques1 = "Who is known for their work in COBOL, an early High level programming language, who's work has played a significant role in making coding accesible in the english language?"
Ques2 = "Who wrote the world's first computer algorithm, earning her place as the world's first computer programmer?"
Ques3 = "Who is the only person honored with a nobel prize in two different scientific fields?"
Ques4 = "Who played a role in laying the foundational framework for modern day WI-FI, GPS and blutooth, while simultanously being a well renowned actoress?"
Ques5 = "Who is known for their immense work in radioactivity along with the discoveries of polonium and radium?"

personality1 = "Marie Curie"
personality2 = "Ada Lovelace"
personality3 = "Grace Hopper"
personality4 ="Hedy Lamarr"


def endgame():
    global exit
    Cont = input("Do you wish to continue, Yes or No: ")
    if Cont == "No" or Cont == "no":
        exit = True

def options():
    print("Write the corresponding number of your answer")
    print("1", " for ",personality1)
    print("2", " for ",personality2)
    print("3", " for ",personality3)
    print("4", " for ",personality4)
    print(" ")
    print("Your Question is: ")

def answer_check(answer, correct_answer):
    if answer == correct_answer:
        print(" ")
        print("Thats Correct!")
    else:
        print(" ")
        print("Wrong answer!")
        

def NextQues():
    global QuesNo
    match QuesNo:
        case 1:
            correct_answer = 3
            options()
            print(" ")
            answer = int(input(Ques1 + " (1,2,3 or 4): "))
            answer_check(answer, correct_answer)
            QuesNo += 1
        case 2:
            correct_answer = 2
            options()
            print(" ")
            answer = int(input(Ques2 + " (1,2,3 or 4): "))
            answer_check(answer, correct_answer)
            QuesNo += 1
        case 3:
            correct_answer = 1
            options()
            print(" ")
            answer = int(input(Ques3 + " (1,2,3 or 4): "))
            answer_check(answer, correct_answer)
            QuesNo += 1
        case 4:
            correct_answer = 4
            options()
            print(" ")
            answer = int(input(Ques4 + " (1,2,3 or 4): "))
            answer_check(answer, correct_answer)
            QuesNo += 1
        case 5:
            correct_answer = 1
            options()
            print(" ")
            answer = int(input(Ques5 + " (1,2,3 or 4): "))
            aanswer_check(answer, correct_answer)
            QuesNo += 1
            
def Play_Game():
    global exit
    play = input("Do you want to play the Multiple Choice (Women in Stem)? ( Y / N ): ")
    print(" ")
    if play == "Y" or play == "y":
        while not exit and QuesNo < 5:
            NextQues()
            endgame()
    print("Thats all, Thanks for playing!")
        

Play_Game()


