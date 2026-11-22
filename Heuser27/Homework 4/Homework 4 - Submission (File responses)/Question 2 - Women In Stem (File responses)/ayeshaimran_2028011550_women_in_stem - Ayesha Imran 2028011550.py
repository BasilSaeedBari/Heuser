def display_menu():
    print("\n" + "=" * 45)
    print("      WOMEN IN STEM - VIRTUAL MUSEUM      ")
    print("=" * 45)
    print("1. Ada Lovelace")
    print("2. Grace Hopper")
    print("3. Katherine Johnson")
    print("4. Exit Museum")
    print("-" * 45)

def display_ada_lovelace():
    print("\n--- ADA LOVELACE (1815–1852) ---")
    print("• First Computer Programmer.")
    print("• Published the first algorithm intended to be processed by a machine.")
    print("• Saw the potential of computers beyond mere calculation.")

def display_grace_hopper():
    print("\n--- GRACE HOPPER (1906–1992) ---")
    print("• Computer Scientist and US Navy Rear Admiral.")
    print("• Invented one of the first linkers and popularized machine-independent programming languages.")
    print("• Coined the term 'debugging' after finding an actual moth in a computer.")

def display_katherine_johnson():
    print("\n--- KATHERINE JOHNSON (1918–2020) ---")
    print("• Mathematician whose calculations were critical to early NASA spaceflights.")
    print("• Calculated trajectories, launch windows, and emergency return paths for Project Mercury.")
    print("• Verified computer calculations by hand for John Glenn's orbit around Earth.")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-4 or name/exit): ").strip().lower()
        
        if choice in ["1", "ada", "ada lovelace"]:
            display_ada_lovelace()
        elif choice in ["2", "grace", "grace hopper"]:
            display_grace_hopper()
        elif choice in ["3", "katherine", "katherine johnson"]:
            display_katherine_johnson()
        elif choice in ["4", "exit", "quit"]:
            print("\nThank you for visiting the Women in STEM Museum! Goodbye.")
            break
        else:
            print("\nInvalid choice. Please pick an option from the menu.")

if __name__ == "__main__":
    main()