import random

def replaceChar(s, index, new_char):
    s[index] = new_char

def generateCipher(inputMessage):
    encodedLetters = {}
    availableAlpha = list("abcdefghijklmnopqrstuvwxyz")
    outputWords = []
    inputWords = inputMessage.split()

    for i, letter in enumerate(inputMessage):
        if letter.isalpha():
            if letter not in encodedLetters.keys():
                randomChar = random.choice(availableAlpha)
                while randomChar == letter:
                    randomChar = random.choice(availableAlpha)
                encodedLetters[letter] = randomChar
            outputWords.append(encodedLetters[letter])
        else:
            outputWords.append(letter)
    return "".join(outputWords)

if __name__=="__main__":
    inputMessage = input("Encrypted Message: ").lower()
    outputMessage = generateCipher(inputMessage)
    print(outputMessage)