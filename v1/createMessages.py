import random

def replaceChar(s, index, new_char):
    s[index] = new_char

def generateCipher(inputMessage):
    encodedLetters = {}
    availableAlpha = list("abcdefghijklmnopqrstuvwxyz")
    output = []

    for letter in inputMessage:
        if letter.isalpha():
            if letter not in encodedLetters:
                random.shuffle(availableAlpha)  # Shuffle to improve randomness
                randomChar = next((ch for ch in availableAlpha if ch != letter), availableAlpha[0])
                encodedLetters[letter] = randomChar
                availableAlpha.remove(randomChar)  # Remove assigned letter
            output.append(encodedLetters[letter])
        else:
            output.append(letter)

    return "".join(output)

# the quick brown fox jumps over the lazy dog while the zebras and the wolves zigzag through fields, fetching jugs of mixed liquor and hefty boxes.
# a jittery mouse vexed a dozing cat while big frogs and quirky zebras hopped over waxy boxes filled with mixed liquid and junk.

if __name__=="__main__":
    inputMessage = input("Encrypted Message: ").lower()
    for i in range(100):
        outputMessage = generateCipher(inputMessage)
        print(outputMessage)