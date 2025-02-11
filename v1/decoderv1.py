
knownWords = {}
availableAlpha = list("EARIOTNSLCUDPMHGBFYWKVXZJQ") # the alphabet in sorted by frequency
symbolMatch = {}  # a dictionary of dictionaries where the key is the symbol and the dictionary keeps track of letters that the symbol can and can't be

def loadWords():
    with open('knownWords.txt', 'r') as file:
        text = file.read()
    text =  text.split('\n')
    for word in text:
        if len(word) not in knownWords.keys():
            knownWords[len(word)] = [word]
        else:
            knownWords[len(word)].append(word)

def replaceChar(s, index, new_char): # replaces character by index
    s[index] = new_char

def sortDictionaryByValue(dict): # sorts a dictionary by value from highest to lowest
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=False)}

def initLoadLetters(inputMessage): # eliminates letters that match with symbols and sets symbols in symbolMatch
    msgCopy = inputMessage.replace(" ", "")
    for symbol in list(msgCopy):
        if symbol not in symbolMatch.keys():
            canLetters = availableAlpha.copy()
            canLetters.remove(symbol)
            symbolMatch[symbol] = {"can": canLetters, "cant": [symbol]}

def rearrangeCanLetters(index, msgWord, knownWordsByLength): # rearranges can letters based on how many times they show up at a certain index of a word
    commonLetters = {} # dictionary keeps track of how many characters show up at an index
    symbol = list(msgWord)[index]
    for word in knownWordsByLength:
        if symbol != list(word)[index]:
            if list(word)[index] in commonLetters.keys():
                commonLetters[list(word)[index]] += 1
            else:
                commonLetters[list(word)[index]] = 1
    commonLetters = sortDictionaryByValue(commonLetters)
    newCanList = symbolMatch[symbol]["can"].copy()
    for char in commonLetters.keys():
        if char in newCanList:
            newCanList.remove(char)
            newCanList.insert(0, char) # moves the letter to the front of the list
    symbolMatch[symbol]["can"] = newCanList

def singleLetterWords(symbol): # this will emininate letters for words that have the length of 1
    currentCanLetters = symbolMatch[symbol]["can"].copy()
    currentCantLetters = symbolMatch[symbol]["cant"].copy()
    for letter in symbolMatch[symbol]["can"]:
        if letter not in ["I", "A"]:
            currentCanLetters.remove(letter)
            currentCantLetters.append(letter)
    symbolMatch[symbol]["can"] = currentCanLetters
    symbolMatch[symbol]["cant"] = currentCantLetters

def processMessage(inputMessage):
    outputWords = []
    messageWords = inputMessage.split()
    initLoadLetters(inputMessage)
    for word in messageWords:
        if len(word) == 1:
            singleLetterWords(word)
        knownWordsByLength = knownWords[len(word)]
        for i, char in enumerate(word):
            rearrangeCanLetters(i, word, knownWordsByLength)

    print(symbolMatch)
    return None

if __name__=="__main__":
    loadWords()
    inputMessage = input("Encrypted Message: ").upper()
    outputMessage = processMessage(inputMessage)
    print(outputMessage)