from tkinter import *
from tkinter import ttk
from tkinter.font import *
from DataBaseConnection import *
from tkcalendar import DateEntry
import tkinter as tk

class PrincipalWindow(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.windowCnfg()
        self.createObjs()
        self.placeObjs()


    def windowCnfg(self):
        self["bg"] = "#000000"
        self.state("zoomed")
        self.title("Árbol genealógico")
        self.resizable(False, False)

    def createObjs(self):
        self.barraMnu = Menu(self, bg="#000000", fg="#ffffff")
        self.mnuArchivo = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.mnuVer = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.mnuBuscar = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.barraMnu.add_cascade(label="Archivo", menu=self.mnuArchivo, underline=0)
        self.barraMnu.add_cascade(label="Ver", menu=self.mnuVer, underline=0)
        self.barraMnu.add_cascade(label="Buscar", menu=self.mnuBuscar, underline=0)
        self.configure(menu=self.barraMnu)

        self.leftFrame = tk.Frame(self, bg="lightgray", width=self.winfo_screenwidth() // 2, height=self.winfo_screenheight())
        self.rightFrame = tk.Frame(self, bg="lightgray", width=self.winfo_screenwidth() // 2, height=self.winfo_screenheight())

        self.lblBisAbueloPa1 = Label(self.leftFrame, text="Bisabuelo paterno", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblBisAbueloMa1 = Label(self.leftFrame, text="Bisabuelo materno", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblBisAbueloPa2 = Label(self.leftFrame, text="Bisabuelo paterno", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblBisAbueloMa2 = Label(self.leftFrame, text="Bisabuelo materno", bg="lightgray", font=("Arial", 12), fg="black")

        self.lblAbueloPa1 = Label(self.leftFrame, text="Abuelo paterno", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblAbueloPa2 = Label(self.leftFrame, text="Abuelo paterno", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblAbueloMa1 = Label(self.leftFrame, text="Abuelo Materno", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblAbueloMa2 = Label(self.leftFrame, text="Abuelo Materno", bg="lightgray", font=("Arial", 12), fg="black")

        self.lblPadre1 = Label(self.leftFrame, text="Padre", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblMadre1 = Label(self.leftFrame, text="Madre", bg="lightgray", font=("Arial", 12), fg="black")

        self.lblTio1 = Label(self.leftFrame, text="Tío", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblTia1 = Label(self.leftFrame, text="Tía", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblTio2 = Label(self.leftFrame, text="Tío", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblTia2 = Label(self.leftFrame, text="Tía", bg="lightgray", font=("Arial", 12), fg="black")

        self.lblHijo1 = Label(self.leftFrame, text="Hijo", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblHijo2 = Label(self.leftFrame, text="Hijo", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblHijo3 = Label(self.leftFrame, text="Hijo", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblHijo4 = Label(self.leftFrame, text="Hijo", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblHijo5 = Label(self.leftFrame, text="Hijo", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblHijo6 = Label(self.leftFrame, text="Hijo", bg="lightgray", font=("Arial", 12), fg="black")

        self.lblFutHijo = Label(self.leftFrame, text="Hijo futuro", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblFutHijo2 = Label(self.leftFrame, text="Hijo futuro", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblFutHijo3 = Label(self.leftFrame, text="Hijo futuro", bg="lightgray", font=("Arial", 12), fg="black")
        self.lblFutHijo4 = Label(self.leftFrame, text="Hijo futuro", bg="lightgray", font=("Arial", 12), fg="black")




    def placeObjs(self):
        self.leftFrame.pack(side="left", fill="y")
        self.rightFrame.pack(side="right", fill="y")
        self.lblBisAbueloPa1.place(x=60, y=10)
        self.lblBisAbueloPa2.place(x=210, y=10)

        self.lblBisAbueloMa1.place(x=430, y=10)
        self.lblBisAbueloMa2.place(x=580, y=10)

        self.lblAbueloMa1.place(x=60, y=100)
        self.lblAbueloMa2.place(x=210, y=100)
        
        self.lblAbueloPa1.place(x=430, y=100)
        self.lblAbueloPa2.place(x=580, y=100)

        self.lblPadre1.place(x=420, y=190)
        self.lblTio1.place(x=50, y=190)
        self.lblTia1.place(x=160, y=190)

        self.lblMadre1.place(x=280, y=190)
        self.lblTio2.place(x=550, y=190)
        self.lblTia2.place(x=700, y=190)

        self.lblHijo1.place(x=100, y=280)
        self.lblHijo2.place(x=360, y=280)
        self.lblHijo3.place(x=620, y=280)
        

class NewPersonWindow(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.personWindowCnfg()
        self.createObjs()
        self.placeObjs()

    def personWindowCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Nueva persona")

    def createObjs(self):
        genderList = ["Masculino", "Femenino", "Otro"]
        civilStateList = ["Soltero", "Casado", "Divorciado", "Viudo", "Union libre"]
        provinceList = ["Alajuela", "Heredia", "Cartago", "Limón", "San José", "Guanacaste", "Puntarenas"]
        self.nucleos = ["0", "1", "2", "3", "4"]
        self.lblName = Label(self, text="Nombre", bg="#FFFFFF", font=("Arial", 12))
        self.lblLastName = Label(self, text="Apellido", bg="#FFFFFF", font=("Arial", 12))
        self.lblLastName2 = Label(self, text="Segundo apellido", bg="#FFFFFF", font=("Arial", 12))
        self.lblId = Label(self, text="Cédula", bg="#FFFFFF", font=("Arial", 12))
        self.lblBirthDate = Label(self, text="Fecha de nacimiento", bg="#FFFFFF", font=("Arial", 12))
        self.lblDeathDate = Label(self, text="Fecha de fallecimiento", bg="#FFFFFF", font=("Arial", 12))
        self.lblGender = Label(self, text="Género", bg="#FFFFFF", font=("Arial", 12))
        self.lblProvince = Label(self, text="Provincia", bg="#FFFFFF", font=("Arial", 12))
        self.lblCivilState = Label(self, text="Estado civil", bg="#FFFFFF", font=("Arial", 12), fg="#000000")
        self.lblNucleo = Label(self, text="Núcleo Familiar", bg="#FFFFFF", font=("Arial", 12))

        self.txtName = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtLastName = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtLastName2 = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtId = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtDeathDate = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.calBirthDate = DateEntry(self, width=27, background='darkblue', foreground='white', borderwidth=2, selectmode="day", date_pattern="dd/mm/yyyy")
        self.cmbxGender = ttk.Combobox(self, state="readonly", values=genderList, width=27)
        self.cmbxProvince = ttk.Combobox(self, state="readonly", values=provinceList, width=27)
        self.cmbxCivilState = ttk.Combobox(self, state="readonly", values=civilStateList, width=27)
        self.cmbxNucleo = ttk.Combobox(self, state="readonly", values=self.nucleos, width=27)
        self.cmbxGender.set("...")
        self.cmbxProvince.set("...")
        self.cmbxCivilState.set("Soltero")
        self.txtId.insert(0, "0")
        self.txtLastName.insert(0, "...")
        self.txtLastName2.insert(0, "...")
        self.txtName.insert(0, "...")
        self.cmbxNucleo.set("0")

        self.btnSave = Button(self, text="Guardar", font=("Arial", 12))

    def placeObjs(self):
        self.lblName.place(x=50, y=50)
        self.lblLastName.place(x=50, y=100)
        self.lblLastName2.place(x=50, y=150)
        self.lblId.place(x=50, y=200)
        self.lblBirthDate.place(x=50, y=250)
        self.lblDeathDate.place(x=50, y=300)
        self.lblGender.place(x=50, y=350)
        self.lblProvince.place(x=50, y=400)
        self.lblCivilState.place(x=50, y=450)
        self.lblNucleo.place(x=50, y=500)

        self.txtName.place(x=250, y=50)
        self.txtLastName.place(x=250, y=100)
        self.txtLastName2.place(x=250, y=150)
        self.txtId.place(x=250, y=200)
        self.calBirthDate.place(x=250, y=250)
        self.txtDeathDate.place(x=250, y=300)
        self.cmbxGender.place(x=250, y=350)
        self.cmbxProvince.place(x=250, y=400)
        self.cmbxCivilState.place(x=250, y=450)
        self.cmbxNucleo.place(x=250, y=500)

        self.btnSave.place(x=250, y=550)

class VistaPersonasFam1(Toplevel):
    def __init__(self, fam, master = None):
        super().__init__(master)
        self.idFam = fam
        self.vistaPersonasCnfg()
        self.createObjs()
        self.placeObjs()
    
    def vistaPersonasCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("1100x500")
        self.title("Vista personas")
        self.focus_set()

    def createObjs(self):
        rowTitles = ("Cédula", "Nombre", "Apellido", "Segundo Apellido", "Fecha de nacimiento", "Fecha de fallecimiento", "Género", "Provincia", "Estado civil", "Nucleo Familiar")
        self.table = ttk.Treeview(self, columns=rowTitles, show="headings")
        self.table["columns"] = rowTitles
        self.table.column("Cédula", anchor=CENTER, width=100)
        self.table.column("Nombre", anchor=CENTER, width=100)
        self.table.column("Apellido", anchor=CENTER, width=100)
        self.table.column("Segundo Apellido", anchor=CENTER, width=100)
        self.table.column("Fecha de nacimiento", anchor=CENTER, width=100)
        self.table.column("Fecha de fallecimiento", anchor=CENTER, width=100)
        self.table.column("Género", anchor=CENTER, width=100)
        self.table.column("Provincia", anchor=CENTER, width=100)
        self.table.column("Estado civil", anchor=CENTER, width=100)
        self.table.column("Nucleo Familiar", anchor=CENTER, width=100)

        self.table.heading("Cédula", text="Cédula", anchor=CENTER)
        self.table.heading("Nombre", text="Nombre", anchor=CENTER)
        self.table.heading("Apellido", text="Apellido", anchor=CENTER)
        self.table.heading("Segundo Apellido", text="Segundo Apellido", anchor=CENTER)
        self.table.heading("Fecha de nacimiento", text="Fecha de nacimiento", anchor=CENTER)
        self.table.heading("Fecha de fallecimiento", text="Fecha de fallecimiento", anchor=CENTER)
        self.table.heading("Género", text="Género", anchor=CENTER)
        self.table.heading("Provincia", text="Provincia", anchor=CENTER)
        self.table.heading("Estado civil", text="Estado civil", anchor=CENTER)
        self.table.heading("Nucleo Familiar", text="Nucleo Familiar", anchor=CENTER)

        conn = DBConnection()
        if self.idFam == 1:
            listaPersonasFam = conn.getDataP1()
        else:
            listaPersonasFam = conn.getDataPer2()
        conn.closeConnection()

        for persona in listaPersonasFam:
            self.table.insert("", END, values=(persona.getId(), persona.getName(), persona.getLastName1(), persona.getLastName2(), persona.getBirthDate(), persona.getDeathDate(), persona.getGender(), persona.getProvince(), persona.getCivilState(), persona.getNucleo()))

    def placeObjs(self):
        self.table.place(x=50, y=50)
        

class Search(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.searchCnfg()
        self.createObjs()
        self.placeObjs()

    def searchCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("300x300+10+10")
        self.title("Buscar persona")
        self.focus_set()

    def createObjs(self):
        self.choice = IntVar()
        self.radFamChoice = tk.Radiobutton(self, text="Familia 1", variable=self.choice, value=1)
        self.radFamChoice2 = tk.Radiobutton(self, text="Familia 2", variable=self.choice, value=2)

        self.btnSelected = Button(self, text="Seleccionar", font=("Arial", 12))
        

    
    def placeObjs(self):
        self.radFamChoice.place(x=50, y=50)
        self.radFamChoice2.place(x=150, y=50)

        self.btnSelected.place(x=90, y=150)

class AfterSearch(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.afterSearchCnfg()
        self.createObjs()
        self.placeObjs()

    
    def afterSearchCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Datos de Familia")
        self.focus_set()

    def createObjs(self):
        questions = ("¿Cuál es la relación entre persona A y persona B?", "¿Quiénes son los primos de primer grado de X?", 
                     "¿Cuáles son todos los antepasados maternos de X?", "¿Cuáles descendientes de X están vivos actualmente?",
                     "¿Cuántas personas nacieron en los últimos 10 años?", "¿Cuáles parejas actuales tienen 2 o más hijos en común?",
                     "¿Cuántas personas fallecieron antes de cumplir 50 años?")
        self.lblReqId = Label(self, text="Ingrese la cédula de las personas:", bg="#FFFFFF", font=("Arial", 12))

        self.txtReqId = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtReqId2 = Entry(self, bg="#FFFFFF", font=("Arial", 12))

        self.btnSearch = Button(self, text="Buscar", font=("Arial", 12))
        self.btnAccept = Button(self, text="Aceptar", font=("Arial", 12))

        self.cmbxOptions = ttk.Combobox(self, state="readonly", values=questions, width=50)

    
    def placeObjs(self):
        self.cmbxOptions.place(x=50, y=50)
        self.btnAccept.place(x=400, y=50)


class FatherSonWindow(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.fatherSonCnfg()
        self.createObjs()
        self.placeObjs()

    def fatherSonCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Padre e hijo")
        self.focus_set()

    def createObjs(self):
        self.lblIdFather = Label(self, text="Cédula del padre", bg="#FFFFFF", font=("Arial", 12))
        self.lblIdSon = Label(self, text="Cédula del hijo", bg="#FFFFFF", font=("Arial", 12))
        self.txtIdFather = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtIdSon = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.btnAccept = Button(self, text="Aceptar", font=("Arial", 12))

    def placeObjs(self):
        self.lblIdFather.place(x=50, y=50)
        self.lblIdSon.place(x=50, y=100)
        self.txtIdFather.place(x=250, y=50)
        self.txtIdSon.place(x=250, y=100)
        self.btnAccept.place(x=250, y=150)


class TimeLine(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.timelineCnfg()
        self.createObjs()
        self.placeObjs()

    def timelineCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Línea de tiempo")
        self.focus_set()


    def createObjs(self):
        self.lblChoice = Label(self, text="Familia (1 o 2):", bg="#FFFFFF", font=("Arial", 12))
        self.fam_var = StringVar()
        self.txtChoice = Entry(self, bg="#FFFFFF", font=("Arial", 12), textvariable=self.fam_var, width=8)
        self.lblId = Label(self, text="Cédula:", bg="#FFFFFF", font=("Arial", 12))
        self.id_var = StringVar()
        self.txtId = Entry(self, bg="#FFFFFF", font=("Arial", 12), textvariable=self.id_var, width=12)
        self.btnWatch = Button(self, text="Ver", font=("Arial", 12))
        self.btnClose = Button(self, text="Cerrar", font=("Arial", 12), command=self.destroy)


    
    def placeObjs(self):
        self.lblChoice.place(x=50, y=50)
        self.txtChoice.place(x=150, y=50)
        self.lblId.place(x=50, y=100)
        self.txtId.place(x=150, y=100)
        self.btnWatch.place(x=50, y=150)
        self.btnClose.place(x=150, y=150)