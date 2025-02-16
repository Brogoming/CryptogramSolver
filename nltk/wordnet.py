from nltk.corpus import wordnet

syns = wordnet.synsets('program')
print(syns)
print(syns[0].lemmas()[0].name()) # gets just the name of first synonym
print(syns[0].definition()) # definition
print(syns[0].examples()) # examples

# get all the synonyms and antonyms of the word good
synonyms = []
antonyms = []
for syn in wordnet.synsets('good'):
    for l in syn.lemmas():
        # print("l: ", l)
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
print(set(antonyms))

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')
print(w1.wup_similarity(w2)) # returns a percentage of similarity

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('car.n.01')
print(w1.wup_similarity(w2)) # returns a percentage of similarity

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('cat.n.01')
print(w1.wup_similarity(w2)) # returns a percentage of similarity

# could possibly use this, not sure