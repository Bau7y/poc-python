from pyodbc import *
from Persona import *
import os

class DBConnection:
    def __init__(self):
        self.driver =r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        baseDir = os.path.dirname(os.path.abspath(__file__))
        dbFile = os.path.join(baseDir, "DB", "BasePersonas.accdb")
        self.DBPath = rf"Dbq={dbFile};"

        self.conn = connect(self.driver + self.DBPath)
        self.cursor = self.conn.cursor()

    def closeConnection(self):
        self.cursor.close()
        self.conn.close()

    def getData(self):
        self.cursor.execute("SELECT * FROM Personas")
        data = self.cursor.fetchall()
        listaPersonas = []
        for row in data:
            persona = Persona(personId=row[0], name=row[1], birthDate=row[2], deathDate=row[3], gender=row[4], province=row[5], civilState=row[6])
            listaPersonas.append(persona)
        return listaPersonas

conn = DBConnection()