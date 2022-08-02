import PySimpleGUI as sg
from tkinter import *
from tkinter import ttk

# dropdown = []
# dropdown1 = ["Option 1 - A","Option 1 - B","Option 1 - C"]
# dropdown2 = ["Option 2 - A","Option 2 - B","Option 2 - C"]
# dropdown3 = ["Option 3 - A","Option 3 - B","Option 3 - C"]

# layout = [[sg.Text("This is the drop down menus test")],
#           [sg.Combo(["Select an option",
#                      "Option 1",
#                      "Option 2",
#                      "Option 3"], key='OPTION',bind_return_key=True,default_value="Select an option",expand_x=True)],
#           [sg.Combo(dropdown, key='OPTION1',expand_x=True)],
#           [sg.Button("Okay",key='OKAY'), sg.Button("Cancel",key='CANCEL')]]
    
# drop_window = sg.Window("Dropdown menu test",layout=layout)
# event,values = drop_window.read()
# if values['OPTION'] == "Option 1":
#     values['OPTION1'] = dropdown1

# drop_window.close()

root = Tk()
root.title('Codemy.com - Learn To Code!')
# root.iconbitmap('c:/gui/codemy.ico')
root.geometry("400x400")

def comboclick(event):
    # myLabel = Label(root, text=myCombo.get()).pack()
    if myCombo.get() == 'Friday':
        myLabel = Label(root, text="Yay! It's Friday!").pack()
    else:
        myLabel=Label(root,text=clicked.get()).pack()
def selected(event):
    # myLabel = Label(root, text=clicked.get()).pack()
    if clicked.get() == 'Friday':
        myLabel = Label(root, text="Yay! It's Friday!").pack()
    else:
        myLabel=Label(root,text=clicked.get()).pack()
options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"]

clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root,clicked,*options,command=selected)
drop.pack(pady=20)

# myButton = Button(root, text="select from list", command= selected)
# myButton.pack()

myCombo = ttk.Combobox(root,value=options)
myCombo.current(0)
myCombo.bind("<<ComboboxSelected>>",comboclick)
myCombo.pack()


root.mainloop()