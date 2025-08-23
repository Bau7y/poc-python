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


def showSearch():
    search = Search()
    search.grab_set()


def savePersonFam2(newPerson):
    if newPerson.txtName.get() == "" or newPerson.txtLastName.get() == "" or newPerson.txtLastName2.get() == "" or newPerson.txtName.get() == "..." or newPerson.txtLastName.get() == "...":
        messagebox.showerror("Error", "Debe llenar todos los campos")
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
            messagebox.showerror("Error", "La persona no pudo ser registrada...")

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
    screen.mnuArchivo.add_command(label="")
    screen.mnuArchivo.add_command(label="Borrar todo", underline=0, command=borrarTodo)
    screen.mnuArchivo.add_command(label="Salir", command=screen.quit)

    screen.mnuVer.add_command(label="Ver Familia 1", underline=0, command=showFam1)
    screen.mnuVer.add_command(label="Ver Familia 2", underline=0, command=showFam2)

    screen.mnuBuscar.add_command(label="Buscar", underline=0, command=showSearch)


if __name__ == "__main__":
    screen = PrincipalWindow()
    mnuHandler()
    mainloop()