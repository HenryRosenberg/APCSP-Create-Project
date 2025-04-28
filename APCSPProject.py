# Written for AP Computer Science Principles in 2025

# Color Defenitions
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
NORMAL = '\033[0m'

WEIGHT_COLORS = [RED, BLUE, YELLOW, GREEN, NORMAL, RED, BLUE, YELLOW, GREEN, NORMAL]
WEIGHT_VALUES = [55, 45, 35, 25, 15, 10, 5, 2.5, 1, 0.5] # Common plate values in pounds
LB_TO_KG_CONVERSION_FACTOR = 2.205

def ASCIIArtOutput(plateCounts):
    # Prints a graphic of the bar loaded with plates ascii row by row
    ASCII_ROW_CUTOFFS = [35, 20, 0, 20, 35] # Top row, 2nd top, center, 2nd bottom, bottom row; the cuttoff values to draw a character

    for cutoff in ASCII_ROW_CUTOFFS: # Iterate through the cuttoff values for each row
        # Match the layout of a barbell (Lightest -> Heaviest -> Bar Handle -> Heaviest -> Lightest). [0] denotes the center of the bar
        plateLayout = plateCounts[::-1] + [1] + plateCounts
        plateColorLayout = WEIGHT_COLORS[::-1] + [NORMAL] + WEIGHT_COLORS
        weightValuesLayout = WEIGHT_VALUES[::-1] + [0] + WEIGHT_VALUES

        for plateCount, plateWeight, plateColor in zip(plateLayout, weightValuesLayout, plateColorLayout): # Interate over all three lists at the same time
            print(plateColor, end="") # Set the output color
            printSymbol = '█'
            if (plateWeight <= 10): # Switch to a smaller block for smaller weights
                printSymbol = '■'
            
            while plateCount > 0: # Draw multiple of the same plates
                if (plateWeight == 0): # bar handle is currently being drawn
                    if (cutoff == 0): # If in middle row draw the handle, or just an offset space
                        print("────────────", end="")
                    else:
                        print("            ", end="")
                    break

                if (plateWeight > cutoff): # If the plate is big enough for a block on the current row
                    print(printSymbol, end="")

                elif (plateWeight > 0): # If there is any weight (but it wasnt enough for a #), then draw a space to keep spacing correct
                        print(" ", end="")
                plateCount -= 1
                
        print("")

def sumWeights(plateCounts, barWeight):
    sumLB = barWeight

    for i in range(len(plateCounts)): # Sum the plates
        sumLB += (WEIGHT_VALUES[i] * plateCounts[i] * 2) # Lifters always use symetric plates, so multiple by 2 for each of the plates per bar

    sumKG = round(sumLB / LB_TO_KG_CONVERSION_FACTOR, 1)
    sumLB = round(sumLB, 1)

    return sumLB, sumKG

def output(plateCounts, barWeight, showHelp=True):
    # Prints a title, calls ASCIIArtOutput() to print the graphic, and prints all relevant information
    print("\033[H\033[J") # Clear console

    print(MAGENTA + "~ How Much Weight is on my Bar? ~\n" + NORMAL) # Title
    
    lb, kg = sumWeights(plateCounts, barWeight) # Returns sum of the plates + bar weight
    print(f"Total Weight: {str(lb)}lb, {str(kg)}kg", end="\n\n")

    ASCIIArtOutput(plateCounts) # Draw graphic
    print() # Newline for visual separation 

    # Print quantiities of the plates
    index = 0
    for i in range(2): # Loop through the rows
        for j in range(5): # Loop through the columns
            print(WEIGHT_COLORS[index] + str(WEIGHT_VALUES[index]) + "lb: " + str(plateCounts[index] * 2), end="  ") # Symetric plate loading
            index += 1
        print() # Force a new line
    
    # Print bar info
    print("Bar Size: " + str(barWeight) + "lb\n")

    if showHelp: # Print Instructions
        print(f"Type {RED}help{NORMAL} for a full list of commands\n")

def plateCountModify(plateValue, operation, plateCounts):
    # operation (Bool): False = remove, True = Add

    try:
        index = WEIGHT_VALUES.index(plateValue)
    except ValueError: # not a valid plate size; not found in list
        return False, plateCounts

    if (operation == False):
        if (plateCounts[index] == 0): # No plates to remove
            return False, plateCounts
        plateCounts[index] -= 1 # remove a weight
        return True, plateCounts
    elif (operation == True):
        plateCounts[index] += 1 # add a weight
        return True, plateCounts

def swapBar(barWeight):
    # 35lb and 45lb are the 2 standard sizes. Swap between them
    if barWeight == 45:
        return 35
    return 45

def solver(plateCounts, barWeight, targetWeight):
    # Calculates the combination of standard plates needed to reach the requested weight, prioritizes using the largest possible plates
    # Adds on top of prexisitng plates to minimize bar reloading
    if targetWeight > 2200: 
        return plateCounts, barWeight, "That's more than double the world record! Please choose a smaller value.\n"
    
    currentWeightLB, _ = sumWeights(plateCounts, barWeight)
    weightNeeded = targetWeight - currentWeightLB

    if weightNeeded <= 0:
        return plateCounts, barWeight, "Value must be larger than current weight to solve.\n"

    for i, selectedWeight in enumerate(WEIGHT_VALUES): # Eneumerate returns a tuple with weight values and their indicies
        while weightNeeded >= 2 * selectedWeight: # Two plates, one for each side
            weightNeeded -= 2 * selectedWeight
            plateCounts[i] += 1

    if weightNeeded > 0:
        return plateCounts, barWeight, f"Warning: Could not exactly match the target weight. {weightNeeded}lb remaining.\n"

    return plateCounts, barWeight, ""

def userInputHander(plateCounts, barWeight):
    userInput = input("Enter command: ") # Get data from terminal

    inputWords = userInput.strip().lower().split(" ") # Clean up and split at spaces
    
    try:
        match inputWords[0]: # First word is the command
            case "help":
                showHelpCommands()
            case "add":
                success, plateCounts = plateCountModify(float(inputWords[1]), True, plateCounts) # True is addition
                if success:
                    output(plateCounts, barWeight) # Go to main page
                else:
                    print(f"Invalid plate size. Use {RED}solve{NORMAL} to reach desired weight")
            case "remove":
                success, plateCounts = plateCountModify(float(inputWords[1]), False, plateCounts) # False is subtraction
                if success:
                    output(plateCounts, barWeight) # Go to main page
                else:
                    print("Invalid plate size or no plates to remove.")
            case "bar":
                barWeight = swapBar(barWeight)
                output(plateCounts, barWeight) # Go to main page
            case "clear":
                barWeight = 45 # Default Values
                plateCounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
                output(plateCounts, barWeight) # Go to main page
            case "solve":
                plateCounts, barWeight, solverMessage = solver(plateCounts, barWeight, float(inputWords[1])) # calculate the plates to add
                output(plateCounts, barWeight) # Go to main page
                print(solverMessage, end="")
            case "exit":
                exit(0) # End program with code of 0 (success) 
            case _: # None of the above
                print("Invalid command")
    
    except ValueError: # Input could not be converted to a float
        print("Invalid value")
    except TypeError:
        print("Error")
    
    return plateCounts, barWeight

def showHelpCommands():
    print(f"  {RED}add{NORMAL} <weight>     Add a weight of <weight> lb to your bar. Example: add 35")
    print(f"  {RED}remove{NORMAL} <weight>  Remove a weight of <weight> lb to your bar. Will have no effect if weight is not on your bar. Example: remove 35")
    print(f"  {RED}solve{NORMAL} <weight>   Set your bar to <weight> lb using a calculated set of plates. Keeps preexisting plates Example: solve 227")
    print(f"  {RED}bar{NORMAL}              Swap the bar between 45lb and 35lb Example: bar")
    print(f"  {RED}clear{NORMAL}            Remove all weights. Example: clear")
    print(f"  {RED}exit{NORMAL}             Exit program. Example: exit\n")

def main():
    barWeight = 45 # Default Mens bar
    weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 

    output(weights, barWeight, False)
    showHelpCommands()

    while(True): 
        weights, barWeight = userInputHander(weights, barWeight)

main()
