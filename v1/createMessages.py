import random

def replaceChar(s, index, new_char):
    s[index] = new_char

def generateCipher(inputMessage):
    encodedLetters = {}
    availableAlpha = list("abcdefghijklmnopqrstuvwxyz")
    outputWords = []
    inputWords = inputMessage.split()

    for word in inputWords:
        characters = list(word)
        outputWord = []
        for char in characters:
            if char not in encodedLetters.keys():
                randomChar = random.choice(availableAlpha)
                while randomChar == char:
                    randomChar = random.choice(availableAlpha)
                encodedLetters[char] = randomChar
                availableAlpha.remove(randomChar)
            outputWord.append(encodedLetters[char])
        outputWords.append("".join(outputWord))
    return " ".join(outputWords)

if __name__=="__main__":
    inputMessage = input("Encrypted Message: ").lower()
    outputMessage = generateCipher(inputMessage)
    print(outputMessage)