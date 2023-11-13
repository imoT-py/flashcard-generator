# This is the first python file from project: Automatic Flashcard Generator For Anki
# Anki is a word learning card application. People can create memory cards which helps to learn literally anything what
# the student wants. The card has a front and a back.

from tkinter import *
from get_cards import cards_to_anki

# The main list where program collect the words that need to be created as a card in Anki
LIST = []

# Using tkinter to create a python GUI
root = Tk()

root.title("Automatic Flashcard Generator For Anki")
root.geometry("350x250")

lbl = Label(root, text="Word: ")
lbl.grid(column=0, row=0)

txt = Entry(root, width=10)
txt.grid(column=2, row=0)

text_list = Listbox(root)


# In the GUI window we can see the words we added to the list
def update_listbox():
    text_list.delete(0, END)
    for text in LIST:
        text_list.insert(END, text)
    text_list.grid(column=2, row=1)


# The function for 'btn', add the written word to the list
def clicked(event=None):
    if txt.get() != "":
        LIST.append(txt.get())
        txt.delete(0, END)
        update_listbox()


# Start the function in get_cards.py, the cards will be created in Anki from the list
def create():
    cards_to_anki(LIST)


# Can delete words from the list from the GUI
def delete():
    global LIST
    if len(LIST) != 0:
        selection = text_list.curselection()
        update_listbox()
        text_list.delete(selection[0])
        del LIST[selection[0]]


# First button which add a word to the main list
btn = Button(root, text="Add", command=clicked)
root.bind("<Return>", clicked)
btn.grid(column=3, row=0)

# Button that start the create() function
btn_card = Button(root, text="Create cards", command=create)
btn_card.grid(column=2, row=3)

# Button that delete a word from the list
btn_delete = Button(root, text="Delete", command=delete)
btn_delete.grid(column=3, row=3)

update_listbox()

root.mainloop()
