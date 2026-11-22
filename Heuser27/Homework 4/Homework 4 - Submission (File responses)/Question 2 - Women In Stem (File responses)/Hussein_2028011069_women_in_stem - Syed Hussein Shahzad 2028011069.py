def display_biography(name, biography):
    print("\n" + "=" * 45)
    print("WOMEN IN STEM VIRTUAL MUSEUM")
    print("=" * 45)
    print("Name:", name)
    print("-" * 45)
    print(biography)
    print("=" * 45)


def find_woman(user_input):
    name = user_input.strip().lower()

    if name == "nergis mavalvala":
        biography = """

    Nergis Mavalvala is a renowned Pakistani-born American physicist who was born in Lahore, Pakistan, and grew up in Karachi.
    From a young age, she showed a strong interest in mathematics and science. She moved to the United States to study at Wellesley College,
    where she earned a degree in physics and astronomy, and later completed her PhD in physics at the Massachusetts Institute of Technology (MIT).
She is best known for her important role in the LIGO project, which made the first direct detection of gravitational waves in 2015, announced
in 2016. These waves are tiny ripples in space and time caused by powerful cosmic events, such as colliding black holes.
Her research helped scientists better understand the universe. In 2020, she became the first woman to serve as dean of MIT’s School of Science.
She has received several prestigious awards, including the MacArthur Fellowship in 2010. Nergis Mavalvala is an inspiration to many,
especially women and young students in Pakistan, showing that dedication and hard work can lead to remarkable achievements.
        """
        display_biography("Nergis Mavalvala", biography)

    elif name == "katherine johnson":
        biography = """
        Katherine Johnson was a famous African American mathematician born on August 26, 1918, in West Virginia, USA.
        From a young age, she had a great love for mathematics and was very talented in solving complex problems.
        She graduated from West Virginia State College in 1937 with degrees in mathematics and French. In 1953, she began working
        at NASA’s predecessor, NACA, where she used her mathematical skills to help scientists and engineers with space research.
        she is best known for calculating the flight paths of astronauts during America’s early space missions.
        Her calculations helped send Alan Shepard into space in 1961 and supported John Glenn’s historic journey around Earth in 1962.
        She also contributed to NASA’s Apollo program, which sent astronauts to the Moon. Despite facing racial discrimination and challenges
        as a woman in science, Katherine continued to work hard and make important contributions. In 2015, she received the
        Presidential Medal of Freedom, one of America’s highest civilian honors. She passed away on February 24, 2020, at the age of 101.
        Her life continues to inspire students, especially girls, to pursue mathematics, science, and their dreams.



        """
        display_biography("Katherine Johnson", biography)

    elif name == "grace hopper":
        biography = """
        Grace Hopper was a famous American mathematician, computer scientist, and U.S. Navy officer born on December 9, 1906,
        in New York City, USA. From an early age, she was curious about how things worked and had a strong interest in mathematics.
        She graduated from Vassar College in 1928 and later earned her master’s degree and PhD in mathematics from Yale University.
        During World War II, she joined the U.S. Navy and became one of the first programmers of the Harvard Mark I computer.
        She is best known for helping develop early computer programming languages. She created FLOW-MATIC, a programming language
        that influenced the development of COBOL, which made it easier for people to give instructions to computers using words similar
        to English. She also helped popularize the term “debugging” in computing. Throughout her career, she broke barriers for women
        in science and technology and eventually retired from the Navy in 1986 with the rank of rear admiral. She passed away on
        January 1, 1992, at the age of 85. Grace Hopper’s life continues to inspire people around the world to explore computer science,
        think creatively, and never stop learning.
        """
        display_biography("Grace Hopper", biography)

    else:
        print("\nSorry, this person is not in our museum.")
        print("Please enter one of the three names listed.")


def main():
    print("=" * 45)
    print("     WOMEN IN STEM: VIRTUAL MUSEUM")
    print("=" * 45)
    print("Explore the achievements of three women in STEM!")

    while True:
        print("\nAvailable biographies:")
        print("1. Nergis Mavalvala")
        print("2. Katherine Johnson")
        print("3. Grace Hopper")
        print("Type 'quit' to exit.")

        user_input = input("\nEnter a woman's name: ")

        if user_input.strip().lower() == "quit":
            print("\nThank you for visiting the museum!")
            break

        else:
            find_woman(user_input)


main()