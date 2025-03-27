from tkinter import *
from tkinter.ttk import Combobox


def select(event):
    selected_item = combo_box.get()
    print(selected_item)

def action():
    print("button clicked")

root = Tk()
root.title("Cryptogram Solver 1.6.0")
root.geometry('500x400')
Label(root, text='Model:').grid(row=0, column=0)
Label(root, text='Model Name:').grid(row=0, column=2)
Label(root, text='Number of Sentences:').grid(row=1, column=0)
Label(root, text='Randomness:').grid(row=1, column=2)
Label(root, text='N Estimators:').grid(row=2, column=0)
Entry(root).grid(row=0, column=1)  # model type

# Create Widgets
combo_box = Combobox(root, values=["RandomForestClassifier", "LogisticRegression", "LinearRegression"])
combo_box.set("RandomForestClassifier")
combo_box.bind("<<ComboboxSelected>>", select)
modelName = Entry(root)
numSent = Entry(root)
randomness = Entry(root)
nEstimators = Entry(root)
trainModelButton = Button(root, text='Train Model', width=30, bg="blue", foreground="white", command=action)

combo_box.grid(row=0, column=1)  # model type
modelName.grid(row=0, column=3)  # model name
numSent.grid(row=1, column=1)  # number of sentences to train
randomness.grid(row=1, column=3)  # randomness
nEstimators.grid(row=2, column=1)  # number of estimators
trainModelButton.grid(row=2, column=2, columnspan=2)  # train model activation

root.mainloop()
