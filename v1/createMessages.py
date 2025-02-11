import random

def replaceChar(s, index, new_char):
    s[index] = new_char

def processMessage(inputMessage):
    symbolMatch = {}
    availableAlpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    outputWords = []
    words = inputMessage.split()
    for word in words:
        characters = list(word)
        for i, char in enumerate(characters):
            if char not in symbolMatch.keys():
                randomChar = random.choice(availableAlpha)
                while randomChar == char:
                    randomChar = random.choice(availableAlpha)
                symbolMatch[char] = randomChar
                availableAlpha.remove(randomChar)
            replaceChar(characters, i, symbolMatch[char])
        outputWords.append("".join(characters))
    return " ".join(outputWords)

if __name__=="__main__":
    inputMessage = input("Encrypted Message: ").upper()
    outputMessage = processMessage(inputMessage)
    print(outputMessage)