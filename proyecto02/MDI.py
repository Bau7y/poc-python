#Para que este programa funcione con la base de datos, se necesita instalar el modulo pyodbc que se usa en el archivo DataBaseConnection.py
#Seguidamente se deberá instalar Access DataBase Engine x64 Redistributable y tener Microsoft Access instalado
#https://www.microsoft.com/en-us/download/details.aspx?id=54920
#para que el calendario funcione se debe instalar el módulo tkcalendar 
from WindowCnfg import *
from tkinter import messagebox

def newPerson():
    newPerson = NewPersonWindow()
    newPerson.grab_set()

def mnuHandler():
    screen.mnuArchivo.add_command(label="Nueva Persona", underline=0, command=newPerson)
    screen.mnuArchivo.add_command(label="Salir", command=screen.quit)


if __name__ == "__main__":
    screen = PrincipalWindow()
    mnuHandler()
    mainloop()