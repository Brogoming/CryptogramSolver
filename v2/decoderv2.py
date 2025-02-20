import random
from nltk.corpus import words
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

englishVocab = set(word.upper() for word in words.words())
englishVocab = sorted(englishVocab, key=len)
freq_letter_dist = FreqDist("".join(englishVocab))
availableAlpha = [letter for letter, v in sorted(freq_letter_dist.items(), key=lambda item: item[1], reverse=True) if letter.isalpha()]

def generateTrainingData():
    trainWords = random.sample(englishVocab, int(len(englishVocab) / 4))
    encryptedWords = []
    for word in trainWords:
        characters = list(word)
        symbolMatch = {}
        for i, letter in enumerate(characters):
            if letter not in symbolMatch.keys():
                randomChar = random.choice(availableAlpha)
                while randomChar == letter and randomChar in symbolMatch.values():
                    randomChar = random.choice(availableAlpha)
                symbolMatch[letter] = randomChar
            replaceChar(characters, i, symbolMatch[letter])
        encryptedWords.append("".join(characters))

def replaceChar(s, index, new_char): # replaces character by index
    s[index] = new_char

def processMessage(tokenizedWords):
    pass

if __name__=="__main__":
    generateTrainingData()
    inputMessage = input("Encrypted Message: ").upper()
    tokenizedWords = word_tokenize(inputMessage)
    processMessage(tokenizedWords)
