#Para que este programa funcione con la base de datos, se necesita instalar el modulo pyodbc que se usa en el archivo DataBaseConnection.py
#Seguidamente se deberá instalar Access DataBase Engine x64 Redistributable y tener Microsoft Access instalado
#https://www.microsoft.com/en-us/download/details.aspx?id=54920
#para que el calendario funcione se debe instalar el módulo tkcalendar 
from WindowCnfg import *
from tkinter import messagebox


def simulation_tick(root):
    conn = DBConnection()
    try:
        unions_cross = conn.auto_create_unions_cross(prob_attempt=0.50, max_pairs=4)

        total_deaths = 0
        for fam in (1, 2):
            conn.tick_birthdays(fam)                 # no persiste edad
            total_deaths += conn.tick_deaths(fam, prob=0.05)

        births_cross = conn.tick_births_cross(prob_per_couple=0.35)

        root.winfo_toplevel().title(
            f"Árbol genealógico | Cross Unions:{unions_cross}  Cross Births:{births_cross}  Fallec:{total_deaths}"
        )
    except Exception as e:
        print("Simulación error:", e)
    finally:
        conn.closeConnection()
    root.after(SIM_INTERVAL_MS, lambda: simulation_tick(root))


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


# ================== HANDLERS DE CONSULTA (NUEVOS) ==================
def _ask_two_ids_and_run(newSearch, fam, action):
    try:
        a = int(newSearch.txtReqId.get().strip())
        b = int(newSearch.txtReqId2.get().strip())
    except:
        messagebox.showerror("Error", "Ingrese dos cédulas válidas.", parent=newSearch); return
    conn = DBConnection()
    try:
        desc, path = conn.find_relationship(a, fam, b, fam)  # misma familia seleccionada
        if not path:
            messagebox.showinfo("Relación", desc, parent=newSearch); return
        ruta = " → ".join([f"{pid}(F{ff})" for (pid, ff) in path])
        messagebox.showinfo("Relación", f"{desc}\nRuta mínima: {ruta}", parent=newSearch)
    finally:
        conn.closeConnection()

def _ask_one_id_and_list(newSearch, fam, fn, title):
    try:
        x = int(newSearch.txtReqId.get().strip())
    except:
        messagebox.showerror("Error", "Ingrese una cédula válida.", parent=newSearch); return
    conn = DBConnection()
    try:
        rows = fn(conn, x, fam)
        if not rows:
            messagebox.showinfo(title, "Sin resultados.", parent=newSearch); return
        if title == "Línea materna":
            txt = " → ".join([f"{pid}(F{ff})" for (pid, ff) in rows])
        else:
            txt = "\n".join([f"{pid}(F{ff})" for (pid, ff) in rows]) if isinstance(rows[0], tuple) else "\n".join(map(str, rows))
        messagebox.showinfo(title, txt, parent=newSearch)
    finally:
        conn.closeConnection()

def _list_recent_births_ui(parent):
    conn = DBConnection()
    try:
        rows = conn.list_recent_births(10)
        if not rows:
            messagebox.showinfo("Nacidos últimos 10 años", "No hay registros.", parent=parent); return
        txt = "\n".join([f"{pid}(F{fam}) - {fec}" for (pid, fam, fec) in rows[:50]])
        messagebox.showinfo("Nacidos últimos 10 años", txt, parent=parent)
    finally:
        conn.closeConnection()

def _list_couples_2_children_ui(parent):
    conn = DBConnection()
    try:
        rows = conn.list_couples_with_children(2)
        if not rows:
            messagebox.showinfo("Parejas con ≥2 hijos", "No hay parejas.", parent=parent); return
        txt = "\n".join([f"P:{p[0]}(F{p[1]}) - M:{m[0]}(F{m[1]})  Hijos:{cnt}" for ((p),(m),cnt) in rows])
        messagebox.showinfo("Parejas con ≥2 hijos", txt, parent=parent)
    finally:
        conn.closeConnection()

def _list_died_before_50_ui(parent):
    conn = DBConnection()
    try:
        rows = conn.list_died_before_age(50)
        if not rows:
            messagebox.showinfo("Fallecidos < 50", "No hay registros.", parent=parent); return
        txt = "\n".join([f"{pid}(F{fam}) - Edad:{edad} - Fecha:{fec}" for (pid, fam, edad, fec) in rows[:50]])
        messagebox.showinfo("Fallecidos antes de 50", txt, parent=parent)
    finally:
        conn.closeConnection()


def questionHandler(newSearch, fam):
    selection = newSearch.cmbxOptions.get()
    if selection == "¿Cuál es la relación entre persona A y persona B?":
        newSearch.lblReqId.place(x=50, y=200)
        newSearch.txtReqId.place(x=50, y=250)
        newSearch.txtReqId2.place(x=50, y=300)
        newSearch.btnSearch.place(x=50, y=350)
        newSearch.btnSearch.configure(command=lambda: _ask_two_ids_and_run(newSearch, fam, "relation"))
    elif selection == "¿Quiénes son los primos de primer grado de X?":
        newSearch.lblReqId.config(text="Ingrese cédula de X:")
        newSearch.lblReqId.place(x=50, y=200)
        newSearch.txtReqId.place(x=50, y=250)
        newSearch.txtReqId2.place_forget()
        newSearch.btnSearch.place(x=50, y=300)
        newSearch.btnSearch.configure(command=lambda: _ask_one_id_and_list(newSearch, fam,
            lambda c, x, f: c.list_first_cousins(x, f), "Primos de 1er grado"))

    elif selection == "¿Cuáles son todos los antepasados maternos de X?":
        newSearch.lblReqId.config(text="Ingrese cédula de X:")
        newSearch.lblReqId.place(x=50, y=200)
        newSearch.txtReqId.place(x=50, y=250)
        newSearch.txtReqId2.place_forget()
        newSearch.btnSearch.place(x=50, y=300)
        newSearch.btnSearch.configure(command=lambda: _ask_one_id_and_list(newSearch, fam,
            lambda c, x, f: c.list_maternal_ancestors(x, f, 10), "Línea materna"))

    elif selection == "¿Cuáles descendientes de X están vivos actualmente?":
        newSearch.lblReqId.config(text="Ingrese cédula de X:")
        newSearch.lblReqId.place(x=50, y=200)
        newSearch.txtReqId.place(x=50, y=250)
        newSearch.txtReqId2.place_forget()
        newSearch.btnSearch.place(x=50, y=300)
        newSearch.btnSearch.configure(command=lambda: _ask_one_id_and_list(newSearch, fam,
            lambda c, x, f: c.list_living_descendants(x), "Descendientes vivos"))

    elif selection == "¿Cuántas personas nacieron en los últimos 10 años?":
        _list_recent_births_ui(newSearch)

    elif selection == "¿Cuáles parejas actuales tienen 2 o más hijos en común?":
        _list_couples_2_children_ui(newSearch)

    elif selection == "¿Cuántas personas fallecieron antes de cumplir 50 años?":
        _list_died_before_50_ui(newSearch)

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
            deathDate = None if newPerson.txtDeathDate.get().strip() == "" else str(newPerson.txtDeathDate.get())
            per = Persona(personId = int(newPerson.txtId.get()), name=newPerson.txtName.get(), lastName1=newPerson.txtLastName.get(), 
                        lastName2=newPerson.txtLastName2.get(), birthDate=str(newPerson.calBirthDate.get()), deathDate=deathDate,
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
            deathDate = None if newPerson.txtDeathDate.get().strip() == "" else str(newPerson.txtDeathDate.get())
            per = Persona(personId = int(newPerson.txtId.get()), name=newPerson.txtName.get(), lastName1=newPerson.txtLastName.get(), 
                        lastName2=newPerson.txtLastName2.get(), birthDate=str(newPerson.calBirthDate.get()), deathDate=deathDate,
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
    SIM_INTERVAL_MS = 10_000  # 10 segundos
    screen = PrincipalWindow()
    mnuHandler()
    screen.after(SIM_INTERVAL_MS, lambda: simulation_tick(screen))
    mainloop()