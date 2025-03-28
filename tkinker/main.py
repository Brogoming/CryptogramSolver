from tkinter import *
from tkinter.ttk import Combobox

def select(event):
    selected_item = modelType.get()
    print(selected_item)

def action():
    print("button clicked")

def print_contents(event):
    print("Hi. The current entry content is:", modelName.get())

root = Tk()
root.title("Cryptogram Solver 1.6.0")
root.geometry('490x450')

# Create Labels
Label(root, text='Model:').grid(row=0, column=0)
Label(root, text='Model Name:').grid(row=0, column=2)
Label(root, text='Number of Sentences:').grid(row=1, column=0)
Label(root, text='Randomness:').grid(row=1, column=2)
Label(root, text='N Estimators:').grid(row=2, column=0)
Label(root, text='-----------------------------------------------------------------------------------------------').grid(row=3, columnspan=4)
Label(root, text='Saved Models:').grid(row=4, column=0)
Label(root, text='Model Loaded:').grid(row=5, column=1)
Label(root, text='-----------------------------------------------------------------------------------------------').grid(row=6, columnspan=4)
Label(root, text='Encrypted Message:').grid(row=7, columnspan=4)
Label(root, text='Number of Results:').grid(row=9, column=0)
Label(root, text='-----------------------------------------------------------------------------------------------').grid(row=10, columnspan=4)
Label(root, text='Decrypted Results:').grid(row=11, columnspan=4)

# Create Widgets
modelType = Combobox(root, values=["RandomForestClassifier", "LogisticRegression", "LinearRegression"])
modelType.set("RandomForestClassifier")
modelType.bind("<<ComboboxSelected>>", select)

modelName = StringVar(value="model01", name="modelName")
modelNameField = Entry(root, textvariable=modelName)
modelNameField.bind('<Key-Return>', print_contents)

numSent = IntVar(value=57340, name="numSent")
numSentField = Entry(root, textvariable=numSent)
numSentField.bind('<Key-Return>', print_contents)

randomness = IntVar(value=0, name="randomness")
randomnessField = Entry(root, textvariable=randomness)
randomnessField.bind('<Key-Return>', print_contents)

nEstimators = IntVar(value=100, name="nEstimators")
nEstimatorsField = Entry(root, textvariable=nEstimators)
nEstimatorsField.bind('<Key-Return>', print_contents)

trainModelButton = Button(root, text='Train Model', width=30, bg="blue", foreground="white", command=action)
savedModels = Combobox(root, values=["stuff1", "stuff2", "stuff3"])
savedModels.set("stuff1")
savedModels.bind("<<ComboboxSelected>>", select)
loadModelButton = Button(root, text='Load Model', width=30, bg="red", foreground="black", command=action)
loadComplete = 'Not Loaded'
loadMessage = Message(root, text=loadComplete, bg='pink', width=80)
messageEntry = Entry(root, width=80)
scrollbar = Scrollbar(root)
decryptedList = Listbox(root, yscrollcommand=scrollbar.set, width=80)

numResults = IntVar(value=1, name="numResults")
numResultsField = Entry(root, textvariable=numResults)
numResultsField.bind('<Key-Return>', print_contents)
decryptButton = Button(root, text='Decrypt Message', width=30, bg="green", foreground="black", command=action)

for line in range(100):
    decryptedList.insert(END, 'This is line number' + str(line))
scrollbar.config(command=decryptedList.yview)

# Place Widgets
modelType.grid(row=0, column=1)  # model type
modelNameField.grid(row=0, column=3)  # model name
numSentField.grid(row=1, column=1)  # number of sentences to train
randomnessField.grid(row=1, column=3)  # randomness
nEstimatorsField.grid(row=2, column=1)  # number of estimators
trainModelButton.grid(row=2, column=2, columnspan=2)  # train model activation
savedModels.grid(row=4, column=1)
loadModelButton.grid(row=4, column=2, columnspan=2)
loadMessage.grid(row=5, column=2)
messageEntry.grid(row=8, column=0, columnspan=4)
numResultsField.grid(row=9, column=1)
decryptButton.grid(row=9, column=2, columnspan=2)
decryptedList.grid(row=12, column=0, rowspan=10, columnspan=4)

root.mainloop()
