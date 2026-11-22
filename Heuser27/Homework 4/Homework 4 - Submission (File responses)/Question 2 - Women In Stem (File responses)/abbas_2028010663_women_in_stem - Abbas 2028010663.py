while True:
    user_input = input("enter if you want to play else quit")
    
    if user_input == "quit":
        print("you have successfully quited")
        break 
       
    user_input = input("choose about which lady u want to study?. options are, adalove lace, grace hopper, katherine johnson")
       
    if user_input == "ada lovelace":
        print("Ada Lovelace, was an English mathematician and writer chiefly known for work on Charles Babbage's proposed mechanical general-purpose computer, the analytical engine. She was the first to recognise the machine had applications beyond pure calculation.")
    elif user_input == "grace hopper":
        print ("Grace Brewster Hopper was an American computer scientist, mathematician, and United States Navy rear admiral. She was a pioneer of computer programming.")
    elif user_input == "katherine johnson":
        print ("reola Katherine Johnson was an American mathematician and human computer whose calculations of orbital mechanics asa NASA employee were critical to the success of the first and subsequent U.S. crewed spaceflights.")
        