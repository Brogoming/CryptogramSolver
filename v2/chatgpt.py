import string
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
from nltk import FreqDist
from nltk.corpus import brown as words

# Common English words to check for in the ciphertext
englishVocab = set(word.lower() for word in words.words())
englishVocab = sorted(englishVocab, key=len)
freqWordDist = FreqDist(words.words())
freqWordDist = [word[0].lower() for word, v in sorted(freqWordDist.items(), key=lambda item: item[1], reverse=True) if word.isalpha()]


# Step 1: Generate a random cipher
def generate_cipher():
    alphabet = list(string.ascii_lowercase)
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))


# Step 2: Encode text using the cipher
def encode_text(text, cipher):
    return ''.join(cipher.get(c, c) for c in text.lower())


# Step 3: Extract features based on letter frequency
def extract_features(text, index):
    features = []

    # 1. Letter Frequencies (normalized count)
    letter_freqs = FreqDist(text)
    letter_total = sum(letter_freqs.values())
    letter_freqs_normalized = {letter: count / letter_total for letter, count in letter_freqs.items()}
    letter = text[index].lower()
    letter_freq = letter_freqs_normalized.get(letter, 0)  # Get normalized frequency for this letter
    features.append(letter_freq)

    # 2. Bigram Frequencies
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    bigram_freqs = FreqDist(bigrams)
    bigram = text[index - 1:index + 1] if index > 0 else ""
    bigram_freq = bigram_freqs.get(bigram, 0) / len(bigrams) if len(bigrams) > 0 else 0  # Normalize bigram frequency
    features.append(bigram_freq)

    # 3. Trigram Frequencies
    trigrams = [text[i:i + 3] for i in range(len(text) - 2)]
    trigram_freqs = FreqDist(trigrams)
    trigram = text[index - 2:index + 2] if index > 0 else ""
    trigram_freq = trigram_freqs.get(trigram, 0) / len(trigrams) if len(trigrams) > 0 else 0  # Normalize trigram frequency
    features.append(trigram_freq)

    # 3. Word Shape (e.g., _e__o for "hello")
    word_start = text.rfind(' ', 0, index) + 1
    word_end = text.find(' ', index) if text.find(' ', index) != -1 else len(text)
    word = text[word_start:word_end]
    word_shape = ''.join('_' if c.isalpha() else c for c in word)

    # Use number of underscores as the feature for word shape
    word_shape_underscore_count = word_shape.count('_')
    features.append(word_shape_underscore_count)

    # 4. Letter Position (First, Middle, Last)
    word_position = 1  # Default to middle
    if index == word_start:  # First letter of the word
        word_position = 0
    elif index == word_end - 1:  # Last letter of the word
        word_position = 2
    features.append(word_position)

    # 5. Common Words Check
    word = ''.join(c for c in text[word_start:word_end] if c.isalpha()).lower()
    is_common_word = 1 if word in freqWordDist else 0
    features.append(is_common_word)

    # Return the feature vector
    return features


# Step 4: Train a simple model (Logistic Regression)
def train_model():
    print("Training...")
    X_train = []
    y_train = []

    # Create training data using random ciphers
    plaintext = "the quick brown fox jumps over the lazy dog"

    for _ in range(1000):  # Generate multiple samples
        cipher = generate_cipher()
        encoded = encode_text(plaintext, cipher)

        # For each letter in the ciphertext, treat it as a sample
        for i, letter in enumerate(encoded):
            if letter.isalpha():  # Only use letters as valid data points
                X_train.append(extract_features(encoded, i))
                y_train.append(plaintext[i])  # Corresponding plaintext letter

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    print("Training Complete")
    return clf


# Step 5: Predict plaintext for a new encrypted message
def solve_cryptogram(ciphertext, model, plaintext):
    decrypted = []
    used_letters = set()  # Set to track used letters in the decryption
    letter_mapping = {}  # Dictionary to store current letter mappings
    letter_freq = {}  # Dictionary to track frequency of letters (for prioritization)

    # Count letter frequencies from the encrypted message to help prioritize
    for letter in ciphertext:
        if letter.isalpha():
            letter_freq[letter] = letter_freq.get(letter, 0) + 1

    for i, letter in enumerate(ciphertext):
        if letter.isalpha():  # Only predict for alphabetic characters
            features = extract_features(ciphertext, i)
            prediction = model.predict([features])[0]

            # If the predicted letter is already assigned, try a different one
            while prediction in used_letters and letter not in letter_mapping.keys():
                # Try to prioritize less used letters in the encrypted message
                available_letters = [c for c in string.ascii_lowercase if c not in used_letters]

                if available_letters:
                    # Prioritize letters based on frequency
                    available_letters = sorted(available_letters, key=lambda x: letter_freq.get(x, 0), reverse=True)
                    prediction = available_letters[0]  # Pick the most frequent remaining letter
                else:
                    print(f"Warning: No available letters for position {i}. Decryption may be incomplete.")
                    prediction = '?'  # Use a placeholder or fallback letter
                    break
            if letter not in letter_mapping.keys():
                # Add the predicted letter to the used letters set
                used_letters.add(prediction)

                # Map the letter and add to the decrypted message
                letter_mapping[ciphertext[i]] = prediction
                decrypted.append(prediction)
            else:
                decrypted.append(letter_mapping[letter])
        else:
            decrypted.append(letter)  # Keep non-alphabetic characters intact

    # Show the letter mapping for clarity
    print("Letter Mapping:", letter_mapping)

    return ''.join(decrypted)


# Train the model
clf = train_model()

# Example encrypted message
encrypted_message = "uvl nxtaw rkybz qyj pxedi yflk uvl hmcs gyo"
decrypted_message = solve_cryptogram(encrypted_message, clf, "the quick brown fox jumps over the lazy dog")
print("Decrypted message:", decrypted_message)
