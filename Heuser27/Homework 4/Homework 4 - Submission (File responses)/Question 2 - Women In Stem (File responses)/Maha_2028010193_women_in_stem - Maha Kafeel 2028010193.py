def display_ada():
    print("Ada Lovelace was the first computer programmer[cite: 2].")

def display_grace():
    print("Grace Hopper invented the first compiler[cite: 2].")

def display_katherine():
    print("Katherine Johnson was a NASA mathematician whose orbital mechanics calculations were critical[cite: 2].")

def main():
    running = True
    while running:
        user_choice = input("Type ada, grace, katherine, or quit: ").strip().lower()
        if user_choice == "quit" or user_choice == "exit":
            running = False
        elif user_choice == "ada":
            display_ada()
        elif user_choice == "grace":
            display_grace()
        elif user_choice == "katherine":
            display_katherine()
        else:
            print("Invalid input.")

main()