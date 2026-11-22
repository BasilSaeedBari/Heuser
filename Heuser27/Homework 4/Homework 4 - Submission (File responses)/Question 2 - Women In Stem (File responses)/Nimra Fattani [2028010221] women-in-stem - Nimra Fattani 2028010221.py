def ada_lovelace():
    print()
    print("ADA LOVELACE")
    print()

    print("STEM Field: Analytical Computing & Mathematical Philosophy")
    print()

    print("General Facts:")
    print("Raised by a mother determined to suppress any artistic impulses through rigorous mathematical tutoring, she grew up surrounded by elite British scientists and intellectuals.")
    print("She collaborated extensively with inventor Charles Babbage, translating and profoundly expanding upon a French article about his theoretical calculating machine.")
    print()

    print("Major Achievements:")
    print("Authored a series of extensive, visionary notes containing the world's very first computer program (Algorithm G).")
    print("Envisioned a future where computing devices could manipulate symbols and compose complex music, stretching far beyond mere arithmetic.")
    print()

    print("Interesting Fact:")
    print("She attempted to use mathematical probability to formulate a foolproof betting system for horse racing, which temporarily resulted in heavy financial losses.")
    print()

    input("Press Enter to return to the menu...")


def marie_curie():
    print()
    print("MARIE CURIE")
    print()

    print("STEM Field: Radiochemistry & Experimental Physics")
    print()

    print("General Facts:")
    print("Born in Warsaw under the name Maria Skłodowska, she initially studied in secret at Poland's clandestine 'Flying University' before moving to Paris to attend the Sorbonne.")
    print("Alongside her husband Pierre Curie, she processed tons of raw pitchblende ore in a drafty, uninsulated shed to isolate fractions of new radioactive substances.")
    print()

    print("Major Achievements:")
    print("Successfully isolated pure radium and established foundational principles for atomic physics and the treatment of malignant tumors.")
    print("Established the Curie Institutes in Paris and Warsaw, which remain preeminent medical research facilities to this day.")
    print()

    print("Interesting Fact:")
    print("During World War I, she personally drove and operated converted Renault trucks equipped with X-ray gear right to the frontline trenches, earning the moniker 'Chef de la Radiographie Militaire.'")
    print()

    input("Press Enter to return to the menu...")


def rosalind_franklin():
    print()
    print("ROSALIND FRANKLIN")
    print()

    print("STEM Field: Molecular Biophysics & X-ray Diffraction")
    print()

    print("General Facts:")
    print("She spent years honing her expertise in physical chemistry in Paris, mastering the complex techniques of interpreting X-ray scattering from coal and organic fibers.")
    print("After her time at King's College London, she transitioned to Birkbeck College, where she made world-class breakthroughs in understanding plant viruses and the polio virus.")
    print()

    print("Major Achievements:")
    print("Produced exceptionally sharp X-ray diffraction images that revealed the helical geometry and hydration states of DNA.")
    print("Authored or co-authored nearly twenty seminal research papers on carbon microstructures and virus architecture, establishing structural virology as a discipline.")
    print()

    print("Interesting Fact:")
    print("An accomplished scientist and avid global traveler, she spent her final years taking extensive photographic expeditions across the Middle East, the US, and Asia despite battling terminal illness.")
    print()

    input("Press Enter to return to the menu...")


while True:
    print()
    print("WOMEN IN STEM")
    print()
    print("1. Ada Lovelace")
    print("2. Marie Curie")
    print("3. Rosalind Franklin")
    print("4. Quit")
    print()

    choice = input("Enter your choice: ")

    if choice == "1":
        ada_lovelace()

    elif choice == "2":
        marie_curie()

    elif choice == "3":
        rosalind_franklin()

    elif choice == "4":
        print()
        print("Goodbye!")
        break

    else:
        print()
        print("Invalid choice. Please try again.")