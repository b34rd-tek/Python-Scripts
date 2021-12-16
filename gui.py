from Tkinter import *
import tkMessageBox

def beenClicked():
    radioValue = relStatus.get()
    tkMessageBox.showinfo("Relationship Status", "Hi " + yourName.get() + "\n" + "You clicked " + radioValue + "\n")
    return

def changeLabel():
    name = "Thanks for the click " + yourName.get()
    labelText.set(name)
    dispName = yourName.get()
    radioValue = relStatus.get()
    happy = checkboxVal.get()
    if ( happy == 1):
        tkMessageBox.showinfo(dispName + "'s Info:", "Hi " + dispName + "!\n" + "You are " + radioValue + "\n" + "And, you are happy about it!")
    else:
        tkMessageBox.showinfo(dispName + "'s Info:", "Hi " + dispName + "!\n" + "You are " + radioValue + "\n" + "And, you are not happy about it.")
    yourName.delete(0, END)
    return

app = Tk()
app.title("TK Gui Example")
app.geometry('450x300+200+200')

labelText = StringVar()
labelText.set("Click the button below and I will update")
label1 = Label(app, textvariable=labelText, height=4)
label1.pack()

checkboxVal = IntVar()
checkBox1 = Checkbutton(app, variable=checkboxVal, text="Happy?", onvalue = 1, offvalue = 0)
checkBox1.pack()

custName = StringVar(None)
yourName = Entry(app, textvariable=custName)
yourName.pack()

relStatus = StringVar()
relStatus.set(None)
radio1 = Radiobutton(app, text="Single", value="Single", variable = relStatus, command=beenClicked).pack()
radio1 = Radiobutton(app, text="Married", value="Married", variable = relStatus, command=beenClicked).pack()

button1 = Button(app, text="Submit", width=10, command=changeLabel)
button1.pack(side="bottom", padx=15, pady=15)
app.mainloop()
