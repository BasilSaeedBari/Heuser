
def display_biography(name, biography):
    print("\n" + "=" * 45)
    print("PAKISTANI WOMEN IN STEM VIRTUAL MUSEUM")
    print("=" * 45)
    print("Name:", name)
    print("-" * 45)
    print(biography)
    print("=" * 45)


def find_woman(user_input):
    name = user_input.strip().lower()

    if name == "nergis mavalvala":
        biography = """
Nergis Mavalvala is a Pakistani-born astrophysicist.
She was born in Lahore and grew up in Karachi.

She is a professor of astrophysics at the
Massachusetts Institute of Technology (MIT).

Her research focuses on gravitational waves,
which are ripples in space-time.

She was part of the scientific team that detected
gravitational waves for the first time in 2015.
The discovery was announced in 2016.

Her work has helped scientists study the universe
and test Einstein's theory of general relativity.
"""
        display_biography("Nergis Mavalvala", biography)

    elif name == "tasneem zehra husain":
        biography = """
Tasneem Zehra Husain is a Pakistani theoretical
physicist, author, and science educator.

She earned a PhD in physics from Stockholm
University in Sweden.

She is recognised as Pakistan's first female
string theorist.

String theory is a theoretical approach that
attempts to explain the fundamental nature
of particles and forces in the universe.

She also works to communicate complex scientific
ideas to students and the general public.
"""
        display_biography("Tasneem Zehra Husain", biography)

    elif name == "sania nishtar" or name == "sania nisar":
        biography = """
Dr. Sania Nishtar is a Pakistani physician and
public-health expert.

She has worked on healthcare policy and improving
health services in Pakistan.

Her work focuses on public health, healthcare
systems, and social support programmes.

She founded Heartfile, a Pakistani health-focused
organisation that works on health policy and
healthcare challenges.

Her career demonstrates how medicine, research,
and evidence-based decisions can improve
healthcare for communities.
"""
        display_biography("Dr. Sania Nishtar", biography)

    else:
        print("\nSorry, this person is not in our museum.")
        print("Please enter one of the three names listed.")


def main():
    print("=" * 45)
    print(" PAKISTANI WOMEN IN STEM: VIRTUAL MUSEUM")
    print("=" * 45)
    print("Explore the achievements of three Pakistani")
    print("women in science, technology, and medicine!")

    while True:
        print("\nAvailable biographies:")
        print("1. Nergis Mavalvala")
        print("2. Tasneem Zehra Husain")
        print("3. Sania Nishtar")
        print("Type 'quit' or 'exit' to leave.")

        user_input = input("\nEnter a woman's name: ")

        if user_input.strip().lower() == "quit" or \
           user_input.strip().lower() == "exit":
            print("\nThank you for visiting the museum!")
            break

        else:
            find_woman(user_input)


main()
