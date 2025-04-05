from tkinter import *
from tkinter.ttk import Combobox
from decoderv6 import *
from pathlib import Path

model = None

def loadModelAction():
    global model  # Use the global model variable
    savedModel = savedModels.get()
    loadMessage.configure(text='Loading...', bg='lightyellow', width=100, padx=15)
    root.update_idletasks()
    model = loadModel(savedModel)
    loadMessage.configure(text='Load Complete', bg='lightgreen', width=100, padx=15)
    root.update_idletasks()

def trainModelAction():
    global model  # Use the global model variable
    modelName = modelNameField.get()
    modelType = modelTypeBox.get()
    numSent = int(numSentVar.get())
    randomness = int(randomnessVar.get())
    nEstimators = int(nEstimatorsVar.get())
    loadMessage.configure(text='Training...', bg='lightyellow', width=100, padx=15)
    root.update_idletasks()
    model = trainModel(modelName, modelType, nEstimators, randomness, numSent)
    loadMessage.configure(text='Training Complete', bg='lightgreen', width=100, padx=15)
    root.update_idletasks()

def solveMessageAction():
    global model  # Use the global model variable

    if model is None:
        print("No model loaded or trained.")
        return
    # Clear the previous results from the list
    decryptedList.delete(0, END)
    messageResults = {}
    encryptedMessage = messageVar.get()
    numResults = int(numResultsVar.get())
    count = 0
    while count < numResults:
        decryptedMessage = processMessage(encryptedMessage, model)
        score = scoreMessage(decryptedMessage, encryptedMessage)
        if score >= 0.8:
            count += 1
            messageResults[decryptedMessage] = score
            decryptedList.insert(END, f"{count}. {decryptedMessage} (Score: {score:.2f})")
            root.update_idletasks()
    scrollbar.config(command=decryptedList.yview)
    root.update_idletasks()

def selectSavedModel(event):
    if savedModels.get() == '':
        loadModelButton.configure(state=DISABLED)
    else:
        loadModelButton.configure(state=NORMAL)
    root.update_idletasks()

def disableTraining(*args):
    if modelNameVar.get() == '' or numSentVar.get() == '' or int(numSentVar.get()) > 57340 or int(numSentVar.get()) == 0 or randomnessVar.get() == '' or int(randomnessVar.get()) > (2**32 - 1) or nEstimatorsVar.get() == '' or int(nEstimatorsVar.get()) > 10000 or int(nEstimatorsVar.get()) == 0:
        trainModelButton.configure(state=DISABLED)
    else:
        trainModelButton.configure(state=NORMAL)
    root.update_idletasks()

def changeParams(*args):
    if modelTypeBox.get() == 'LogisticRegression':
        nEOrMI.configure(text="Max Iteration:")
    else:
        nEOrMI.configure(text="N Estimators:")
    root.update_idletasks()

def disableDecoder(*args):
    if messageVar.get() == '' or numResultsVar.get() == '' or int(numResultsVar.get()) > 100 or int(numResultsVar.get()) == 0:
        decryptButton.configure(state=DISABLED)
    else:
        decryptButton.configure(state=NORMAL)
    root.update_idletasks()

root = Tk()
root.title("Cryptogram Solver 1.6.0")
root.geometry('490x450')

# Create Labels
Label(root, text='Model:').grid(row=0, column=0)
Label(root, text='Model Name:').grid(row=0, column=2)
Label(root, text='Number of Sentences:').grid(row=1, column=0)
Label(root, text="Randomness:").grid(row=1, column=2)
nEOrMI = Label(root, text='N Estimators:')
nEOrMI.grid(row=2, column=0)
Label(root, text='-----------------------------------------------------------------------------------------------').grid(row=3, columnspan=4)
Label(root, text='Saved Models:').grid(row=4, column=0)
Label(root, text='Model Loaded:').grid(row=5, column=1)
Label(root, text='-----------------------------------------------------------------------------------------------').grid(row=6, columnspan=4)
Label(root, text='Encrypted Message:').grid(row=7, columnspan=4)
Label(root, text='Number of Results:').grid(row=9, column=0)
Label(root, text='-----------------------------------------------------------------------------------------------').grid(row=10, columnspan=4)
Label(root, text='Decrypted Results:').grid(row=11, columnspan=4)

# Create Widgets
## Train Model
modelTypeBox = Combobox(root, values=["RandomForestClassifier", "LogisticRegression", "GradientBoostingClassifier"])
modelTypeBox.bind('<<ComboboxSelected>>', changeParams)
modelTypeBox.set("RandomForestClassifier")

modelNameVar = StringVar(value="model01", name="modelName")
modelNameVar.trace_add("write", disableTraining)
modelNameField = Entry(root, textvariable=modelNameVar)

numSentVar = StringVar(value="57340", name="numSent")
numSentVar.trace_add("write", disableTraining)
numSentField = Entry(root, textvariable=numSentVar)

randomnessVar = StringVar(value="0", name="randomness")
randomnessVar.trace_add("write", disableTraining)
randomnessField = Entry(root, textvariable=randomnessVar)

nEstimatorsVar = StringVar(value="100", name="nEstimators")
nEstimatorsVar.trace_add("write", disableTraining)
nEstimatorsField = Entry(root, textvariable=nEstimatorsVar)

trainModelButton = Button(root, text='Train Model', width=30, bg="blue", foreground="white", command=trainModelAction, border=5)

## Load Model
currentDir = Path(__file__).parent
fileList = [f.name for f in currentDir.glob('*.sav')]
savedModels = Combobox(root, values=fileList)
savedModels.set("")
savedModels.bind("<<ComboboxSelected>>", selectSavedModel)

loadModelButton = Button(root, state=DISABLED, text='Load Model', width=30, bg="red", foreground="black", command=loadModelAction, border=5)
loadMessage = Message(root, text='No Model', bg='pink', width=100)

## Decrypt Message
messageVar = StringVar(name="messageVar")
messageVar.trace_add("write", disableDecoder)
messageEntry = Entry(root, width=80, textvariable=messageVar)

scrollbar = Scrollbar(root)
decryptedList = Listbox(root, yscrollcommand=scrollbar.set, width=80)

numResultsVar = StringVar(value="1", name="numResults")
numResultsVar.trace_add("write", disableDecoder)
numResultsField = Entry(root, textvariable=numResultsVar)

decryptButton = Button(root, state=DISABLED, text='Decrypt Message', width=30, bg="green", foreground="black", command=solveMessageAction, border=5)

# Place Widgets
modelTypeBox.grid(row=0, column=1)  # model type
modelNameField.grid(row=0, column=3)  # model name
numSentField.grid(row=1, column=1)  # number of sentences to train
randomnessField.grid(row=1, column=3)  # randomness
nEstimatorsField.grid(row=2, column=1)  # number of estimators
trainModelButton.grid(row=2, column=2, columnspan=2)  # train model activation
savedModels.grid(row=4, column=1)
loadModelButton.grid(row=4, column=2, columnspan=2)
loadMessage.grid(row=5, column=2, columnspan=2)
messageEntry.grid(row=8, column=0, columnspan=4)
numResultsField.grid(row=9, column=1)
decryptButton.grid(row=9, column=2, columnspan=2)
decryptedList.grid(row=12, column=0, rowspan=10, columnspan=4)

root.mainloop()
