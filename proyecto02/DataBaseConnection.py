from pyodbc import *
from Persona import *
import os
from datetime import datetime


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
        self.conn.commit()


    def dataInsertFam2(self, per):
        self.cursor.execute("INSERT INTO Personas2 (ID, Nombre, Apellido, Apellido2, FechaNacimiento, FechaFallecimiento, Genero, Provincia, EstadoCivil, IdNucleo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (int(per.getId()), per.getName().upper(), per.getLastName1().upper(), per.getLastName2().upper(), per.getBirthDate(), per.getDeathDate(), per.getGender(), per.getProvince(), per.getCivilState(), int(per.getNucleo())))
        self.conn.commit()

    
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
            self.cursor.execute("SELECT * FROM Personas WHERE ID = ?", (pid, ))
        else:
            self.cursor.execute("SELECT * FROM Personas2 WHERE ID = ?", (pid, ))
        data = self.cursor.fetchone()
        if data != None:
            person = Persona(personId=data[0], name=data[1], lastName1=data[2], lastName2=data[3], birthDate=data[4], 
                             deathDate=data[5], gender=data[6], province=data[7], civilState=data[8], nucleo=data[9])
            return person
        else:
            return None
        
    def _tables_by_family(self, fam: int):
        if fam == 1:
            return ("Personas", "PadreHijo1", "RelacionesFam1")
        else:
            return ("Personas2", "PadreHijo2", "RelacionesFam2")

    def _normalize_couple(self, a: int, b: int):
        return (a, b) if a <= b else (b, a)
    

    def insert_parent_child_PH(self, parent_id: int, child_id: int, fam: int) -> bool:
        _, ph_table, _ = self._tables_by_family(fam)

        self.cursor.execute(f"SELECT 1 FROM {ph_table} WHERE IdPadre=? AND IdHijo=?", (int(parent_id), int(child_id)))
        if self.cursor.fetchone():
            return False
        
        self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(parent_id), int(child_id)))
        self.conn.commit()
        return True
    
    def get_other_parent_for_child(self, child_id: int, known_parent_id: int, fam: int):
        _, ph_table, _ = self._tables_by_family(fam)
        self.cursor.execute(
            f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=? AND IdPadre<>?",
            (int(child_id), int(known_parent_id))
        )
        row = self.cursor.fetchone()
        return int(row[0]) if row else None
    
    def ensure_union_if_shared_child(self, parent_a_id: int, parent_b_id: int, fam: int) -> bool:
        person_table, _, rel_table = self._tables_by_family(fam)
        pa = self.searchPerson(parent_a_id, fam)
        pb = self.searchPerson(parent_b_id, fam)
        if pa is None or pb is None:
            raise ValueError("No se encontraron ambos padres en la familia indicada.")
        
        def pick_roles(p1, p2):
            g1 = (p1.getGender() or "").strip().lower()
            g2 = (p2.getGender() or "").strip().lower()
            if "masculino" in g1 and "femenino" in g2:
                return (p1.getId(), p2.getId())
            if "femenino" in g1 and "masculino" in g2:
                return (p2.getId(), p1.getId())
            a, b = self._normalize_couple(p1.getId(), p2.getId())
            return (a, b)
        padre_id, madre_id = pick_roles(pa, pb)

        self.cursor.execute(
            f"SELECT 1 FROM {rel_table} WHERE (IdPadre=? AND IdMadre=?) OR (IdPadre=? AND IdMadre=?)",
            (int(padre_id), int(madre_id), int(madre_id), int(padre_id))
        )
        if self.cursor.fetchone():
            return False
        
        self.cursor.execute(
            f"INSERT INTO {rel_table} (IdPadre, IdMadre, FechaUnion, TipoUnion) VALUES (?, ?, ?, ?)",
            (int(padre_id), int(madre_id), datetime.now(), "Por descendencia")
        )
        self.conn.commit()
        return True

conn = DBConnection()