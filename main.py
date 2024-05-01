from expansion import Expansion

TITLE = "The structure of theorem should exactly look like this: \n(a.x^N + b.y^N)^n \n"

if __name__ == "__main__":
    print(TITLE)

    while True:
        inputExpansion = input("Type the expansion: ")
            
        if(Expansion.isExpansion(inputExpansion) != True):
            raise ValueError("Please enter the valid expansion !")
        else:
            expansion = Expansion.strToExpansion(inputExpansion)

            if(expansion.theExpansionType() == "EXPANSION"):
                print(expansion.solvesTheBinomialExpansion() , end="\n\n")
            else:
                print(expansion.solvesTheBinomialSeries() , end="\n\n")