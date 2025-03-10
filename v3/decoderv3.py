import string
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from nltk import FreqDist
from nltk.corpus import brown
import re
import pickle

englishVocab = set(word.lower() for word in brown.words() if re.search("^(?=[a-z']*$)(?=[^aeiou']*[aeiou])(?=[^bcdfghjklmnpqrstvwxyz']*[bcdfghjklmnpqrstvwxyz])[a-z']+$",word))
englishVocab.add('a')
englishVocab.add('i')
englishVocab = sorted(englishVocab, key=len)

freqWordDist = FreqDist(brown.words())
freqWordDist = [word[0].lower() for word, v in sorted(freqWordDist.items(), key=lambda item: item[1], reverse=True) if word.isalpha()]

symbolMatch = {}
messageResults = {}

letterFreq = FreqDist("".join(englishVocab))

def symbolMatchingInit(inputMessage):
    msgCopy = inputMessage.replace(" ", "")
    for symbol in list(msgCopy):
        if symbol not in symbolMatch.keys():
            symbolMatch[symbol] = ""

def createFeatureList(text, index):
    features = []

    # 1. Letter Frequencies (normalized count)
    letterFreqs = FreqDist(text)
    letterTotal = sum(letterFreqs.values())
    letterFreqsNormalized = {letter: count / letterTotal for letter, count in letterFreqs.items()}
    letter = text[index].lower()
    letterFreq = letterFreqsNormalized.get(letter, 0)  # Get normalized frequency for this letter
    features.append(letterFreq)

    # 2. Bigram Frequencies
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    bigramFreqs = FreqDist(bigrams)
    bigram = text[index - 1:index + 1] if index > 0 else ""
    bigramFreq = bigramFreqs.get(bigram, 0) / len(bigrams) if len(bigrams) > 0 else 0  # Normalize bigram frequency
    features.append(bigramFreq)

    # 3. Trigram Frequencies
    trigrams = [text[i:i + 3] for i in range(len(text) - 2)]
    trigramFreqs = FreqDist(trigrams)
    trigram = text[index - 2:index + 2] if index > 0 else ""
    trigramFreq = trigramFreqs.get(trigram, 0) / len(trigrams) if len(
        trigrams) > 0 else 0  # Normalize trigram frequency
    features.append(trigramFreq)

    # 4. Word Shape (e.g., _e__o for "hello")
    wordStart = text.rfind(' ', 0, index) + 1
    wordEnd = text.find(' ', index) if text.find(' ', index) != -1 else len(text)
    word = text[wordStart:wordEnd]
    wordShape = ''.join('_' if c.isalpha() else c for c in word)

    # Use number of underscores as the feature for word shape
    wordShapeUnderscoreCount = wordShape.count('_')
    features.append(wordShapeUnderscoreCount)

    # 5. Letter Position (First, Middle, Last)
    wordPosition = 1  # Default to middle
    if index == wordStart:  # First letter of the word
        wordPosition = 0
    elif index == wordEnd - 1:  # Last letter of the word
        wordPosition = 2
    features.append(wordPosition)

    # 6. Common Words Check
    word = ''.join(c for c in text[wordStart:wordEnd] if c.isalpha()).lower()
    isCommonWord = 1 if word in freqWordDist else 0
    features.append(isCommonWord)

    # Return the feature vector
    return features

def processMessage(ciphertext, model):
    decrypted = []

    for i, symbol in enumerate(ciphertext):
        if symbol.isalpha():
            if symbolMatch[symbol] != '':
                decrypted.append(symbolMatch[symbol])
            else:
                features = createFeatureList(ciphertext, i)
                prediction = str(model.predict([features])[0])
                availableLetters = [c for c in string.ascii_lowercase if c not in list(symbolMatch.values())]
                while prediction in list(symbolMatch.values()) or prediction == symbol or prediction.isalpha() == False:
                    if availableLetters:
                        # Prioritize letters based on frequency
                        prediction = random.choices(list(letterFreq.keys()), list(letterFreq.values()), k=1)[0]
                    else:
                        print(f"Warning: No available letters for position {i}. Decryption may be incomplete.")
                        prediction = '?'  # Use a placeholder or fallback letter
                        break
                symbolMatch[symbol] = str(prediction)
                decrypted.append(symbolMatch[symbol])
        else:
            decrypted.append(symbol)
    return ''.join(decrypted)

def trainModel(loadModel = True):
    filename = 'test_model2.sav'
    if loadModel:
        print("Training...")
        X_train = []
        y_train = []

        # Create training data using random ciphers
        sents = [" ".join(s).lower() for s in brown.sents()]

        print(len(sents))
        for sent in sents:  # Generate multiple samples

            # For each letter in the ciphertext, treat it as a sample
            for i, letter in enumerate(sent):
                if letter.isalpha():  # Only use letters as valid data points
                    X_train.append(createFeatureList(sent, i))
                    y_train.append(sent[i])  # Corresponding plaintext letter

        # clf = RandomForestClassifier(n_jobs=-1, max_samples=1000)
        clf = RandomForestClassifier(n_jobs=-1, random_state=24, max_features=None)
        clf.fit(X_train, y_train)
        pickle.dump(clf, open(filename, 'wb'))
        print("Training Complete")
    else:
        clf = pickle.load(open(filename, 'rb'))
    return clf

def storeMessages(message):
    messagePoint = 0
    for word in message.split(" "):
        if word in englishVocab:
            messagePoint += 1
    messageResults[message] = messagePoint/len(message.split(" "))

def presentNewMessage():
    bestMessage = ""
    bestScore = 0.0
    for message in messageResults.keys():
        if bestScore < messageResults[message]:
            bestMessage = message
            bestScore = messageResults[message]
    print("Decrypted Message:", bestMessage, "\nMessage Score:", bestScore)

if __name__ == "__main__":
    clf = trainModel(False)  # Train the model
    encryptedMessage = input("Encrypted Message: ")
    for i in range(100):
        symbolMatchingInit(encryptedMessage)
        decryptedMessage = processMessage(encryptedMessage, clf)
        storeMessages(decryptedMessage)
        symbolMatch = {}
    presentNewMessage()