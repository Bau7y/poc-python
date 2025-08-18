from tkinter import *
from tkinter import ttk
from tkinter.font import *
from DataBaseConnection import *

class PrincipalWindow(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.windowCnfg()
        self.createObjs()


    
    def windowCnfg(self):
        self["bg"] = "#000000"
        self.state("zoomed")
        self.title("Árbol genealógico")

    def createObjs(self):
        self.barraMnu = Menu(self, bg="#000000", fg="#ffffff")
        self.mnuArchivo = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.mnuVer = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.mnuBuscar = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.barraMnu.add_cascade(label="Archivo", menu=self.mnuArchivo, underline=0)
        self.barraMnu.add_cascade(label="Ver", menu=self.mnuVer, underline=0)
        self.barraMnu.add_cascade(label="Buscar", menu=self.mnuBuscar, underline=0)
        self.configure(menu=self.barraMnu)
