from pyodbc import *
from Persona import *

class DBConnection:
    def __init__(self):
        self.driver = r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        self.DBPath = r"Dbq=DB/BasePersonas.accdb;"
        self.conn = connect(self.driver+self.DBPath)
        self.cursor = self.conn.cursor()

    def closeConnection(self):
        self.cursor.close()
        self.conn.close()

    def getData(self):
        self.cursor.execute("SELECT * FROM Personas")
        data = self.cursor.fetchall()
        listaPersonas = []
        for row in data:
            persona = Persona(personId=row[0], name=row[1])
            listaPersonas.append(persona)
        return listaPersonas
