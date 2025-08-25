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

    def getDataP1(self):
        self.cursor.execute("SELECT * FROM Personas")
        data = self.cursor.fetchall()
        listaPersonas = []
        for row in data:
            persona = Persona(personId=row[0], name=row[1], lastName1=row[2], lastName2=row[3], birthDate=row[4], deathDate=row[5], gender=row[6], province=row[7], civilState=row[8], nucleo=row[9])
            listaPersonas.append(persona)
        return listaPersonas
    
    def getDataPer2(self):
        self.cursor.execute("SELECT * FROM Personas2")
        data = self.cursor.fetchall()
        listaPersonas = []
        for row in data:
            persona = Persona(personId=row[0], name=row[1], lastName1=row[2], lastName2=row[3], birthDate=row[4], deathDate=row[5], gender=row[6], province=row[7], civilState=row[8], nucleo=row[9])
            listaPersonas.append(persona)
        return listaPersonas
    
    def dataInsertFam1(self, per):
        self.cursor.execute("INSERT INTO Personas (ID, Nombre, Apellido, Apellido2, FechaNacimiento, FechaFallecimiento, Genero, Provincia, EstadoCivil, IdNucleo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (int(per.getId()), per.getName().upper(), per.getLastName1().upper(), per.getLastName2().upper(), per.getBirthDate(), per.getDeathDate(), per.getGender(), per.getProvince(), per.getCivilState(), per.getNucleo()))
        self.cursor.commit()


    def dataInsertFam2(self, per):
        self.cursor.execute("INSERT INTO Personas2 (ID, Nombre, Apellido, Apellido2, FechaNacimiento, FechaFallecimiento, Genero, Provincia, EstadoCivil, IdNucleo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (int(per.getId()), per.getName().upper(), per.getLastName1().upper(), per.getLastName2().upper(), per.getBirthDate(), per.getDeathDate(), per.getGender(), per.getProvince(), per.getCivilState(), int(per.getNucleo())))
        self.cursor.commit()

    
    def delAllDataP1(self):
        self.cursor.execute("DELETE * FROM Personas")
        self.cursor.execute("DELETE * FROM RelacionesFam1")
        self.conn.commit()
    
    def delAllDataP2(self):
        self.cursor.execute("DELETE * FROM Personas2")
        self.cursor.execute("DELETE * FROM RelacionesFam2")
        self.conn.commit()


    def searchPerson(self, pid, fam):
        if fam == 1:
            self.cursor.execute("SELECT * FROM Personas WHERE ID = ?", (pid))
        else:
            self.cursor.execute("SELECT * FROM Personas2 WHERE ID = ?", (pid))
        data = self.cursor.fetchone()
        if data != None:
            person = Persona(personId=data[0], name=data[1], lastName1=data[2], lastName2=data[3], birthDate=data[4], 
                             deathDate=data[5], gender=data[6], province=data[7], civilState=data[8], nucleo=data[9])
            return person
        else:
            return None
        

conn = DBConnection()