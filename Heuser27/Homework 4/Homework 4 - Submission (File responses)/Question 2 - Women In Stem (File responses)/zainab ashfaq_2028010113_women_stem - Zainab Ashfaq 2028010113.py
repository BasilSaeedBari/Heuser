def show_woman_1():
    print("-" * 30)
    print("katherine johnson")
    print()
    print("She started high school at age 10 and graduated from college summa cum laude at just 18.")
    print("Astronaut John Glenn refused to fly his 1962 orbital mission until Katherine verified the computer's calculations by hand.")
    print("She calculated the launch window and flight trajectories that sent Apollo 11 to the Moon in 1969.")
    print("In 1960, she became the first woman in her NASA division to receive official co-author credit on a research paper.")
    print("She was awarded the Presidential Medal of Freedom by President Barack Obama in 2015.")
    print("-" * 30)
def show_woman_2():
    print("-" * 30)
    print("ada lovelace")
    print()
    print("She published the world's first machine algorithm, designed to compute Bernoulli numbers on Charles Babbage's mechanical Analytical Engine.")
    print("She was the only legitimate child of the famous Romantic poet Lord Byron, though her mother raised her strictly focused on mathematics to suppress any 'poetic madness.'")
    print("She envisioned that machines could process more than just numbers, predicting modern computing by realizing they could manipulate music, text, or graphics.")
    print("She referred to her unique approach to science as 'poetical science,' combining mathematical logic with creative imagination.")
    print("-" * 30)

def show_woman_3():
    print("-" * 30)
    print("grace hopper")
    print()
    print("She developed the world's first compiler, translating human-readable English instructions into machine code.")
    print("Her pioneering work on machine-independent programming languages led directly to the creation of COBOL, one of the earliest high-level programming languages.")
    print("She popularized the term 'debugging' after her team found a real moth stuck in a relay of the Harvard Mark II computer in 1947.")
    print("She was the first woman to earn a Ph.D. in mathematics from Yale University, completing it in 1934.")
    print("-" * 30)

def show_menu():
    print()
    print("welcome this program is about the most outstanding women in history")
    print("1 - katherine johnson ")
    print("2 - ada lovelace")
    print("3 - grace hoppers")
    print("quit - exit")

running = True
while running:
    show_menu()
    choice = input("Your choice: ").lower()

    if choice == "1":
        show_woman_1()
    elif choice == "2":
        show_woman_2()
    elif choice == "3":
        show_woman_3()
    elif choice == "quit" or choice == "exit":
        print("Goodbye!")
        running = False
    else:
        print("Invalid choice, try again.")