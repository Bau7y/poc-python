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
        self.cursor.execute("INSERT INTO Personas (ID, Nombre, Apellido, Apellido2, FechaNacimiento, FechaFallecimiento, Genero, Provincia, EstadoCivil) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (int(per.getId()), per.getName().upper(), per.getLastName1().upper(), per.getLastName2().upper(), per.getBirthDate(), per.getDeathDate(), per.getGender(), per.getProvince(), per.getCivilState(), per.getNucleo()))
        self.cursor.commit()

        self.cursor.execute("SELECT @@IDENTITY")
        newId = self.cursor.fetchone()[0]

        self.actualizarRelaciones(int(per.getNucleo()))

        return newId
    
    def actualizarRelaciones(self, nucleo):
        self.cursor.execute("SELECT ID FROM Personas WHERE IdNucleo=?", (nucleo,))
        ids = [row[0] for row in self.cursor.fetchall()]

        if len(ids) >= 2:
            id1, id2 = ids[0], ids[1]

            self.cursor.execute("SELECT COUNT(*) FROM RelacionesFam1 WHERE IdNucleo=?", (nucleo, ))
            existe = self.cursor.fetchone()[0]
            if existe == 0:
                self.cursor.execute("INSERT INTO RelacionesFam1 (IdUnion, IdPadre, IdMadre) VALUES (?, ?, ?)", (nucleo, id1, id2))
            else:
                self.cursor.execute("UPDATE RelacionesFam1 SET IdPadre=?, IdMadre=? WHERE IdUnion=?", (id1, id2, nucleo))
            self.cursor.commit()


    def dataInsertFam2(self, per):
        self.cursor.execute("INSERT INTO Personas2 (ID, Nombre, Apellido, Apellido2, FechaNacimiento, FechaFallecimiento, Genero, Provincia, EstadoCivil, IdNucleo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (int(per.getId()), per.getName().upper(), per.getLastName1().upper(), per.getLastName2().upper(), per.getBirthDate(), per.getDeathDate(), per.getGender(), per.getProvince(), per.getCivilState(), int(per.getNucleo())))
        self.cursor.commit()

        self.cursor.execute("SELECT @@IDENTITY")
        newId = self.cursor.fetchone()[0]

        self.actualizarRelacionesFam2(int(per.getNucleo()))

        return newId
    
    def actualizarRelacionesFam2(self, nucleo):
        self.cursor.execute("SELECT ID FROM Personas2 WHERE IdNucleo=?", (nucleo, ))
        ids = [row[0] for row in self.cursor.fetchall()]

        if len(ids) >= 2:
            id1, id2 = ids[0], ids[1]

            self.cursor.execute("SELECT COUNT(*) FROM RelacionesFam2 WHERE IdNucleo=?", (nucleo,))
            existe = self.cursor.fetchone()[0]
            if existe == 0:
                self.cursor.execute("INSERT INTO RelacionesFam2 (IdUnion, IdPadre, IdMadre) VALUES (?, ?, ?)", (nucleo,id1, id2))
            else:
                self.cursor.execute("UPDATE RelacionesFam2 SET IdPadre=?, IdMadre=? WHERE IdUnion=?", (id1, id2, nucleo))
            self.cursor.commit()

    
    def delAllDataP1(self):
        self.cursor.execute("DELETE * FROM Personas")
        self.conn.commit()


conn = DBConnection()