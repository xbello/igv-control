"""GUI for IGV controller."""
from tkinter import *
from tkinter import ttk

import helpers


def new_file():
    print("NEW FILE")

def next_item():
    print("NEXT")

def prev_item():
    print("PREV")


def guimode():
    """Launch the IGV-control as a TK GUI."""
    ##  http://www.tkdocs.com/tutorial/ ##
    controller = helpers.IGV()

    # Test the IGV is running and accepting
    try:
        controller.check_igv()
    except OSError:
        # Be mild about timeouts because IGV timeouts a lot.
        print("IGV was not detected " +
              "on ip {}, port {}".format(controller.host,
                                         controller.port))

    root = Tk()
    root.resizable(0, 0)
    root.title("IGV Control")

    root.option_add('*tearOff', FALSE)
    menubar = Menu(root)
    root["menu"] = menubar
    menu_file = Menu(menubar)
    menubar.add_cascade(menu=menu_file, label='File')
    menu_file.add_command(label='New', command=new_file)

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    infoholder = ttk.Label(root, text="VOID")
    infoholder.grid(column=0, row=1, columnspan=3)

    ttk.Button(mainframe, text="Previous", command=prev_item).grid(
        column=0, row=0, sticky=W)
    ttk.Button(mainframe, text="Next", command=next_item).grid(
        column=2, row=0, sticky=W)

    root.mainloop()
