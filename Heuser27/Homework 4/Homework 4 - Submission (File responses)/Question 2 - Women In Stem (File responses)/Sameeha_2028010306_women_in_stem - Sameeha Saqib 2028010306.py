LINE = "-" * 50

PROFILES = {
    "curie": {
        "name": "Marie Curie (1867-1934)",
        "field": "Physics and Chemistry",
        "facts": [
            "Born in Warsaw, Poland, and later worked in France.",
            "She was the first woman to win a Nobel Prize.",
            "She is the only person to win Nobel Prizes in two different sciences: Physics (1903) and Chemistry (1911).",
            "With her husband Pierre she discovered the elements polonium and radium.",
            "In World War I she helped set up mobile X-ray units to treat wounded soldiers.",
        ],
    },
    "franklin": {
        "name": "Rosalind Franklin (1920-1958)",
        "field": "Chemistry and X-ray crystallography",
        "facts": [
            "A British scientist who used X-rays to study the structure of molecules.",
            "Her X-ray image known as Photo 51 gave key evidence for the double-helix shape of DNA.",
            "She also did important research on coal and on viruses.",
            "She died at only 37, and her contribution to the DNA discovery was recognised widely only later.",
        ],
    },
    "hamilton": {
        "name": "Margaret Hamilton (born 1936)",
        "field": "Computer Science and Software Engineering",
        "facts": [
            "She led the MIT team that wrote the flight software for NASA's Apollo missions.",
            "She helped popularise the term 'software engineering'.",
            "During the Apollo 11 landing, her team's software handled a computer overload by prioritising the most important tasks.",
            "She received the Presidential Medal of Freedom in 2016.",
        ],
    },
    "wu": {
        "name": "Chien-Shiung Wu (1912-1997)",
        "field": "Experimental Physics",
        "facts": [
            "A Chinese-American physicist nicknamed the 'First Lady of Physics'.",
            "Her 1956 experiment using cobalt-60 showed that parity is not conserved in weak nuclear interactions.",
            "She worked on the Manhattan Project, helping with uranium enrichment.",
            "Her male colleagues received the 1957 Nobel Prize for the theory, but she did not, which many consider an oversight.",
        ],
    },
}


def print_header(title):
    print()
    print(LINE)
    print(title.upper())
    print(LINE)


def show_menu():
    print_header("Women in STEM Museum")
    print("Type a name to read a biography:")
    print("  curie / franklin / hamilton / wu")
    print("Or type quit to leave.")


def display_profile(key):
    person = PROFILES[key]
    print_header(person["name"])
    print("Field:", person["field"])
    print()
    for fact in person["facts"]:
        print(" *", fact)


def main():
    running = True
    while running:
        show_menu()
        choice = input("\nYour choice: ").strip().lower()

        if choice in PROFILES:
            display_profile(choice)
        elif choice == "quit" or choice == "exit":
            print("\nThanks for visiting. Goodbye!")
            running = False
        else:
            print("\nSorry, I didn't recognise that. Please try again.")


main()