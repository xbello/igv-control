"""GUI for IGV controller."""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk

import helpers

class StatusBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.parent.resizable(0, 0)


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
        self._statusbar()

    def _menubar(self):
        menubar = tk.Menu(self.parent)
        self.parent["menu"] = menubar
        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_file)

    def _mainframe(self):
        mainframe = ttk.Frame(self.parent, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.prev_btn = ttk.Button(mainframe,
                                   text="Previous",
                                   state=("disabled",),
                                   command=self.prev_item)
        self.prev_btn.grid(column=0, row=0, sticky=tk.W)
        self.next_btn = ttk.Button(mainframe,
                                   text="Next",
                                   state=("disabled",),
                                   command=self.next_item)
        self.next_btn.grid(column=2, row=0, sticky=tk.E)

    def _statusbar(self):
        self.info_label = tk.StringVar()
        infoholder = ttk.Label(self.parent, textvariable=self.info_label)
        infoholder.grid(column=0, row=1, columnspan=3)

    def new_file(self):
        variants_file = askopenfilename(
            filetypes=(("Tabbed files", ("*.tab", "*.txt")),
                       ("VCF files", "*.vcf"),
                       ("All files", "*")))

        if variants_file:
            self.variants = list(helpers.Variants(variants_file))
            self.variants_index = 0
            self.info_label.set(variants_file)
            self.next_btn.state(statespec=("!disabled",))

    def next_item(self):
        self._view_item(self.variants[self.variants_index])
        self.variants_index += 1
        self.prev_btn.state(statespec=("!disabled",))

        if self.variants_index == len(self.variants):
            self.next_btn.state(statespec=("disabled",))

    def prev_item(self):
        self.variants_index -= 1
        self._view_item(self.variants[self.variants_index])
        self.next_btn.state(statespec=("!disabled",))

        if self.variants_index == 0:
            self.prev_btn.state(statespec=("disabled",))

    def _view_item(self, item):
        self.info_label.set(self.variants[self.variants_index])
        try:
            self.controller.goto(":".join(self.variants[self.variants_index]))
        except:
            pass


def guimode():
    """Launch the IGV-control as a TK GUI."""
    controller = helpers.IGV()

    # Test the IGV is running and accepting
    try:
        controller.check_igv()
    except OSError:
        # Be mild about timeouts because IGV timeouts a lot.
        print("IGV was not detected " +
              "on ip {}, port {}".format(controller.host,
                                         controller.port))

    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
