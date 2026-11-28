def display_ada_lovelace():
    print("\n--- Ada Lovelace (1815–1852) ---")
    print("Role: First Computer Programmer")
    print("Achievement: Wrote the first algorithm intended for Babbage's Analytical Engine")
    print("and saw that machines could process symbols and music, not just numbers.")


def display_grace_hopper():
    print("\n--- Grace Hopper (1906–1992) ---")
    print("Role: Computer Scientist & U.S. Navy Rear Admiral")
    print("Achievement: Built the first compiler and helped pioneer English-like")
    print("programming languages (leading to COBOL).")


def display_katherine_johnson():
    print("\n--- Katherine Johnson (1918–2020) ---")
    print("Role: NASA Mathematician & Orbital Mechanics Specialist")
    print("Achievement: Calculated trajectory and launch windows for Project Mercury")
    print("and Apollo 11, verifying orbital paths by hand.")


def show_menu():
    print("\n=== Women in STEM Virtual Museum ===")
    print("Type a name or number to explore:")
    print("  1. Ada Lovelace")
    print("  2. Grace Hopper")
    print("  3. Katherine Johnson")
    print("Type 'quit' or 'exit' to leave.")


def run_museum():
    while True:
        show_menu()
        choice = input("\nYour choice: ").strip().lower()

        if choice in ("quit", "exit"):
            print("\nThanks for visiting the Women in STEM Virtual Museum!")
            break
        elif choice in ("1", "ada", "ada lovelace"):
            display_ada_lovelace()
        elif choice in ("2", "grace", "grace hopper"):
            display_grace_hopper()
        elif choice in ("3", "katherine", "katherine johnson"):
            display_katherine_johnson()
        else:
            print("\nUnrecognized input. Please choose 1–3, a name, or 'quit'/'exit'.")


if __name__ == "__main__":
    run_museum()