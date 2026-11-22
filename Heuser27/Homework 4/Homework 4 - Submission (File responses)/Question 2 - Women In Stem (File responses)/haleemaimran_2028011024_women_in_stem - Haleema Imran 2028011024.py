# Custom Function for Ada Lovelace
def display_ada():
  print("\n" + "=" * 40)
  print("ADA LOVELACE")
  print("=" * 40)
  print("Widely considered the first computer programmer.")
  print(
      "She wrote an algorithm for Charles Babbage's mechanical computer, the"
      " Analytical Engine, in the 1840s."
  )


# Custom Function for Grace Hopper
def display_grace():
  print("\n" + "=" * 40)
  print("GRACE HOPPER")
  print("=" * 40)
  print("A pioneering US Navy Rear Admiral and computer scientist.")
  print(
      "She invented the first compiler-related tools and was a major force"
      " behind the development of COBOL."
  )


# Custom Function for Katherine Johnson
def display_katherine():
  print("\n" + "=" * 40)
  print("KATHERINE JOHNSON")
  print("=" * 40)
  print("A brilliant NASA mathematician and physicist.")
  print(
      "Her orbital mechanics calculations were critical to the success of"
      " crewed spaceflights like Apollo 11."
  )


def main():
  print("Welcome to the Women in STEM Virtual Museum!")

  # 1. Main Loop (Runs continuously until user types 'quit' or 'exit')
  while True:
    print("\nSelect a figure to learn about:")
    print("1. Ada Lovelace")
    print("2. Grace Hopper")
    print("3. Katherine Johnson")
    print("Type 'quit' or 'exit' to close the program.")

    user_choice = input("\nEnter your choice: ").strip().lower()

    # 2. Conditionals to handle user input
    if user_choice in ["quit", "exit"]:
      print("\nThank you for visiting the museum. Goodbye!")
      break
    elif user_choice == "1" or user_choice == "ada":
      display_ada()
    elif user_choice == "2" or user_choice == "grace":
      display_grace()
    elif user_choice == "3" or user_choice == "katherine":
      display_katherine()
    else:
      print("\nInvalid choice. Please enter 1, 2, 3, or type 'quit' to exit.")


# Run the main program loop
if __name__ == "__main__":
  main()