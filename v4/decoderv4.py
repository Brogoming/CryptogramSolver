import random
import sys
from sklearn.ensemble import RandomForestClassifier
from nltk import FreqDist, bigrams, trigrams
from nltk.corpus import brown
import re
import pickle

englishVocab = set(word.lower() for word in brown.words() if re.search("^(?=[a-z']*$)(?=[^aeiou']*[aeiou])(?=[^bcdfghjklmnpqrstvwxyz']*[bcdfghjklmnpqrstvwxyz])[a-z']+$",word))
englishVocab.add('a')
englishVocab.add('i')
englishVocab = sorted(englishVocab, key=len)

freqWordDist = FreqDist(word.lower() for word in brown.words() if re.search("^(?=[a-z']*$)(?=[^aeiou']*[aeiou])(?=[^bcdfghjklmnpqrstvwxyz']*[bcdfghjklmnpqrstvwxyz])[a-z']+$",word))
freqWordDist = [word[0].lower() for word, v in sorted(freqWordDist.items(), key=lambda item: item[1], reverse=True)]

symbolMatch = {}
messageResults = {}

def symbolMatchingInit(inputMessage):
    msgCopy = inputMessage.replace(" ", "")
    for symbol in list(msgCopy):
        if symbol not in symbolMatch.keys():
            symbolMatch[symbol] = ""

def createFeatureList(word, char):
    features = []
    charIndex = word.index(char)

    # 1. Letter Frequencies of the word(normalized count)
    charFreqs = FreqDist(word)
    charTotal = sum(charFreqs.values())
    charFreqsNormalized = {char: count / charTotal for char, count in charFreqs.items()}
    charFreq = charFreqsNormalized.get(char, 0)  # Get normalized frequency for this letter
    features.append(charFreq)

    # 2. Bigram Frequencies
    wordBigrams = list(bigrams(word))
    bigramFreqs = FreqDist(wordBigrams)
    bigram = tuple(word[charIndex - 1:charIndex + 1]) if charIndex > 0 else None
    bigramFreq = bigramFreqs[bigram] / len(wordBigrams) if bigram and len(wordBigrams) > 0 else 0
    features.append(bigramFreq)

    # 3. Trigram Frequencies
    wordTrigrams = list(trigrams(word))
    trigramFreqs = FreqDist(wordTrigrams)
    trigram = tuple(word[charIndex - 2:charIndex + 1]) if charIndex > 1 else None
    trigramFreq = trigramFreqs[trigram] / len(wordTrigrams) if trigram and len(wordTrigrams) > 0 else 0
    features.append(trigramFreq)

    # 4. Word Shape (e.g., _e__o for "hello")
    wordShape = ''.join('_' if c.isalpha() else c for c in word)

    # Use number of underscores as the feature for word shape
    wordShapeUnderscoreCount = wordShape.count('_')
    features.append(wordShapeUnderscoreCount)

    # 5. Letter Position (First, Middle, Last)
    letterPosition = 1  # Default to middle
    if char == word[0]:  # First letter of the word
        letterPosition = 0
    elif char == word[-1]:  # Last letter of the word
        letterPosition = 2
    features.append(letterPosition)

    # 6. Common Words Check
    isCommonWord = 1 if word in freqWordDist else 0
    features.append(isCommonWord)

    # Return the feature vector
    return features

def getAvailableWords(word):
    availWords = [t for t in englishVocab if len(t) == len(word)]
    if any(symbol in symbolMatch.keys() for symbol in list(word)):
        for s, symbol in enumerate(word):
            if symbolMatch[symbol] != "":
                availWords = [w for w in availWords if w[s] == symbolMatch[symbol]]
    return availWords

def processMessage(cipherText, model):
    decrypted = []

    sortedText = sorted(cipherText.split(" "), key=len)

    for word in sortedText:
        availWords = getAvailableWords(word)
        if len(availWords) == 0:
            print('not enough words')
            continue
        for s, symbol in enumerate(word):
            if symbol.isalpha() and symbolMatch[symbol] == '':
                features = createFeatureList(word, symbol)
                prediction = str(model.predict([features])[0])

                availLetters = [t[s] for t in availWords if t[s].isalpha()]
                letterFreq = FreqDist(availLetters)
                while prediction in list(symbolMatch.values()) or prediction == symbol or not prediction.isalpha() or prediction not in availLetters:
                    if len(letterFreq) > 0:
                        prediction = random.choices(list(letterFreq.keys()), list(letterFreq.values()), k=1)[0]
                        letterFreq.pop(prediction)
                    else:
                        print(f"Warning: No available letters. Decryption may be incomplete.")
                        prediction = '?'  # Use a placeholder or fallback letter
                        break
                symbolMatch[symbol] = str(prediction)

    for symbol in cipherText:
        if symbol in symbolMatch.keys():
            decrypted.append(symbolMatch[symbol])
        else:
            decrypted.append(symbol)

    return "".join(decrypted)

def trainModel(newModel):
    filename = 'RFC_model1.sav'
    if newModel:
        print("Training...")
        X_train = []
        y_train = []

        # Create training data using random ciphers
        sents = [" ".join(s).lower() for s in brown.sents()]

        for sent in sents:  # Generate multiple samples
            for i, word in enumerate(sent.split(" ")):
                for letter in word:
                    if letter.isalpha():  # Only use letters as valid data points
                        X_train.append(createFeatureList(word, letter))
                        y_train.append(letter)  # Corresponding plaintext letter

        clf = RandomForestClassifier(n_jobs=-1, n_estimators=1000, random_state=100, max_features=None)
        clf.fit(X_train, y_train)
        pickle.dump(clf, open(filename, 'wb'))
        print("Training Complete")
    else:
        print("Loading...")
        clf = pickle.load(open(filename, 'rb'))
        print("Loading Complete")
    return clf

def storeMessages(message):
    messagePoint = 0
    for word in message.split(" "):
        if word in englishVocab:
            messagePoint += 1
    messageResults[message] = messagePoint/len(message.split(" "))


def presentNewMessage():
    sortedMessages = sorted(messageResults.items(), key=lambda x: x[1], reverse=True)[:5]
    print("--------------------------------Ranks Messages--------------------------------")
    for i, (message, score) in enumerate(sortedMessages, start=1):
        print(f"Rank {i}:")
        print(f"Decrypted Message: {message}")
        print(f"Message Score: {score}\n")

    if (input("Do you want to see the other results? (Y/N): ").upper() == 'Y'):
        print("--------------------------------Other Messages--------------------------------")
        for i, (message, score) in enumerate(sortedMessages, start=1):
            print("Decrypted Message:", message, "\nMessage Score:", sortedMessages[message], "\n")


if __name__ == "__main__":
    newModel = int(input("Train Model (1) or Load Model (0): "))
    if newModel == 0:
        clf = trainModel(False)  # Train the model
    elif newModel == 1:
        clf = trainModel(True)  # Train the model
    else:
        print("Invalid Input")
        sys.exit()
    encryptedMessage = input("Encrypted Message: ")
    for i in range(100):
        symbolMatchingInit(encryptedMessage)
        decryptedMessage = processMessage(encryptedMessage, clf)
        storeMessages(decryptedMessage)
        symbolMatch = {}
    presentNewMessage()

    # kpf jccmy bif cu oeif
    # p yxx dprexe ar uv spre