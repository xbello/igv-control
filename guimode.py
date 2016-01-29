"""GUI for IGV controller."""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk

import helpers

class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #self.grid(column=0, row=0, sticky="we")

        self.info_label = tk.StringVar()
        self.infoholder = ttk.Label(self, textvariable=self.info_label)
        self.infoholder["relief"] = "sunken"
        self.infoholder.pack(side="left", fill="x")
        #infoholder.grid(row=0, sticky="w")

        self.progress_label = tk.StringVar()
        self.progress = ttk.Label(self, textvariable=self.progress_label)
        self.progress["relief"] = "sunken"
        self.progress.pack(side="left", fill="x")
        #self.progress.grid(column=2, row=0, sticky="e")


class MainApp():
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.parent.resizable(0, 0)
        self.parent.title("IGV Control")

        self.parent.option_add('*tearOff', tk.FALSE)

        self.controller = helpers.IGV()

        # Test the IGV is running and accepting
        try:
            self.controller.check_igv()
        except OSError:
            # Be mild about timeouts because IGV timeouts a lot.
            print("IGV was not detected " +
                  "on ip {}, port {}".format(self.controller.host,
                                             self.controller.port))

        self._menubar()
        self._mainframe()
        self.statusbar = StatusBar(self.parent)

        self.statusbar.grid(column=0, row=2, columnspan=2, sticky="w")

    def _menubar(self):
        menubar = tk.Menu(self.parent)
        self.parent["menu"] = menubar
        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New...', command=self.new_file)

    def _mainframe(self):
        self.mainframe = ttk.Frame(self.parent, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=("nwes"))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.prev_btn = ttk.Button(self.mainframe,
                                   text="Previous",
                                   state=("disabled",),
                                   command=self.prev_item)
        self.prev_btn.grid(column=0, row=0, sticky="w")
        self.next_btn = ttk.Button(self.mainframe,
                                   text="Next",
                                   state=("disabled",),
                                   command=self.next_item)
        self.next_btn.grid(column=1, row=0, sticky="e")

    def new_file(self):
        variants_file = askopenfilename(
            filetypes=(("Tabbed files", ("*.tab", "*.txt")),
                       ("VCF files", "*.vcf"),
                       ("All files", "*")))

        if variants_file:
            self.variants = list(helpers.Variants(variants_file))
            self.variants_index = 0
            # Set a maximum of 22 chars
            self.statusbar.info_label.set(variants_file[-22:])
            self.statusbar.progress_label.set("{} variants".format(
                len(self.variants)))
            self.next_btn.state(statespec=("!disabled",))

    def next_item(self):
        self._view_item(self.variants[self.variants_index])

        # Enable the PREV button if we are beyond the second element
        if self.variants_index > 0:
            self.prev_btn.state(statespec=("!disabled",))

        if self.variants_index == len(self.variants) - 1:
            # Disable the NEXT button at the last element.
            self.next_btn.state(statespec=("disabled",))
        else:
            self.variants_index += 1

    def prev_item(self):
        self.variants_index -= 1
        self._view_item(self.variants[self.variants_index])

        # Enable the NEXT button if we just come from the last element.
        self.next_btn.state(statespec=("!disabled",))
        # We just served the 0 element. Disable the PREV.
        if self.variants_index == 0:
            self.prev_btn.state(statespec=("disabled",))

    def _view_item(self, item):
        self.statusbar.info_label.set(item)
        self.statusbar.progress_label.set("{} of {}".format(
            self.variants_index + 1, len(self.variants)))
        try:
            self.controller.goto(":".join(item))
        except OSError:
            # IGV always timesout, even working properly.
            pass


def guimode():
    """Launch the IGV-control as a TK GUI."""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    guimode()
