def check_answer(user_input, correct_answer):
    if user_input.lower() == correct_answer.lower():
        return True
    else:
        return False

def ask_guess(correct_answer):
    guess = input("Your guess (Enter = next clue, exit = quit): ")
    if guess.lower() == "exit":
        return "exit"
    if guess == "":
        return "next"
    if check_answer(guess, correct_answer):
        print("Correct!")
        return "correct"
    print("Try again!")
    return "next"

def display_ada_lovelace():
    print("I wrote an algorithm for a machine that was never built in my lifetime, making me the world's first computer programmer.")
    result = ask_guess("Ada Lovelace")
    if result != "next":
        return result
    print("My famous collaborator was Charles Babbage, but I saw beyond his mathematical calculations to envision machines creating music and art.")
    result = ask_guess("Ada Lovelace")
    if result != "next":
        return result
    print("My father was the famous poet Lord Byron, but my mother made sure I studied logic and mathematics instead.")
    result = ask_guess("Ada Lovelace")
    if result == "next":
        print("The answer was Ada Lovelace")
    return result

def display_katherine_johnson():
    print("Before supercomputers existed, NASA relied on my precise manual calculations as a human 'computer' to send astronauts into space.")
    result = ask_guess("Katherine Johnson")
    if result != "next":
        return result
    print("John Glenn famously refused to fly his historic orbital mission until I personally double-checked the computer's flight numbers.")
    result = ask_guess("Katherine Johnson")
    if result != "next":
        return result
    print("My incredible journey at NASA as a pioneering Black mathematician was showcased in the book and film Hidden Figures.")
    result = ask_guess("Katherine Johnson")
    if result == "next":
        print("The answer was Katherine Johnson")
    return result

def display_Rosalind_franklin():
    print("My expert work in X-ray crystallography captured 'Photo 51,' revealing the double-helix shape of life's building blocks.")
    result = ask_guess("Rosalind Franklin")
    if result != "next":
        return result
    print("While my work was crucial to uncovering the structure of DNA, my contributions were largely uncredited during the Nobel Prize presentation.")
    result = ask_guess("Rosalind Franklin")
    if result != "next":
        return result
    print("Beyond DNA, I made major breakthroughs researching the molecular structures of viruses, coal, and graphite.")
    result = ask_guess("Rosalind Franklin")
    if result == "next":
        print("The answer was Rosalind Franklin")
    return result

choice = ""
while choice != "exit":
    choice = display_ada_lovelace()

    if choice != "exit":
        choice = display_katherine_johnson()

    if choice != "exit":
        choice = display_Rosalind_franklin()