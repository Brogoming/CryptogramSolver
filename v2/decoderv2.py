from nltk.corpus import brown as words
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

english_vocab = list(word.upper() for word in words.words())
english_vocab = sorted(english_vocab, key=len)
freq_letter_dist = FreqDist("".join(english_vocab))
availableAlpha = [letter for letter, v in sorted(freq_letter_dist.items(), key=lambda item: item[1], reverse=True) if letter.isalpha()]

symbolMatch = {}

def replaceChar(s, index, new_char): # replaces character by index
    s[index] = new_char

def initLetters(inputMessage): # eliminates letters that match with symbols and sets symbols in symbolMatch
    msgCopy = inputMessage.replace(" ", "")
    for symbol in list(msgCopy):
        if symbol not in symbolMatch.keys() and symbol.isalpha():
            canLetters = availableAlpha.copy()
            canLetters.remove(symbol)
            symbolMatch[symbol] = {"assign": "", "can": canLetters, "cant": [symbol]}

def processMessage(tokens):
    initOneLWords(tokens)

def initOneLWords(tokens): # initialize 1-letter words
    for token in {t for t in tokens if len(t) == 1 and t.isalpha()}:  # Use a set for uniqueness
        possible_letters = [letter for letter in symbolMatch[token]["can"]]
        impossible_letters = symbolMatch[token]["cant"]  # Direct reference (no need to copy)

        # Retain only 'I' and 'A' in 'can', move others to 'cant'
        symbolMatch[token]["can"] = [letter for letter in possible_letters if letter in {"I", "A"}]
        impossible_letters.extend(letter for letter in possible_letters if letter not in {"I", "A"})

if __name__=="__main__":
    inputMessage = input("Encrypted Message: ").upper()
    initLetters(inputMessage)
    tokenizedWords = word_tokenize(inputMessage)
    processMessage(tokenizedWords)
