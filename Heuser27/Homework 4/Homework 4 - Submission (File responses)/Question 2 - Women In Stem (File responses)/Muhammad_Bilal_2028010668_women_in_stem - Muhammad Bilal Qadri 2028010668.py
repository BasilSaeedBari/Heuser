print("-"*30 ,"Welcome to virtual Museum" ,"-"*30)


print("This is a virtual museum where you will read about 5 of the famous women in history")
print("")
    
def grace_hopper():
    print("-" * 30 ,"Grace Hopper","-"*30)
    print("Early Life:")
    
    print("""Grace Brewster Murray was born in New York on 9th of December 1906.She studied maths and astronomy in Vassar College.
She recieved her maths degree from Yale university in 1930 and on the same year she married Vincent Foster Hopper recieving the name Grace Hopper.(she got divorced in 1945 but stll kept this name)
In 1931,she started teaching at Vassar College,while studying in Yale and finally got her Ph.D. in mathematics becoming one of the few women to earn such a degree.
During WWII she joined US Navy Reserve and was commisioned a lieutenant in June 1944.
However her main accomplishment was in computer.""")
    print("-" * 30)
    print("Main accomplishment:")
    print("""
During WWII Hopper was assigned to the Beareu of Ordanace Computation project at Harvard University where she learned to program Mark I.
After the war she remained a reserve in US Navy reserve where she worked with Mark II and Mark III computers.
Wanting to work with computers, in 1949 she moved to a private industry, first with the 'Eckert-Mauchly Computer' then with 'Remington Rand' where she oversaw programming for UNIVAC computers.
In 1952, her term created the first compiler for computer languages. This compiler was a precursor for the Common Business Oriented Language(COBOL).
""")
    print("-" * 30)
    print("Last years and death:")
    print("""
    In 1986 Hopper retired from the navy at the age og 79 becoming the oldest serving officer. Even after retiring hopper stayed in the computer industry for few more years.
    She was awarded the National Medal of Technology in 1991-becoming the first female individual recipient of honor.
    At the age of 85, she died in the Arlington, Virginia, on January 1, 1992.""")


def chien():
    print('-'*30,"Chien-Shiung Wu",'-'*30)
    print("Early life:")
    
    print("""
Born in a small town near Shangai, Wu attended a school started by her father, who believed in education for girls. Wu went on to study physics at a university in Shangai.
After graduation, she became a research assistant when her supervisor encouraged her to pursue advance education in America.
In 1906 she arrived in San Fransisco, and enrolled in the University of California where she obtained her Ph.D in 1940. She married Luke Yuan in
1942.
""")
    print("-"*30)
    print("Scientific Contribution:")
    print("""
In 1944, Wu joined the Manhattan Project at the Subsitute Alloy Materials(SAM) lab at Columbia University, focusing on radiation detectors.
Wu helped indetify Xenon-135 poisoning after a reactor at hanford mysteriously shut down.In 1949 Wu and her student performed a
grounbreaking experiment on quantum entanglement in the basement of Pupin Hall at Columbia. Wu also began investigating beta decay, which
occurs when the nucleus of one element changes into another element. She made several contibutions, including making the first confirmation
of Enrico Fermi's theory of beta decay. In 1958, her research helped answer important biological questions about blood and sickle cell anemia.
She was also the first women president of the American Physical Society. Her awards include the National Medal of Science, the Comstock Prize, and the
first honory doctorate awareded to a women at Princeton University. She also won the Wolf Prize in Physics in 1978.
She died in New York City, on Febuary 16, 1997.""")

    
def katherine():
    print('-'*30,"Katherine Johnson",'-'*30)
    print("Early Life:")
    print("""
Born in 1918 in White Sulpher Springs, West Virginia, Johnson's love for mathematics was inherint. At a young age she was ready and anxious to go to school.
Johnson was so excelled that she began her studies from the second grade, and by the age of 10 she was inn highschool. At the age of 15 she gaduated high school and entered West Virginia State College.
At West Virginia she was immersed in academia and the mathematics program. She loved being surrounded by smart people. At the age of 18, Johnson graduated with Bachelor of Science degrees in Mathematics and French.
After graduating she started teaching, but shortly she got married and stopped.""")
    print("-"*30)
    print("Contributions")
    print("""
Johnson began working for NACA(before NASA was named NACA back in the days) in 1953. She worked with the agency until 1986. During her tenure at NASA, Johnson recieved many awards. Among them were the NASA Lunar Orbiter Award and three NASA Special Achievement awards.
She was named mathematican of the year in 1997 by the National Technical Association. In addition to these NASA awards, Johnson was honored with an honorary Doctor of Law degree from the State University of New York and honorary Doctor of Science degrees from Capitol College in
Maryland and Old Dominion University in Virginia. Katherine Johnson passed from this life on the morning of Feb. 24, 2020. She was 101 years old.""")
    


    

    
while True:
    
    choice = int(input("Type '1' for 'Grace Hopper' biography, '2' for 'Chien-Shiung' Wu, '3' for 'Katherine Johnson', '4' to exit: "))
    match choice:
        case 1:
            grace_hopper()
        case 2:
            chien()
        case 3:
            katherine()
        case 4:
            print("Goodbye!")
            break
        case _:
            print("Invalid option")
            
        

