def marie_curie():
    print("==== MADAM CURIE====")
    print()
    print("==== Early life and Education ====")
    print()
    print("Marie Curie was born Maria Skłodowska in 1867 in Warsaw, Poland. At a time when women faced major barriers to higher education, she moved to Paris and studied at the University of Paris (Sorbonne), earning degrees in physics and mathematics. Her determination to pursue scientific education became an important part of her legacy.")
    print("==== Key Achievements ====")
    print()
    print("Curie became one of the most important scientists in the history of physics and chemistry through her pioneering research into radioactivity. Working with Pierre Curie, she investigated radioactive materials and helped discover the elements polonium and radium. Her work fundamentally changed scientists' understanding of atoms and radiation and later contributed to developments in medical applications of radiation.")
    print()
    print("==== Direct Role in STEM ====")
    print()
    print("Curie's direct contribution was as a physicist and chemist conducting experimental research. She developed methods for studying radioactive substances and isolated radioactive materials for further investigation. Her scientific work helped establish radioactivity as an important field of research rather than simply being an unusual property of certain materials.")
    print()
    print("==== Awards and Recognition ====")
    print()
    print("Marie Curie received the 1903 Nobel Prize in Physics, shared with Pierre Curie and Henri Becquerel, for research into radiation phenomena. In 1911, she won the Nobel Prize in Chemistry for her discoveries of radium and polonium and her work on radium. She remains the only person to have received Nobel Prizes in two different scientific fields.")
    print()
    print("==== Legacy ====")
    print()
    print("Curie's influence extends far beyond her own discoveries. She became an important symbol of women's participation in science and demonstrated that women could make groundbreaking contributions to fields that were overwhelmingly dominated by men. Her work also helped establish foundations for later research involving radiation and medicine.")
    
def ada_lovelace():
    print("==== ADA LOVELACE ====")
    print()
    print("==== Early life and Education ====")
    print()
    print("Augusta Ada King, Countess of Lovelace, was born in 1815 in England. She developed an interest in mathematics and science from an early age and received an unusually advanced mathematical education for a woman of her era. She later became closely associated with mathematician and inventor Charles Babbage and his proposed Analytical Engine")
    print()
    print("==== Key Achievements ====")
    print()
    print("Lovelace's most famous contribution came through her work on Babbage's Analytical Engine, an early design for a general-purpose mechanical computer. While translating an Italian article about the machine, she added extensive notes of her own. One of these notes contained an algorithm for calculating Bernoulli numbers, which is widely regarded as the first published computer program")
    print()
    print("==== Direct role in STEM ====")
    print()
    print("Her direct role was that of a mathematician and early computer-science thinker. What made Lovelace particularly remarkable was that she understood that a machine like Babbage's could potentially manipulate symbols and information beyond simple numerical calculations. Her ideas anticipated the broader concept of general-purpose computing more than a century before modern computers existed.")
    print()
    print("==== Awards and Recognition ====")
    print()
    print("Because Lovelace died in 1852, before most modern scientific award systems existed, she did not receive the major scientific prizes associated with later scientists. Instead, her recognition grew substantially after her death. Her work was rediscovered in the 20th century, and she is now widely recognized as a pioneer of computer programming. The programming language Ada was named in her honor.")
    print()
    print("==== Legacy ====")
    print()
    print("Lovelace's greatest influence was conceptual. She demonstrated that computing could be about processing information and following algorithms, rather than merely performing arithmetic. Her ideas appeared almost a century before electronic computers became practical, making her an important historical figure in computer science.")
    
    
def katherine_johnson():
    print("==== KATHERINE JOHNSON ====")
    print()
    print("==== Early life and Education ====")
    print()
    print("Katherine Johnson was born in 1918 in White Sulphur Springs, West Virginia. She showed exceptional mathematical ability from childhood and graduated from high school at just 14. She later attended West Virginia State College, where she studied mathematics and French and graduated with highest honors.")
    print()
    print("==== Key Achievements ====")
    print()
    print("Johnson became one of NASA's most important mathematical researchers. She calculated and verified flight trajectories for early American space missions, including Alan Shepard's first American human spaceflight and John Glenn's orbital mission. She also contributed to the calculations associated with the Apollo missions, including the trajectory for the 1969 Moon landing, as well as work on the Space Shuttle and Earth-observation programs.")
    print()
    print("==== Direct Role in STEM ====")
    print ()
    print("Her direct role was as a research mathematician at NASA's Langley Research Center. Before computers could reliably perform many complex calculations, mathematicians like Johnson performed calculations by hand. Her expertise became so trusted that astronaut John Glenn asked Johnson to personally verify the computer's calculations before his 1962 orbital flight.")
    print()
    print("==== Awards and Recognition ====")
    print()
    print("Johnson received numerous honors during and after her career. One of the most significant was the Presidential Medal of Freedom in 2015, America's highest civilian honor. She also received NASA awards, the Silver Snoopy Award, and the Arthur B.C. Walker II Award. In 2019, she received the Congressional Gold Medal.")
    print()
    print("==== Legacy ====")
    print()
    print("Johnson's importance goes beyond mathematics and space exploration. She broke barriers as an African American woman working in a highly segregated scientific environment. Her story became widely known through the book and film Hidden Figures, and NASA later named its Computational Research Facility after her.")
    
print("==== WOMEN IN STEM ====")
print()
print("About Whom would you like to have information about?")
print()
print("1. Madam Curie")
print()
print("2. Ada Lovelace")
print()
print("3. Katherine Johnson")
print()
print("4 . Quit")

proceed = True 

while proceed == True:
   answer = input()
   if answer == "1":
      madam_curie()
   elif answer == "2":
      ada_lovelace()
   elif answer == "3":
      katherine_johnson()
   elif answer == "4":
     proceed = False
     print("Goodbye")
   else:
       print("Invalid Input")
            
            