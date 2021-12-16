#!/usr/bin/python env

from Tkinter import *
import tkMessageBox
import sys
import os
from subprocess import call
#from passlib.hash import atlassian_pbkdf2_sha1 as e

# ===============================================
# Setup Command Functions
# ===============================================

def submit ():
    selection = hashType.get()
    if ( selection == "Atlassian" ):
        tkMessageBox.showinfo("Atlassian", "You selected Atlassian")
    elif ( selection == "ColdFusion" ):
        tkMessageBox.showinfo("Cold Fusion", "You selected Cold Fusion")
    else:
        tkMessageBox.showerror("Selection Error", "You failed to make a selection!")
    return

def quit ():
    exit(0)

def atlassian (p,h):
    print "Atlassian Password Verifier ..."

def coldfusion (p):
    call('clear')
    print "Cold Fusion Password Decryption ..."
    pwd = sys.argv[1]
    seed = "0yJ!@1$r8p0L@r1$6yJ!@1rj"
    key = pyDes.triple_des(seed)
    decrypted_key = key.decrypt( base64.decodestring(pwd), "*")
    print "Decrypted Password: " + decrypted_key
# ================================================
# Setup the Interface
# ================================================

app = Tk()
app.title("Hash Decryptor")
#app.geometry('250x100')

Label(app, text="Select hash type:").grid(row=0, column=0)

hashType = StringVar()
hashType.set(None)
Radiobutton(app, text = "Atlassian", value = "Atlassian", variable = hashType).grid(row=1, column=0, sticky='w')
Radiobutton(app, text = "Cold Fusion", value = "ColdFusion", variable = hashType).grid(row=2, column=0, sticky='w')

Label(app, text = "( Bamboo, Jira, Confluence, etc )").grid(row=1, column=1, sticky='w')
Label(app, text = "( Adobe Cold Fusion Data Source )").grid(row=2, column=1, sticky='w')

Label(app, text = "Password Hash:").grid(row=3, column=0, sticky='w')
Label(app, text = "Password List:").grid(row=4, column=0, sticky='w')

passwordList = StringVar(None)
passwordHash = StringVar(None)
Entry(app, textvariable=passwordHash).grid(row=3, column=1, sticky='w')
Entry(app, textvariable=passwordList).grid(row=4, column=1, sticky='w')

Button(app, text = "Ok", command = submit).grid(row=4, column=2, sticky='e')
Button(app, text = "Quit", command = quit).grid(row=4, column=3, sticky='w')

app.mainloop()
