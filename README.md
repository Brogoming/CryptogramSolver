# Cryptogram Solver 1.6.0
This project is for my Senior Seminar class, CIS 480, at Wayne State College. 
The purpose of this project is to be able to solve any cryptogram as close as possible.
To solve these encrypted messages it uses a Machine Learning model that is trained on a set number of sentences
along with other sentences. 

## Table of Content
- [How Does it Work](#how-does-it-work)
  - [Training](#training)
  - [Loading](#loading)
  - [Decoder](#decoder)
- [Decoder Rules](#decoder-rules)
- [Resources](#resources)
- [Python Packages](#python-packages)
- [Developer](#developer)

## How Does it Work
When starting up the program the cryptogram solver UI will pop up with different types 
of inputs and settings for the user to configure. 

### Training
The top section allows the user to create a ML model. There are 5 settings that need to be configured:

- **Model Type** - There are 3 model types to choose from: Random Forest Classifier, Logistic Regression, and Gradient Boosting Classifier.
- **Model Name** - Name of the model you want to save. This saves the model in the models folder.
- **Number of Sentences** - The number of sentences to train on. No more than 57340 sentences.
- **Randomness** - How random the model is when being trained. 
- **N Estimators/Max Iterations** - If the model type is Logistic Regression you'll be configuring Max Iterations. If it's the other two you'll be configuring N Estimators. No more than 10000

Once the settings are set you can click on the **Train Model** button. Depending on the settings this might take a while. The high the settings the slower it is to train.
The lower the settings the faster it is to train. This can have varying results when trying to decode an encrypted message.
Once the training is complete you can now decode your message. No need to load the model.

### Loading
If you have already saved models they will show up as options to use. Once a saved model is selected click 
the **Load Model** button, it shouldn't take longer than training a model. You don't need to do this if you just trained a model.

### Decoder
Here you can set the encrypted message and how many times you want the message to be decrypted. Depending on the length of the 
message and how many times you want it to be decrypted along with the complexity of the model chosen determines the time it
takes to solve the encryption.

## Decoder Rules

- The encrypted messages have to be full sentences.
- The encrypted words have to be real english words.
- This only works with lower case letters. Numbers and symbols will be ignored. 
- The words have to be spelt correctly.
- Do not click on anything else in the UI while it is training, loading, and decoding.
- Be careful where you run this, it will take a lot of computing power to train, load, and decode.

## Resources

- [Machine Learning with PyTorch and Scikit-Learn: Develop machine learning and deep learning models with Python](#https://www.amazon.com/dp/1801819319?ref=ppx_yo2ov_dt_b_fed_asin_title)
- [Harvard's CS50 AI Course](#https://learning.edx.org/course/course-v1:HarvardX+CS50AI+1T2020/home)
- [NLTK with Python 3 for Natural Language Processing](#https://www.youtube.com/playlist?list=PLQVvvaa0QuDf2JswnfiGkliBInZnIC4HL)
- [Scikit-learn Machine Learning with Python and SKlearn](#https://www.youtube.com/playlist?list=PLQVvvaa0QuDd0flgGphKCej-9jp-QdzZ3)

## Python Packages
- [Scikit-learn](#https://scikit-learn.org/stable/api/index.html)
- [nltk](#https://www.nltk.org/api/nltk.html)
- [scipy](#https://scipy.org/)
- [numpy](#https://numpy.org/)

## Extra Notes
If you are wanting to test any models with your own message, but it's not encrypted 
you can run the createMessages.py file and it will generate 100 encrypted messages for you based on the 
real message given.

## Developer
Linkedin: [Dakota Gullicksen](https://www.linkedin.com/in/dakota-w-gullicksen/)