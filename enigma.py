import collections
import sys

# Get int from char (A-0, Z-25)
def uniChar(lett):
    return ord(lett) - ord('A')

# Transform char digit into int
def uniInt(int):
    return ord(int) - ord('0')

# Plugmap
plugMap = [i for i in range(26)]

# Set the plugs in the enigma machine
    # plugs: Plugboard connections. Ex. (AB,CD,...) Should not have repeats.
def setPlug(plugs):
    if plugs != "":
        plugList = plugs.split(",")
        for pair in plugList:
            plugMap[uniChar(pair[0])] = uniChar(pair[1])
            plugMap[uniChar(pair[1])] = uniChar(pair[0])

# Three rotors, three elements on each.
    # First one is the distance it travels
    # Second one is where it maps to
    # The third one is where the notch is located
rotorArr = [[[],[],[]],[[],[],[]],[[],[],[]]]

# Stores the original rotors' settings
rotor = [[[],[],16],[[],[],4],[[],[],21],[[],[],9],[[],[],25]]
rotorNotch = [16,4,21,9,25] # Q, E, V, J, Z

rotor[0][0] = [4,9,10,2,7,1,23,9,13,16,3,8,2,9,10,18,7,3,0,22,6,13,5,20,4,10]
rotor[0][1] = [4,10,12,5,11,6,3,16,21,25,13,19,14,22,24,7,23,20,18,15,0,8,1,17,2,9] # I THINK THIS SHIT BUGGED?

rotor[1][0] = [0,8,1,7,14,3,11,13,15,18,1,22,10,6,24,13,0,15,7,20,21,3,9,24,16,5]
rotor[1][1] = [0,9,3,10,18,8,17,20,23,1,11,7,22,19,12,2,16,6,25,13,15,24,5,21,14,4]

rotor[2][0] = [1,2,3,4,5,6,22,8,9,10,13,10,13,0,10,15,18,5,14,7,16,17,24,21,18,15]
rotor[2][1] = [1,3,5,7,9,11,2,15,17,19,23,21,25,13,24,4,8,22,6,0,10,12,20,18,16,14]

rotor[3][0] = [4,17,12,18,11,20,3,19,16,7,10,23,5,20,9,22,23,14,1,13,16,8,6,15,24,2]
rotor[3][1] = [4,18,14,21,15,25,9,0,24,16,20,8,17,7,23,11,13,5,19,6,10,3,2,12,22,1]

rotor[4][0] = [21,24,25,14,2,3,13,17,12,6,8,18,1,20,23,8,10,5,20,16,22,19,9,7,4,11]
rotor[4][1] = [21,25,1,17,6,8,19,24,20,15,18,3,13,7,11,23,0,22,12,9,16,14,5,4,2,10]

# Cycle the numbers mapped to account for the rotor rotating
def cycleRotor(index):
    for x in range(26):
        rotorArr[index][1][x] -= 1
        if (rotorArr[index][1][x] < 0):
            rotorArr[index][1][x] += 26

# Set the rotors to the proper numbers and the starting point
    # rotors: Rotor number (Ex. 123)
    # pos: Position of the rotors (Ex. GRS)
def setRotor(rotors, pos):
    for i in range(3):
        # Set the rotors and their notch in place
        rotorArr[i][0] = collections.deque(rotor[uniInt(rotors[i])-1][0])
        rotorArr[i][1] = collections.deque(rotor[uniInt(rotors[i])-1][1])
        rotorArr[i][2] = rotor[uniInt(rotors[i])-1][2]

        # Rotate the rotors to the given position
        for x in range(uniChar(pos[i])):
            rotorArr[i][0].append(rotorArr[i][0].popleft())
            rotorArr[i][1].append(rotorArr[i][1].popleft())

            cycleRotor(i)

            # Take the notch position into account
            rotorArr[i][2] -= 1
            if (rotorArr[i][2] < 0):
                rotorArr[i][2] = 25

# Takes a step on the rotor, if hits the notch, turn next rotor
def stepRotor(index):
    rotorArr[index][0].append(rotorArr[index][0].popleft())
    rotorArr[index][1].append(rotorArr[index][1].popleft())

    cycleRotor(index)

    # If hitting notch, moves the next rotor
    if (rotorArr[index][2] == 0 and index > 0):
        rotorArr[index][2] = 25
        stepRotor(index-1)
    else:
        rotorArr[index][2] -= 1

# Reflectors
refArr = [[],[],[]]
refArr[0] = [4,9,12,25,0,11,24,23,21,1,22,5,2,17,16,20,14,13,19,18,15,8,10,7,6,3]
refArr[1] = [24,17,20,7,16,18,11,3,15,23,13,6,14,10,12,8,4,1,5,25,2,22,21,9,0,19]
refArr[2] = [5,21,15,9,8,0,14,24,4,3,17,25,23,22,6,2,19,10,20,16,18,1,13,12,7,11]

# Sets the reflector
def setReflector(refl):
    refIndex = ord(refl) - ord('A')
    return refArr[refIndex]

# Enigma machine
def enigma_machine(settings, plugs, text):
    # Split up settings and plugs
    reflectorSetting = settings[0:1]
    rotorOrder = settings[1:4]
    rotorStart = settings[4:7]

    # Set Reflector, Plug and Rotors
    reflector = setReflector(reflectorSetting)
    setRotor(rotorOrder,rotorStart)
    setPlug(plugs)

    print("The encoded text is: ",end="")

    # Encode all of the letters
    for char in text:
        # Turns the char into int
        char = uniChar(char)
        
        # Rotates rightmost rotor
        stepRotor(2)

        # Plug letter
        char = plugMap[char]
        
        # Rotor changes character three times

        for i in range(2,-1,-1):
            char = char + rotorArr[i][0][char]
            if (char > 25):
                char -= 26

        # Reflector changes
        char = reflector[char]

        # Inverted Rotor changes character three times
        for i in range(3):
            char = rotorArr[i][1].index(char)

        # Plug again
        char = plugMap[char]

        # Print character
        print(chr(char+ord('A')),end="")
    print()

# Ask for first line (Reflector, three rotors, starting position)
    # Set reflector (A,B,C)
    # Set rotors L M R
    # Set starting positions of Rotors
settings = input("Enter the Reflector, Order of three rotors, and starting position (Ex: A123AAA): ")

# Ask for second line (Two letters separated by comma)
    # Link Letter to Letter, separated by comma
plugs = input("Enter the plugs: ")

# String to translate
plainText = input("Enter the message to encode: ")

enigma_machine(settings,plugs,plainText)
