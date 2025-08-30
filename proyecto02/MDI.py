#Para que este programa funcione con la base de datos, se necesita instalar el modulo pyodbc que se usa en el archivo DataBaseConnection.py
#Seguidamente se deberá instalar Access DataBase Engine x64 Redistributable y tener Microsoft Access instalado
#https://www.microsoft.com/en-us/download/details.aspx?id=54920
#para que el calendario funcione se debe instalar el módulo tkcalendar 
from WindowCnfg import *
from tkinter import messagebox


def showFam2():
    fam2 = VistaPersonasFam1(2)
    fam2.grab_set()


def showFam1():
    fam1 = VistaPersonasFam1(1)
    fam1.grab_set()

def insertParentChild(fam: int, win):
    try:
        parent_id = int(win.txtIdFather.get().strip())
        child_id  = int(win.txtIdSon.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Las cédulas deben ser numéricas.", parent=win)
        return

    conn = DBConnection()
    try:
        # Valida existencia de ambos
        parent = conn.searchPerson(parent_id, fam)
        child  = conn.searchPerson(child_id, fam)
        if parent is None or child is None:
            messagebox.showerror("Error", "Padre o hijo no existen en la familia seleccionada.", parent=win)
            return

        # Inserta vínculo padre-hijo
        created = conn.insert_parent_child_PH(parent_id, child_id, fam)
        if not created:
            messagebox.showinfo("Información", "La relación padre/hijo ya existía.", parent=win)
        else:
            messagebox.showinfo("Éxito", "Relación padre/hijo registrada.", parent=win)

        # Busca si este hijo ya tenía otro progenitor
        other_parent_id = conn.get_other_parent_for_child(child_id, parent_id, fam)
        if other_parent_id:
            try:
                made_union = conn.ensure_union_if_shared_child(parent_id, other_parent_id, fam)
                if made_union:
                    messagebox.showinfo(
                        "Éxito",
                        f"Se registró la pareja automáticamente (comparten hijo): {parent_id} y {other_parent_id}",
                        parent=win
                    )
            except Exception as e:
                messagebox.showwarning(
                    "Atención",
                    "Padre/hijo guardado. No se pudo crear la unión automática.\n"
                    "Revisa nombres/columnas de RelacionesFam{fam}.\n\n"
                    f"Detalle: {e}",
                    parent=win
                )

        win.destroy()

    finally:
        conn.closeConnection()


def addParentsFam1():
    add1 = FatherSonWindow()
    add1.btnAccept.configure(command=lambda: insertParentChild(1, add1))
    add1.grab_set()


def addParentsFam2():
    add2 = FatherSonWindow()
    add2.btnAccept.configure(command=lambda: insertParentChild(2, add2))
    add2.grab_set()


def personFound(newSearch, fam):
    try:
        conn = DBConnection()
        person1 = conn.searchPerson(newSearch.txtReqId.get(), fam)
        person2 = conn.searchPerson(newSearch.txtReqId2.get(), fam)
        conn.closeConnection()
        if person1 != None and person2 != None:
            messagebox.showinfo("Éxito", "La persona fue encontrada con éxito!!!", parent=newSearch)
            newSearch.txtReqId.place_forget()
            newSearch.lblReqId.place_forget()
            newSearch.txtReqId2.place_forget()
            newSearch.btnSearch.place_forget()
        else:
            messagebox.showerror("Error", "No se encontró a la persona", parent=newSearch)
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar un ID válido", parent=newSearch)


def questionHandler(newSearch, fam):
    if newSearch.cmbxOptions.get() == "¿Cuál es la relación entre persona A y persona B?":
        newSearch.lblReqId.place(x=50, y=200)
        newSearch.txtReqId.place(x=50, y=250)
        newSearch.txtReqId2.place(x=50, y=300)
        newSearch.btnSearch.place(x=50, y=350)
        newSearch.btnSearch.configure(command=lambda: personFound(newSearch, fam))
    elif newSearch.cmbxOptions.get() == "¿Quiénes son los primos de primer grado de X?":
        messagebox.showinfo("Respuesta", "Los primos de primer grado de X son: ...", parent=newSearch)
    elif newSearch.cmbxOptions.get() == "¿Cuáles son todos los antepasados maternos de X?":
        messagebox.showinfo("Respuesta", "Los antepasados maternos de X son: ...", parent=newSearch)
    elif newSearch.cmbxOptions.get() == "¿Cuáles descendientes de X están vivos actualmente?":
        messagebox.showinfo("Respuesta", "Los descendientes de X están vivos actualmente: ...", parent=newSearch)
    elif newSearch.cmbxOptions.get() == "¿Cuántas personas nacieron en los últimos 10 años?":
        messagebox.showinfo("Respuesta", "Las personas nacieron en los últimos 10 años: ...", parent=newSearch)
    elif newSearch.cmbxOptions.get() == "¿Cuáles parejas actuales tienen 2 o más hijos en común?":
        messagebox.showinfo("Respuesta", "Las parejas actuales tienen 2 o más hijos en común: ...", parent=newSearch)
    elif newSearch.cmbxOptions.get() == "¿Cuántas personas fallecieron antes de cumplir 50 años?":
        messagebox.showinfo("Respuesta", "Las personas fallecieron antes de cumplir 50 años: ...", parent=newSearch)

def lookingFor(searchWindow):
    if searchWindow.choice.get() == 1 or searchWindow.choice.get() == 2:
        searchWindow.destroy()
        newSearch = AfterSearch()
        newSearch.btnAccept.configure(command= lambda: questionHandler(newSearch, searchWindow.choice.get()))
    else:
        messagebox.showerror("Error", "Debe seleccionar una opcion", parent=searchWindow)


def showSearch():
    search = Search()
    search.btnSelected.configure(command= lambda: lookingFor(search))
    search.grab_set()


def savePersonFam2(newPerson):
    if newPerson.txtName.get() == "" or newPerson.txtLastName.get() == "" or newPerson.txtLastName2.get() == "" or newPerson.txtName.get() == "..." or newPerson.txtLastName.get() == "...":
        messagebox.showerror("Error", "Debe llenar todos los campos", parent=newPerson)
    else:
        try:
            per = Persona(personId = int(newPerson.txtId.get()), name=newPerson.txtName.get(), lastName1=newPerson.txtLastName.get(), 
                        lastName2=newPerson.txtLastName2.get(), birthDate=str(newPerson.calBirthDate.get()), deathDate=str(newPerson.calDeathDate.get()),
                            gender=newPerson.cmbxGender.get(), province=newPerson.cmbxProvince.get(), civilState=newPerson.cmbxCivilState.get(), nucleo=int(newPerson.cmbxNucleo.get()))
            conn = DBConnection()
            conn.dataInsertFam2(per)
            conn.closeConnection()
            messagebox.showinfo("Éxito", "La persona fue registrada con éxito!!!")
            newPerson.destroy()
        except:
            messagebox.showerror("Error", "La persona no pudo ser registrada...", parent=newPerson)

def savePerson(newPerson):
    if newPerson.txtName.get() == "" or newPerson.txtLastName.get() == "" or newPerson.txtLastName2.get() == "" or newPerson.txtName.get() == "..." or newPerson.txtLastName.get() == "...":
        messagebox.showerror("Error", "Debe llenar todos los campos")
    else:
        try:
            per = Persona(personId = int(newPerson.txtId.get()), name=newPerson.txtName.get(), lastName1=newPerson.txtLastName.get(), 
                        lastName2=newPerson.txtLastName2.get(), birthDate=str(newPerson.calBirthDate.get()), deathDate=str(newPerson.calDeathDate.get()),
                            gender=newPerson.cmbxGender.get(), province=newPerson.cmbxProvince.get(), civilState=newPerson.cmbxCivilState.get(), nucleo=int(newPerson.cmbxNucleo.get()))
            conn = DBConnection()
            conn.dataInsertFam1(per)
            conn.closeConnection()
            messagebox.showinfo("Éxito", "La persona fue registrada con éxito!!!")
            newPerson.destroy()
        except:
            messagebox.showerror("Error", "La persona no pudo ser registrada...")


def newPersonFam2():
    newPerson = NewPersonWindow()
    newPerson.btnSave.configure(command = lambda: savePersonFam2(newPerson))
    newPerson.grab_set()


def newPerson():
    newPerson = NewPersonWindow()
    newPerson.btnSave.configure(command = lambda: savePerson(newPerson))
    newPerson.grab_set()

def borrarTodo():
    answer = messagebox.askyesno("Borrar todo", "¿Está seguro que desea borrar todos los datos?")
    if answer:
        conn = DBConnection()
        conn.delAllDataP1()
        conn.delAllDataP2()
        conn.closeConnection()
        messagebox.showinfo("Éxito", "Se borraron todos los datos de la familia 1 y 2")


def mnuHandler():
    screen.mnuArchivo.add_command(label="Añadir a Familia 1", underline=0, command=newPerson)
    screen.mnuArchivo.add_command(label="Añadir a Familia 2", underline=0, command=newPersonFam2)
    screen.mnuArchivo.add_separator()
    screen.mnuArchivo.add_command(label="Anexar Padres Familia 1", command=addParentsFam1)
    screen.mnuArchivo.add_command(label="Anexar Padres Familia 2", command=addParentsFam2)
    screen.mnuArchivo.add_separator()
    screen.mnuArchivo.add_command(label="Borrar todo", underline=0, command=borrarTodo)
    screen.mnuArchivo.add_command(label="Salir", command=screen.quit)

    screen.mnuVer.add_command(label="Ver Familia 1", underline=0, command=showFam1)
    screen.mnuVer.add_command(label="Ver Familia 2", underline=0, command=showFam2)
    screen.mnuVer.add_separator()
    screen.mnuVer.add_command(label="Ver Linea de Tiempo Familia 1")
    screen.mnuVer.add_command(label="Ver Linea de Tiempo Familia 2")

    screen.mnuBuscar.add_command(label="Buscar", underline=0, command=showSearch)


if __name__ == "__main__":
    screen = PrincipalWindow()
    mnuHandler()
    mainloop()