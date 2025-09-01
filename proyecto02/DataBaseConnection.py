from pyodbc import *
from Persona import Persona
import os
from datetime import datetime
import datetime as dt
import random

class DBConnection:
    def __init__(self):
        self.driver =r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        baseDir = os.path.dirname(os.path.abspath(__file__))
        dbFile = os.path.join(baseDir, "DB", "BasePersonas.accdb")
        self.DBPath = rf"Dbq={dbFile};"

        self.conn = connect(self.driver + self.DBPath)
        self.cursor = self.conn.cursor()
        self._ensure_hist_table()

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
        deathDate = per.getDeathDate() if per.getDeathDate() not in ("", None) else None
        self.cursor.execute("""
            INSERT INTO Personas (ID, Nombre, Apellido, Apellido2, FechaNacimiento,
                                FechaFallecimiento, Genero, Provincia, EstadoCivil, IdNucleo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (int(per.getId()), per.getName().upper(), per.getLastName1().upper(), per.getLastName2().upper(),
            per.getBirthDate(), deathDate, per.getGender(), per.getProvince(),
            per.getCivilState(), per.getNucleo())
        )
        self.conn.commit()


    def dataInsertFam2(self, per):
        deathDate = per.getDeathDate() if per.getDeathDate() not in ("", None) else None
        self.cursor.execute("""
            INSERT INTO Personas2 (ID, Nombre, Apellido, Apellido2, FechaNacimiento,
                                FechaFallecimiento, Genero, Provincia, EstadoCivil, IdNucleo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (int(per.getId()), per.getName().upper(), per.getLastName1().upper(), per.getLastName2().upper(),
            per.getBirthDate(), deathDate, per.getGender(), per.getProvince(),
            per.getCivilState(), per.getNucleo())
        )
        self.conn.commit()

    
    def resetAllData(self):
        self.cursor.execute("DELETE * FROM HistorialEventos")
        self.cursor.execute("DELETE * FROM RelacionesFam1")
        self.cursor.execute("DELETE * FROM PadreHijo1")
        self.cursor.execute("DELETE * FROM Tutorias")
        self.cursor.execute("DELETE * FROM PadreHijo2")
        self.cursor.execute("DELETE * FROM RelacionesFam2")
        self.cursor.execute("DELETE * FROM RelacionesCross")
        self.cursor.execute("DELETE * FROM Personas")
        self.cursor.execute("DELETE * FROM Personas2")
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
        
    #----------Utilidades
    def _tables_by_family(self, fam: int):
        if fam == 1:
            return ("Personas", "RelacionesFam1", "PadreHijo1")
        else:
            return ("Personas2", "RelacionesFam2", "PadreHijo2")
        

    def _normalize_couple(self, a: int, b: int):
        return (a, b) if a <= b else (b, a)
    
    
    def _col_exists(self, table: str, column: str) -> bool:
        cols = [r.column_name.lower() for r in self.cursor.columns(table=table)]
        return column.lower() in cols
    
    
    def _to_date(self, d):
        if d is None: return None
        if isinstance(d, dt.datetime): 
            return d.date()
        if isinstance(d, dt.date): 
            return d
        s = str(d).strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
            try: 
                return dt.datetime.strptime(s, fmt).date()
            except: 
                pass
        return None

    def _calc_age_from_birth(self, birth_date, ref_date=None):
        """
        Calcula edad desde la fecha de nacimiento. No persiste nada.
        """
        b = self._to_date(birth_date)
        if b is None:
            return None
        today = ref_date or dt.date.today()
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))
    
    def _searchPerson_any(self, pid: int):
        """Devuelve (persona, fam) buscando en ambas familias, o (None, None)."""
        p = self.searchPerson(pid, 1)
        if p: return p, 1
        p = self.searchPerson(pid, 2)
        if p: return p, 2
        return None, None
    
    def _is_alive(self, pid: int, fam: int) -> bool:
        person_table, _, _ = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT FechaFallecimiento FROM {person_table} WHERE ID=?", (int(pid),))
        r = self.cursor.fetchone()
        return (r is not None) and (r[0] is None)
    
    def _log_event(self, pid:int, fam:int, tipo:str, detalle:str, fecha=None):
        """Inserta en HistorialEventos. Asegura la tabla antes de escribir."""
        # Garantiza existencia de la tabla
        try:
            self.cursor.execute("SELECT 1 FROM HistorialEventos WHERE 1=0")
        except Exception:
            try:
                self.cursor.execute(
                    "CREATE TABLE HistorialEventos ("
                    "IdPersona INTEGER, Familia INTEGER, Fecha DATETIME, "
                    "Tipo TEXT(50), Detalle TEXT)"
                )
                self.conn.commit()
            except Exception:
                return  # si Access no deja crearla por algún motivo, no rompemos

        ts = fecha or dt.datetime.now()
        try:
            self.cursor.execute(
                "INSERT INTO HistorialEventos (IdPersona, Familia, Fecha, Tipo, Detalle) "
                "VALUES (?, ?, ?, ?, ?)",
                (int(pid), int(fam), ts, tipo, detalle)
            )
            self.conn.commit()
        except Exception:
            pass

    def _person_exists(self, pid:int, fam:int) -> bool:
        person_table, _, _ = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT 1 FROM {person_table} WHERE ID=?", (int(pid),))
        return self.cursor.fetchone() is not None
    

    def _parents_of_child(self, child_id:int, fam_child:int):
        """Devuelve lista de (parent_id, fam_parent). Usa PH de la familia del hijo."""
        _, _, ph_table = self._tables_by_family(fam_child)
        self.cursor.execute(f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=?", (int(child_id),))
        out = []
        for (pid,) in self.cursor.fetchall():
            p, f = self._searchPerson_any(int(pid))  # ya lo tienes en Punto 3
            if p: out.append((int(pid), int(f)))
        return out
    

    def insert_parent_child_PH(self, parent_id: int, child_id: int, fam: int) -> bool:
        _, _, ph_table = self._tables_by_family(fam)

        self.cursor.execute(f"SELECT 1 FROM {ph_table} WHERE IdPadre=? AND IdHijo=?", (int(parent_id), int(child_id)))
        if self.cursor.fetchone():
            return False
        
        self.cursor.execute(f"SELECT COUNT(*) FROM {ph_table} WHERE IdHijo=?", (int(child_id),))
        cnt = self.cursor.fetchone()[0]
        if cnt >= 2:
            raise ValueError("Este hijo ya tiene dos progenitores registrados.")
        
        self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(parent_id), int(child_id)))
        self.conn.commit()
        return True
    
    def get_other_parent_for_child(self, child_id: int, known_parent_id: int, fam: int):
        _, _, ph_table = self._tables_by_family(fam)
        self.cursor.execute(
            f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=? AND IdPadre<>?",
            (int(child_id), int(known_parent_id))
        )
        row = self.cursor.fetchone()
        return int(row[0]) if row else None
    
    def ensure_union_if_shared_child(self, parent_a_id: int, parent_b_id: int, fam: int) -> bool:
        # Detecta familias reales de cada progenitor
        pa, fa = self._searchPerson_any(parent_a_id)
        pb, fb = self._searchPerson_any(parent_b_id)
        if pa is None or pb is None:
            raise ValueError("No se encontraron ambos padres en ninguna familia.")
        
        # Helper: asignar roles por género si se puede (solo para consistencia visual)
        def pick_roles(p1, f1, p2, f2):
            g1 = (p1.getGender() or "").strip().lower()
            g2 = (p2.getGender() or "").strip().lower()
            # padre = masculino, madre = femenino (si no, orden estable por ID)
            if "masculino" in g1 and "femenino" in g2:
                return (p1.getId(), f1, p2.getId(), f2)
            if "femenino" in g1 and "masculino" in g2:
                return (p2.getId(), f2, p1.getId(), f1)
            # estable por ID
            if int(p1.getId()) <= int(p2.getId()):
                return (p1.getId(), f1, p2.getId(), f2)
            else:
                return (p2.getId(), f2, p1.getId(), f1)

        # MISMA FAMILIA → RelacionesFam{fam}
        if fa == fb:
            person_table, rel_table, _ = self._tables_by_family(fa)
            padre_id, padre_fam, madre_id, madre_fam = pick_roles(pa, fa, pb, fb)
            # ¿Existe?
            self.cursor.execute(
                f"SELECT 1 FROM {rel_table} WHERE (IdPadre=? AND IdMadre=?) OR (IdPadre=? AND IdMadre=?)",
                (int(padre_id), int(madre_id), int(madre_id), int(padre_id))
            )
            if self.cursor.fetchone():
                return False
            # Insertar
            self.cursor.execute(
                f"INSERT INTO {rel_table} (IdPadre, IdMadre, FechaUnion, TipoUnion) VALUES (?, ?, ?, ?)",
                (int(padre_id), int(madre_id), datetime.now(), "Por descendencia")
            )
            # Opcional: estado civil e historial
            try:
                self.cursor.execute(f"UPDATE {person_table} SET EstadoCivil=? WHERE ID IN (?,?)", ("Casado", int(padre_id), int(madre_id)))
                self._log_event(int(padre_id), fa, "Unión (interna)", f"Con {int(madre_id)} (F{fa}) por descendencia")
                self._log_event(int(madre_id), fa, "Unión (interna)", f"Con {int(padre_id)} (F{fa}) por descendencia")
            except Exception:
                pass
            self.conn.commit()
            return True

        # DISTINTAS FAMILIAS → RelacionesCross
        self._ensure_relaciones_cross()
        padre_id, padre_fam, madre_id, madre_fam = pick_roles(pa, fa, pb, fb)
        # evita duplicado en cualquier orden
        self.cursor.execute(
            """SELECT 1 FROM RelacionesCross
            WHERE (IdPersonaA=? AND FamA=? AND IdPersonaB=? AND FamB=?)
                OR (IdPersonaA=? AND FamA=? AND IdPersonaB=? AND FamB=?)""",
            (int(padre_id), int(padre_fam), int(madre_id), int(madre_fam),
            int(madre_id), int(madre_fam), int(padre_id), int(padre_fam))
        )
        if self.cursor.fetchone():
            return False

        self.cursor.execute(
            "INSERT INTO RelacionesCross (IdPersonaA, FamA, IdPersonaB, FamB, FechaUnion, TipoUnion) VALUES (?, ?, ?, ?, ?, ?)",
            (int(padre_id), int(padre_fam), int(madre_id), int(madre_fam), datetime.now(), "Por descendencia")
        )
        # Opcional: estado civil e historial
        try:
            ptA, _, _ = self._tables_by_family(padre_fam)
            ptB, _, _ = self._tables_by_family(madre_fam)
            self.cursor.execute(f"UPDATE {ptA} SET EstadoCivil=? WHERE ID=?", ("Casado", int(padre_id)))
            self.cursor.execute(f"UPDATE {ptB} SET EstadoCivil=? WHERE ID=?", ("Casado", int(madre_id)))
            self._log_event(int(padre_id), int(padre_fam), "Unión (cross)", f"Con {int(madre_id)} (F{madre_fam}) por descendencia")
            self._log_event(int(madre_id), int(madre_fam), "Unión (cross)", f"Con {int(padre_id)} (F{padre_fam}) por descendencia")
        except Exception:
            pass

        self.conn.commit()
        return True
    

    # ------- Cumpleaños (+1 año simulado) -------
    def tick_birthdays(self, fam:int) -> int:
        """
        Sin campo 'Edad' en BD: no persistimos nada y devolvemos 0.
        La edad se calculará al vuelo con _calc_age_from_birth cuando haga falta.
        """
        return 0

    # ------- Fallecimientos aleatorios -------
    def tick_deaths(self, fam:int, prob:float=0.05, sim_date: dt.date | None = None) -> int:
        person_table, _, _ = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT ID, FechaFallecimiento FROM {person_table}")
        rows = self.cursor.fetchall()

        deaths = 0
        for (pid, fdef) in rows:
            if fdef:
                continue
            if random.random() < prob:
                fecha = sim_date or dt.date.today()
                self.cursor.execute(f"UPDATE {person_table} SET FechaFallecimiento=? WHERE ID=?", (fecha, int(pid)))
                self.conn.commit()
                deaths += 1
                # evento + efectos
                self._log_event(int(pid), fam, "Fallecimiento", "Marcado por simulación [SIM]", fecha)
                try:
                    self._handle_death_side_effects(int(pid), fam)  # mantiene 'Viudo' del cónyuge
                except Exception as e:
                    print("Side-effects error:", e)
        return deaths

    def _age_or_calc(self, person, fam:int):
        """Obtiene edad persistida si existe, o la calcula desde FechaNacimiento."""
        _, _ = self._tables_by_family(fam)

        # Calcula desde fecha nacimiento
        try:
            d = dt.datetime.strptime(str(person.getBirthDate()), "%d/%m/%Y").date()
        except:
            # Si Access guarda como fecha nativa
            bd = person.getBirthDate()
            if hasattr(bd, "timestamp"):
                d = dt.datetime.fromtimestamp(bd.timestamp()).date()
            else:
                d = dt.date.today()
        hoy = dt.date.today()
        return hoy.year - d.year - ((hoy.month, hoy.day) < (d.month, d.day))

    def _are_eligible_to_unite(self, pa, pb, fam:int):
        if not self._is_opposite_gender(pa, pb):
            return False

        # 1) >=18 años
        ea = self._calc_age_from_birth(pa.getBirthDate())
        eb = self._calc_age_from_birth(pb.getBirthDate())
        if ea is None or eb is None:
            return False
        if ea < 18 or eb < 18:
            return False

        # 2) diferencia <= 15
        if abs(ea - eb) > 15:
            return False

        # 3) compatibilidad simple
        comp = 50
        if (pa.getProvince() or "").strip().lower() == (pb.getProvince() or "").strip().lower():
            comp += 25
        if (pa.getCivilState() or "").lower().startswith("solt") and (pb.getCivilState() or "").lower().startswith("solt"):
            comp += 15
        comp += random.randint(0, 20)
        if comp < 70:
            return False

        # 4) evitar hermanos (comparten al menos un IdPadre en PH de la familia consultada)
        _, _, ph_table = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=?", (int(pa.getId()),))
        padres_a = {r[0] for r in self.cursor.fetchall()}
        self.cursor.execute(f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=?", (int(pb.getId()),))
        padres_b = {r[0] for r in self.cursor.fetchall()}
        if padres_a & padres_b:
            return False

        return True

    def tick_births(self, fam:int, prob_per_couple:float=0.15):
        return 0
    
        # ----------- Cross unions (F1 <-> F2) -----------
    def _table_exists(self, table_name: str) -> bool:
        try:
            for r in self.cursor.tables(tableType='TABLE'):
                if r.table_name.lower() == table_name.lower():
                    return True
        except Exception:
            pass
        try:
            self.cursor.execute(f"SELECT 1 FROM {table_name} WHERE 1=0")
            _ = self.cursor.fetchone()
            return True
        except Exception:
            return False

    def _ensure_relaciones_cross(self):
        if not self._table_exists("RelacionesCross"):
            self.cursor.execute("""
                CREATE TABLE RelacionesCross (
                    IdPersonaA LONG,
                    FamA BYTE,
                    IdPersonaB LONG,
                    FamB BYTE,
                    FechaUnion DATETIME,
                    TipoUnion TEXT(50)
                )
            """)
            # índice único para evitar duplicados
            try:
                self.cursor.execute(
                    "CREATE UNIQUE INDEX UX_RelCross ON RelacionesCross (IdPersonaA, FamA, IdPersonaB, FamB)"
                )
            except Exception:
                pass
            self.conn.commit()

    def _is_in_union_any(self, person_id: int, fam: int) -> bool:
        # Uniones internas
        _, rel_table, _ = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT 1 FROM {rel_table} WHERE IdPadre=? OR IdMadre=?", (int(person_id), int(person_id)))
        if self.cursor.fetchone():
            return True
        # Uniones cross (si existe)
        if self._table_exists("RelacionesCross"):
            self.cursor.execute(
                "SELECT 1 FROM RelacionesCross WHERE (IdPersonaA=? AND FamA=?) OR (IdPersonaB=? AND FamB=?)",
                (int(person_id), fam, int(person_id), fam)
            )
            if self.cursor.fetchone():
                return True
        return False

    def _list_eligible_singles_cross(self, fam: int):
        """
        Devuelve objetos Persona de la familia 'fam' que estén vivos, solteros
        y sin unión previa (ni interna ni cross).
        """
        person_table, _, _ = self._tables_by_family(fam)
        self.cursor.execute(
            f"""
            SELECT ID, Nombre, Apellido, Apellido2, FechaNacimiento, FechaFallecimiento,
                   Genero, Provincia, EstadoCivil, IdNucleo
            FROM {person_table}
            WHERE FechaFallecimiento IS NULL
              AND (EstadoCivil IS NULL OR EstadoCivil LIKE 'Solt%')
            """
        )
        rows = self.cursor.fetchall()
        singles = []
        for r in rows:
            if not self._is_in_union_any(r[0], fam):
                singles.append(
                    Persona(
                        personId=r[0], name=r[1], lastName1=r[2], lastName2=r[3],
                        birthDate=r[4], deathDate=r[5], gender=r[6],
                        province=r[7], civilState=r[8], nucleo=r[9]
                    )
                )
        return singles

    def auto_create_unions_cross(self, prob_attempt: float = 0.40, max_pairs: int = 3,
                             sim_date: dt.date | None = None, mark_sim: bool = False) -> int:
        self._ensure_relaciones_cross()
        singles1 = self._list_eligible_singles_cross(1)
        singles2 = self._list_eligible_singles_cross(2)
        if not singles1 or not singles2:
            return 0

        random.shuffle(singles1); random.shuffle(singles2)
        created = 0
        for a, b in zip(singles1, singles2):
            if created >= max_pairs: break
            if random.random() > prob_attempt: continue
            for a, b in zip(singles1, singles2):
                if created >= max_pairs: break
                if random.random() > prob_attempt: continue
                
                if not self._is_opposite_gender(a, b):
                    continue
                if not self._are_eligible_to_unite(a, b, 1):
                    continue
            if not self._are_eligible_to_unite(a, b, 1):  # chequeo básico
                continue

            # evitar duplicado
            self.cursor.execute(
                """SELECT 1 FROM RelacionesCross
                WHERE (IdPersonaA=? AND FamA=1 AND IdPersonaB=? AND FamB=2)
                    OR (IdPersonaA=? AND FamA=2 AND IdPersonaB=? AND FamB=1)""",
                (int(a.getId()), int(b.getId()), int(b.getId()), int(a.getId()))
            )
            if self.cursor.fetchone(): 
                continue

            tipo = "Afinidad Cross" + (" [SIM]" if mark_sim else "")
            fecha = sim_date or dt.date.today()
            self.cursor.execute(
                "INSERT INTO RelacionesCross (IdPersonaA, FamA, IdPersonaB, FamB, FechaUnion, TipoUnion) VALUES (?, 1, ?, 2, ?, ?)",
                (int(a.getId()), int(b.getId()), fecha, tipo)
            )
            # historial
            self._log_event(int(a.getId()), 1, "Unión (cross)", f"Con {int(b.getId())} (F2){' [SIM]' if mark_sim else ''}", fecha)
            self._log_event(int(b.getId()), 2, "Unión (cross)", f"Con {int(a.getId())} (F1){' [SIM]' if mark_sim else ''}", fecha)

            # estado civil
            self.cursor.execute("UPDATE Personas  SET EstadoCivil=? WHERE ID=?", ("Casado", int(a.getId())))
            self.cursor.execute("UPDATE Personas2 SET EstadoCivil=? WHERE ID=?", ("Casado", int(b.getId())))
            self.conn.commit()
            created += 1
        return created

    def _assign_roles_cross(self, pa, pb):
        """
        Devuelve: (father_id, father_fam, mother_id, mother_fam)
        Si no se puede detectar por género, usa un orden consistente.
        """
        g1 = (pa.getGender() or "").strip().lower()
        g2 = (pb.getGender() or "").strip().lower()
        if "masculino" in g1 and "femenino" in g2:
            return pa.getId(), 1, pb.getId(), 2
        if "femenino" in g1 and "masculino" in g2:
            return pb.getId(), 2, pa.getId(), 1
        # Sin claridad: decide por ID para tener estabilidad
        if pa.getId() <= pb.getId():
            return pa.getId(), 1, pb.getId(), 2
        else:
            return pb.getId(), 2, pa.getId(), 1

    def list_cross_couples(self):
        """
        Devuelve lista de tuplas (idA, famA, idB, famB) de RelacionesCross
        donde no estén fallecidos ambos.
        """
        if not self._table_exists("RelacionesCross"):
            return []
        couples = []
        self.cursor.execute("SELECT IdPersonaA, FamA, IdPersonaB, FamB FROM RelacionesCross")
        for (ida, fama, idb, famb) in self.cursor.fetchall():
            # Vivos? (al menos uno)
            pa = self.searchPerson(ida, fama)
            pb = self.searchPerson(idb, famb)
            if not pa or not pb:
                continue
            if (pa.getDeathDate() is None) or (pb.getDeathDate() is None):
                couples.append((int(ida), int(fama), int(idb), int(famb)))
        return couples

    def tick_births_cross(self, prob_per_couple: float = 0.25, sim_date: dt.date | None = None) -> int:
        births = 0
        couples = self.list_cross_couples()
        if not couples:
            return births

        for (ida, fama, idb, famb) in couples:
            pa = self.searchPerson(ida, fama)
            pb = self.searchPerson(idb, famb)
            if pa is None or pb is None: 
                continue
            if not self._are_eligible_to_unite(pa, pb, 1):
                continue
            if random.random() >= prob_per_couple:
                continue

            father_id, father_fam, mother_id, mother_fam = self._assign_roles_cross(pa, pb)
            bebe_fam = father_fam
            person_table, _, ph_table = self._tables_by_family(bebe_fam)

            # nuevo ID no existente
            new_id = random.randint(10_000_000, 99_999_999)
            self.cursor.execute(f"SELECT 1 FROM {person_table} WHERE ID=?", (int(new_id),))
            if self.cursor.fetchone():
                continue

            genero = random.choice(["Masculino","Femenino"])
            nombre = random.choice(["Juan","Carlos","Pedro","José","Diego"] if genero.startswith("M") else
                                ["Ana","María","Laura","Sofía","Lucía"])
            padre = pa if father_fam==fama else pb
            madre = pb if father_fam==fama else pa
            last1 = padre.getLastName1()
            last2 = madre.getLastName2()
            provincia = random.choice([pa.getProvince(), pb.getProvince()])
            nucleo = padre.getNucleo()
            fecha = sim_date or dt.date.today()

            bebe = Persona(new_id, nombre, last1, last2, fecha, None, genero, provincia, "Soltero", nucleo)
            if bebe_fam == 1: self.dataInsertFam1(bebe)
            else:              self.dataInsertFam2(bebe)

            # PH en la familia del bebé (padre y madre)
            self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(father_id), int(new_id)))
            self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(mother_id), int(new_id)))
            self.conn.commit()

            # historial
            self._log_event(int(new_id), int(bebe_fam), "Nacimiento", "Nació por simulación [SIM]", fecha)
            self._log_event(int(father_id), int(father_fam), "Nacimiento de hijo", f"Hijo {int(new_id)} [SIM]", fecha)
            self._log_event(int(mother_id), int(mother_fam), "Nacimiento de hijo", f"Hijo {int(new_id)} [SIM]", fecha)

            births += 1
        return births
    # ===================== EFECTOS COLATERALES =====================
    # ---------- Viudez automática ----------
    def _set_widow_internal(self, deceased_id: int, fam: int):
        person_table, rel_table, _ = self._tables_by_family(fam)
        # ¿Era padre/madre en una relación interna?
        self.cursor.execute(
            f"SELECT IdPadre, IdMadre FROM {rel_table} WHERE IdPadre=? OR IdMadre=?",
            (int(deceased_id), int(deceased_id))
        )
        rows = self.cursor.fetchall()
        spouses = set()
        for (p, m) in rows:
            if p == deceased_id: spouses.add(m)
            if m == deceased_id: spouses.add(p)
        for sp in spouses:
            # Solo si el/la cónyuge está vivo(a)
            if self._is_alive(sp, fam):
                self.cursor.execute(f"UPDATE {person_table} SET EstadoCivil=? WHERE ID=?", ("Viudo", int(sp)))
                self.conn.commit()
                self._log_event(sp, fam, "Viudez", f"Quedó viudo(a) por fallecimiento de {deceased_id}")


    def _set_widow_cross(self, deceased_id: int, fam: int):
        if not self._table_exists("RelacionesCross"): return
        other_id, other_fam = None, None
        # ¿A era IdPersonaA?
        self.cursor.execute(
            "SELECT IdPersonaB, FamB FROM RelacionesCross WHERE IdPersonaA=? AND FamA=?",
            (int(deceased_id), fam)
        )
        r = self.cursor.fetchone()
        if r: other_id, other_fam = int(r[0]), int(r[1])
        else:
            self.cursor.execute(
                "SELECT IdPersonaA, FamA FROM RelacionesCross WHERE IdPersonaB=? AND FamB=?",
                (int(deceased_id), fam)
            )
            r = self.cursor.fetchone()
            if r: other_id, other_fam = int(r[0]), int(r[1])

        if other_id and other_fam and self._is_alive(other_id, other_fam):
            person_table, _, _ = self._tables_by_family(other_fam)
            self.cursor.execute(f"UPDATE {person_table} SET EstadoCivil=? WHERE ID=?", ("Viudo", int(other_id)))
            self.conn.commit()
            self._log_event(other_id, other_fam, "Viudez", f"Quedó viudo(a) por fallecimiento de {deceased_id} (cross)")

    # ---------- Tutor legal para huérfanos ----------
    def _parents_of(self, child_id: int, fam_child: int):
        """Devuelve lista de tuplas (parent_id, fam_parent) a partir del PH de la familia del menor."""
        _, _, ph_table = self._tables_by_family(fam_child)
        self.cursor.execute(f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=?", (int(child_id),))
        parents = []
        for (pid,) in self.cursor.fetchall():
            p, f = self._searchPerson_any(int(pid))
            if p: parents.append((int(pid), int(f)))
        return parents  # puede venir 0,1,2 según datos

    def _children_of(self, parent_id: int, fam_of_ph: int):
        """Hijos de un padre/madre usando PH de la familia 'fam_of_ph'."""
        _, _, ph_table = self._tables_by_family(fam_of_ph)
        self.cursor.execute(f"SELECT IdHijo FROM {ph_table} WHERE IdPadre=?", (int(parent_id),))
        return [int(r[0]) for r in self.cursor.fetchall()]

    def _siblings_in_same_family(self, child_id: int, fam_child: int):
        """Hermanos del menor (mismo padre y/o madre) dentro de la MISMA familia del menor."""
        sibs = set()
        # Padres del menor (con su familia real)
        parents = self._parents_of(child_id, fam_child)
        if not parents: return []
        # Para cada padre, busca hijos en el PH de la familia del menor (ahí quedó el vínculo al nacer)
        _, _, ph_table = self._tables_by_family(fam_child)
        for (pid, _) in parents:
            self.cursor.execute(f"SELECT IdHijo FROM {ph_table} WHERE IdPadre=?", (int(pid),))
            for (hid,) in self.cursor.fetchall():
                if int(hid) != int(child_id):
                    sibs.add(int(hid))
        return list(sibs)

    def _grandparents(self, parent_id: int, fam_parent: int):
        """Devuelve IDs de abuelos de 'parent_id' buscando en PH de la familia del propio padre/madre."""
        _, _, ph_table = self._tables_by_family(fam_parent)
        self.cursor.execute(f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=?", (int(parent_id),))
        return [int(r[0]) for r in self.cursor.fetchall()]

    def _choose_tutor(self, child_id: int, fam_child: int):
        """Estrategia: 1) Hermano mayor (>=18) vivo en la misma familia; 2) Abuelo(a) vivo(a) más longevo(a)."""
        # 1) Hermanos
        sibs = self._siblings_in_same_family(child_id, fam_child)
        candidates = []
        for sid in sibs:
            sp, _ = self._searchPerson_any(sid)
            if not sp: continue
            if self._is_alive(sid, fam_child):
                age = self._calc_age_from_birth(sp.getBirthDate())
                if age is not None and age >= 18:
                    candidates.append((sid, fam_child, age))
        if candidates:
            # el mayor
            candidates.sort(key=lambda x: x[2], reverse=True)
            return candidates[0][0], candidates[0][1]

        # 2) Abuelos
        parents = self._parents_of(child_id, fam_child)
        gp_candidates = []
        for (pid, pfam) in parents:
            for gid in self._grandparents(pid, pfam):
                # el abuelo puede pertenecer a fam del propio padre/madre
                if self._is_alive(gid, pfam):
                    gp, _ = self._searchPerson_any(gid)
                    age = self._calc_age_from_birth(gp.getBirthDate()) if gp else None
                    if age is not None and age >= 18:
                        gp_candidates.append((gid, pfam, age))
        if gp_candidates:
            gp_candidates.sort(key=lambda x: x[2], reverse=True)
            return gp_candidates[0][0], gp_candidates[0][1]

        return None, None  # sin tutor válido

    def _ensure_tutor_if_orphan(self, child_id: int, fam_child: int):
        """Si ambos padres han fallecido (o no existen), asigna tutor y registra evento."""
        parents = self._parents_of(child_id, fam_child)
        if len(parents) < 2:
            return  # requiere dos progenitores para considerar orfandad “plena”
        all_dead = True
        for (pid, pfam) in parents:
            if self._is_alive(pid, pfam):
                all_dead = False; break
        if not all_dead:
            return

        tutor_id, tutor_fam = self._choose_tutor(child_id, fam_child)
        if tutor_id and tutor_fam:
            # Registrar en Tutorias (si existe)
            try:
                if self._table_exists("Tutorias"):
                    from datetime import datetime
                    self.cursor.execute(
                        "INSERT INTO Tutorias (IdMenor, FamMenor, IdTutor, FamTutor, Fecha, Motivo) VALUES (?, ?, ?, ?, ?, ?)",
                        (int(child_id), fam_child, int(tutor_id), tutor_fam, datetime.now(), "AmbosPadresFallecidos")
                    )
                    self.conn.commit()
                self._log_event(child_id, fam_child, "TutorAsignado", f"Tutor {tutor_id} (Fam {tutor_fam}) por orfandad")
            except Exception:
                pass
        else:
            self._log_event(child_id, fam_child, "TutorPendiente", "No se encontró tutor disponible")

    # ---------- Efectos al fallecer alguien ----------
    def _handle_death_side_effects(self, deceased_id: int, fam: int):
        # 1) Viudez
        self._set_widow_internal(deceased_id, fam)
        self._set_widow_cross(deceased_id, fam)

        # 2) Tutoría para hijos huérfanos
        # Hijos en PH de ambas familias, porque pudo ser padre/madre de niños en fam 1 o 2 (por nacimientos cross)
        for fam_ph in (1, 2):
            _, _, ph_table = self._tables_by_family(fam_ph)
            self.cursor.execute(f"SELECT IdHijo FROM {ph_table} WHERE IdPadre=?", (int(deceased_id),))
            for (hid,) in self.cursor.fetchall():
                # El hijo 'hid' vive (pertenece) a 'fam_ph'; verificar orfandad y asignar tutor
                self._ensure_tutor_if_orphan(int(hid), fam_ph)


    # ================== CONSULTAS (NUEVAS) ==================

    def _spouses_of(self, pid:int, fam:int):
        """(NUEVO) Cónyuges del pid: internos y cross."""
        spouses = []
        _, rel_table, _ = self._tables_by_family(fam)
        # internas
        self.cursor.execute(f"SELECT IdPadre, IdMadre FROM {rel_table} WHERE IdPadre=? OR IdMadre=?", (int(pid), int(pid)))
        for (p,m) in self.cursor.fetchall():
            if p == pid: spouses.append((int(m), fam, "interna"))
            if m == pid: spouses.append((int(p), fam, "interna"))
        # cross
        if self._table_exists("RelacionesCross"):
            self.cursor.execute("SELECT IdPersonaB, FamB FROM RelacionesCross WHERE IdPersonaA=? AND FamA=?", (int(pid), fam))
            spouses += [(int(sid), int(sf), "cross") for (sid, sf) in self.cursor.fetchall()]
            self.cursor.execute("SELECT IdPersonaA, FamA FROM RelacionesCross WHERE IdPersonaB=? AND FamB=?", (int(pid), fam))
            spouses += [(int(sid), int(sf), "cross") for (sid, sf) in self.cursor.fetchall()]
        return spouses

    def _gender_of(self, pid:int, fam:int):
        """(NUEVO) Género en minúsculas para clasificación materna/paterna."""
        person_table, _, _ = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT Genero FROM {person_table} WHERE ID=?", (int(pid),))
        r = self.cursor.fetchone()
        return (r[0] or "").strip().lower() if r else ""

    def find_relationship(self, a_id:int, a_fam:int, b_id:int, b_fam:int):
        """(NUEVO) Relación A↔B por BFS sobre aristas: parent/child y spouse."""
        from collections import deque

        if a_id == b_id and a_fam == b_fam:
            return ("Es la misma persona.", [(a_id, a_fam)])

        def neighbors(node):
            pid, fam = node
            neigh = []
            # padres del nodo
            for (ppid, pfam) in self._parents_of(pid, fam):
                neigh.append(((ppid, pfam), "parent"))
            # hijos del nodo (pueden vivir en F1 o F2)
            for fam_ph in (1,2):
                for hid in self._children_of(pid, fam_ph):
                    neigh.append(((hid, fam_ph), "child"))
            # cónyuges
            for (sid, sfam, _) in self._spouses_of(pid, fam):
                neigh.append(((sid, sfam), "spouse"))
            return neigh

        start, goal = (a_id, a_fam), (b_id, b_fam)
        q = deque([start])
        prev = { start: (None, None) }
        seen = { start }
        found = False

        while q:
            u = q.popleft()
            if u == goal:
                found = True; break
            for (v, edge) in neighbors(u):
                if v not in seen:
                    seen.add(v); prev[v] = (u, edge); q.append(v)
        if not found:
            return ("Sin relación detectable (en los datos actuales).", [])

        # reconstruir ruta
        path, edges = [], []
        cur = goal
        while cur is not None:
            path.append(cur)
            pr, ed = prev[cur]
            if ed: edges.append(ed)
            cur = pr
        path.reverse(); edges = list(reversed(edges))

        # clasificación básica por patrones cortos
        if edges == ["parent"]: return ("Padre/Madre", path)
        if edges == ["child"]:  return ("Hijo/Hija", path)
        if edges == ["spouse"]: return ("Cónyuges", path)
        if len(edges) == 2 and set(edges) == {"parent","child"}: return ("Hermanos/as", path)
        if edges == ["parent","parent"]: return ("Abuelo/a", path)
        if edges == ["child","child"]:   return ("Nieto/a", path)
        if len(edges) == 3 and edges.count("parent")+edges.count("child") == 3:
            return ("Tío/Tía o Sobrino/a", path)
        if len(edges) == 4 and edges.count("parent")+edges.count("child") == 4:
            return ("Primos/as de primer grado", path)
        if "spouse" in edges and (edges.count("parent")+edges.count("child"))>=1:
            return ("Parentesco por afinidad (político)", path)
        return (f"Pariente a distancia {len(edges)} (ruta mínima)", path)

    def list_first_cousins(self, pid:int, fam:int):
        """(NUEVO) Primos de 1er grado de X."""
        primos = set()
        parents = self._parents_of(pid, fam)
        for (ppid, pfam) in parents:
            # abuelos de ese padre/madre
            for (gpid, gpfam) in self._parents_of(ppid, pfam):
                # hijos del abuelo = tíos (incluye al propio padre)
                for fam_ph in (1,2):
                    for unc in self._children_of(gpid, fam_ph):
                        if unc == ppid:  # saltar al padre/madre
                            continue
                        for cuz in self._children_of(unc, fam_ph):
                            primos.add((cuz, fam_ph))
        return sorted(list(primos))

    def list_maternal_ancestors(self, pid:int, fam:int, max_depth:10):
        """(NUEVO) Línea materna de X (hasta max_depth)."""
        out = []
        cur_id, cur_fam = pid, fam
        for _ in range(max_depth):
            parents = self._parents_of(cur_id, cur_fam)
            if not parents: break
            mother = None
            for (ppid, pfam) in parents:
                if "femen" in self._gender_of(ppid, pfam):
                    mother = (ppid, pfam); break
            if not mother: mother = parents[0]
            out.append(mother)
            cur_id, cur_fam = mother
        return out

    def list_living_descendants(self, pid:int):
        """(NUEVO) Descendientes vivos de X (todas las generaciones)."""
        vivos, seen = set(), set([pid])
        stack = [(pid, 1), (pid, 2)]  # explora hijos en PH1 y PH2
        while stack:
            cur, fam_ph = stack.pop()
            for hid in self._children_of(cur, fam_ph):
                if (hid, fam_ph) in seen: 
                    continue
                seen.add((hid, fam_ph))
                if self._is_alive(hid, fam_ph):
                    vivos.add((hid, fam_ph))
                # sigue recursivo
                stack.append((hid, fam_ph))
        return sorted(list(vivos))

    def list_recent_births(self, years:int=10):
        """(NUEVO) Nacidos en los últimos N años (ambas familias)."""
        today = dt.date.today()
        cutoff = today.replace(year=today.year - years)
        out = []
        for fam in (1,2):
            person_table, _, _ = self._tables_by_family(fam)
            self.cursor.execute(f"SELECT ID, FechaNacimiento FROM {person_table}")
            for (pid, fnac) in self.cursor.fetchall():
                d = self._to_date(fnac)
                if isinstance(d, dt.datetime):   # 🔧 forzar a date si aún quedara datetime
                    d = d.date()
                if d and d >= cutoff:
                    out.append((int(pid), fam, d))
        out.sort(key=lambda x: x[2], reverse=True)
        return out

    def list_couples_with_children(self, min_children:int=2):
        """(NUEVO) Parejas con ≥N hijos (internas + cross)."""
        result = []
        # internas
        for fam in (1,2):
            _, rel_table, ph_table = self._tables_by_family(fam)
            self.cursor.execute(f"SELECT IdPadre, IdMadre FROM {rel_table}")
            for (p, m) in self.cursor.fetchall():
                self.cursor.execute(f"SELECT IdHijo FROM {ph_table} WHERE IdPadre=?", (int(p),))
                children = [int(r[0]) for r in self.cursor.fetchall()]
                cnt = 0
                for hid in children:
                    self.cursor.execute(f"SELECT 1 FROM {ph_table} WHERE IdPadre=? AND IdHijo=?", (int(m), int(hid)))
                    if self.cursor.fetchone(): cnt += 1
                if cnt >= min_children:
                    result.append(((int(p), fam), (int(m), fam), cnt))
        # cross
        if self._table_exists("RelacionesCross"):
            self.cursor.execute("SELECT IdPersonaA, FamA, IdPersonaB, FamB FROM RelacionesCross")
            for (ida, fama, idb, famb) in self.cursor.fetchall():
                pa = self.searchPerson(int(ida), int(fama))
                pb = self.searchPerson(int(idb), int(famb))
                if not pa or not pb: continue
                father_id, father_fam, mother_id, mother_fam = self._assign_roles_cross(pa, pb)
                _, _, ph_table = self._tables_by_family(father_fam)
                self.cursor.execute(f"SELECT IdHijo FROM {ph_table} WHERE IdPadre=?", (int(father_id),))
                children = [int(r[0]) for r in self.cursor.fetchall()]
                cnt = 0
                for hid in children:
                    self.cursor.execute(f"SELECT 1 FROM {ph_table} WHERE IdPadre=? AND IdHijo=?", (int(mother_id), int(hid)))
                    if self.cursor.fetchone(): cnt += 1
                if cnt >= min_children:
                    result.append(((int(father_id), father_fam), (int(mother_id), mother_fam), cnt))
        return sorted(result, key=lambda x: x[2], reverse=True)

    def list_died_before_age(self, max_age:int=50):
        """(NUEVO) Fallecidos con edad < max_age."""
        out = []
        for fam in (1,2):
            person_table, _, _ = self._tables_by_family(fam)
            self.cursor.execute(f"SELECT ID, FechaNacimiento, FechaFallecimiento FROM {person_table} WHERE FechaFallecimiento IS NOT NULL")
            for (pid, fnac, fdef) in self.cursor.fetchall():
                b = self._to_date(fnac); d = self._to_date(fdef)
                if b and d:
                    age = d.year - b.year - ((d.month, d.day) < (b.month, b.day))
                    if age < max_age:
                        out.append((int(pid), fam, age, d))
        out.sort(key=lambda x: (x[2], x[3]))
        return out
    

    def build_person_timeline(self, pid:int, fam:int):
        """
        Línea de tiempo para una persona:
        - Nacimiento (desde Personas/2)
        - Uniones de pareja (RelacionesFam{fam} y RelacionesCross)
        - Nacimientos de hijos (desde PadreHijo1/2 con fecha del hijo)
        - Viudez (desde HistorialEventos, si existe)
        - Fallecimiento (desde Personas/2)
        Retorna: lista de dicts [{fecha: date/datetime, tipo: str, detalle: str}]
        """
        events = []

        # --- Persona base (nacimiento/fallecimiento)
        person_table, rel_table, ph_table = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT Nombre, Apellido, Apellido2, FechaNacimiento, FechaFallecimiento FROM {person_table} WHERE ID=?", (int(pid),))
        row = self.cursor.fetchone()
        if not row:
            return []
        nombre, a1, a2, fnac, fdef = row
        d_nac = self._to_date(fnac)
        d_def = self._to_date(fdef)
        if d_nac:
            events.append({"fecha": d_nac, "tipo": "Nacimiento", "detalle": f"{nombre} {a1} {a2}".strip()})
        if d_def:
            events.append({"fecha": d_def, "tipo": "Fallecimiento", "detalle": f"{nombre} {a1} {a2}".strip()})

        # --- Uniones internas (en su misma familia)
        self.cursor.execute(f"SELECT IdPadre, IdMadre, FechaUnion, TipoUnion FROM {rel_table} WHERE IdPadre=? OR IdMadre=?", (int(pid), int(pid)))
        for (p, m, fu, tu) in self.cursor.fetchall():
            spouse_id = m if p == pid else p
            fu_d = self._to_date(fu) or dt.date.today()
            events.append({"fecha": fu_d, "tipo": "Unión (interna)", "detalle": f"Con {spouse_id} (F{fam}) - {tu or ''}".strip()})

        # --- Uniones F1<->F2 (RelacionesCross)
        if self._table_exists("RelacionesCross"):
            # como A
            self.cursor.execute("SELECT IdPersonaB, FamB, FechaUnion, TipoUnion FROM RelacionesCross WHERE IdPersonaA=? AND FamA=?", (int(pid), int(fam)))
            for (sid, sf, fu, tu) in self.cursor.fetchall():
                fu_d = self._to_date(fu) or dt.date.today()
                events.append({"fecha": fu_d, "tipo": "Unión (cross)", "detalle": f"Con {sid} (F{sf}) - {tu or ''}".strip()})
            # como B
            self.cursor.execute("SELECT IdPersonaA, FamA, FechaUnion, TipoUnion FROM RelacionesCross WHERE IdPersonaB=? AND FamB=?", (int(pid), int(fam)))
            for (sid, sf, fu, tu) in self.cursor.fetchall():
                fu_d = self._to_date(fu) or dt.date.today()
                events.append({"fecha": fu_d, "tipo": "Unión (cross)", "detalle": f"Con {sid} (F{sf}) - {tu or ''}".strip()})

        # --- Nacimientos de hijos (revisar PH1 y PH2 porque el hijo puede vivir en cualquiera)
        for fam_ph in (1, 2):
            _, _, ph_t = self._tables_by_family(fam_ph)
            self.cursor.execute(f"SELECT IdHijo FROM {ph_t} WHERE IdPadre=?", (int(pid),))
            hijos = [int(r[0]) for r in self.cursor.fetchall()]
            if not hijos:
                continue
            # Para cada hijo, tomar su fecha de nacimiento desde su tabla Personas/2 (según familia del hijo)
            for hid in hijos:
                # primero intentamos en fam_ph
                pt, _, _ = self._tables_by_family(fam_ph)
                self.cursor.execute(f"SELECT FechaNacimiento FROM {pt} WHERE ID=?", (int(hid),))
                r = self.cursor.fetchone()
                if not r or not r[0]:
                    # fallback: buscar en la otra familia por si el hijo fue movido
                    other_fam = 1 if fam_ph == 2 else 2
                    pt2, _, _ = self._tables_by_family(other_fam)
                    self.cursor.execute(f"SELECT FechaNacimiento FROM {pt2} WHERE ID=?", (int(hid),))
                    r = self.cursor.fetchone()
                if r and r[0]:
                    fh = self._to_date(r[0])
                    if fh:
                        events.append({"fecha": fh, "tipo": "Nacimiento de hijo", "detalle": f"Hijo {hid} (F{fam_ph})"})

        # --- Viudez desde HistorialEventos (si existe)
        try:
            self.cursor.execute("SELECT Fecha, Detalle FROM HistorialEventos WHERE IdPersona=? AND Familia=? AND Tipo='Viudez' ORDER BY Fecha", (int(pid), int(fam)))
            for (fec, det) in self.cursor.fetchall():
                events.append({"fecha": fec, "tipo": "Viudez", "detalle": det or ""})
        except Exception:
            pass

        # Ordenar por fecha
        events.sort(key=lambda x: self._to_date(x["fecha"]) or dt.date.min)
        return events

    def reset_sim_changes(self):
        """
        Limpia SOLO lo generado por la simulación:
        - Borra bebés creados por sim (identificados por HistorialEventos 'Nacimiento' [SIM]) y sus PH.
        - Borra uniones CROSS con '[SIM]'.
        - Revive fallecidos marcados [SIM] y revierte 'Viudo' cuando corresponda.
        - Recalcula EstadoCivil a 'Soltero' para personas que ya no tienen NINGUNA unión tras borrar cross [SIM].
        - Borra eventos [SIM].
        """
        summary = {"personas_borradas":0, "ph_borrados":0, "cross_borradas":0, "fallecimientos_revertidos":0, "viudez_revertida":0, "eventos_borrados":0}
        self.cursor.execute("DELETE * FROM Tutorias")

        # 1) bebés [SIM]
        sim_babies = []
        try:
            self.cursor.execute("SELECT IdPersona, Familia FROM HistorialEventos WHERE Tipo='Nacimiento' AND Detalle LIKE '%[SIM]%'")
            sim_babies = [(int(r[0]), int(r[1])) for r in self.cursor.fetchall()]
        except Exception:
            pass
        for (pid, fam) in sim_babies:
            _, _, ph_table = self._tables_by_family(fam)
            self.cursor.execute(f"DELETE FROM {ph_table} WHERE IdHijo=?", (int(pid),))
            summary["ph_borrados"] += self.cursor.rowcount or 0
            person_table, _, _ = self._tables_by_family(fam)
            self.cursor.execute(f"DELETE FROM {person_table} WHERE ID=?", (int(pid),))
            summary["personas_borradas"] += self.cursor.rowcount or 0
            self.conn.commit()

        # 2) personas afectadas por CROSS [SIM] (para recalcular estado civil después)
        impacted = set()
        if self._table_exists("RelacionesCross"):
            try:
                self.cursor.execute("SELECT IdPersonaA, FamA, IdPersonaB, FamB FROM RelacionesCross WHERE TipoUnion LIKE '%[SIM]%'")
                for (ida, fama, idb, famb) in self.cursor.fetchall():
                    impacted.add((int(ida), int(fama)))
                    impacted.add((int(idb), int(famb)))
            except Exception:
                pass

        # 3) borrar uniones cross [SIM]
        if self._table_exists("RelacionesCross"):
            self.cursor.execute("DELETE FROM RelacionesCross WHERE TipoUnion LIKE '%[SIM]%'")
            summary["cross_borradas"] += self.cursor.rowcount or 0
            self.conn.commit()

        # 4) revivir fallecidos [SIM] + revertir viudez si corresponde (uniones internas)
        try:
            self.cursor.execute("SELECT IdPersona, Familia FROM HistorialEventos WHERE Tipo='Fallecimiento' AND Detalle LIKE '%[SIM]%'")
            to_revive = [(int(r[0]), int(r[1])) for r in self.cursor.fetchall()]
        except Exception:
            to_revive = []
        for (pid, fam) in to_revive:
            person_table, rel_table, _ = self._tables_by_family(fam)
            self.cursor.execute(f"UPDATE {person_table} SET FechaFallecimiento=NULL WHERE ID=?", (int(pid),))
            if self.cursor.rowcount:
                summary["fallecimientos_revertidos"] += 1
            # cónyuge (interno) -> si vive, 'Casado'
            self.cursor.execute(f"SELECT IdPadre, IdMadre FROM {rel_table} WHERE IdPadre=? OR IdMadre=?", (int(pid), int(pid)))
            spouses = []
            for (p,m) in self.cursor.fetchall():
                if p == pid: spouses.append(m)
                if m == pid: spouses.append(p)
            for sp in set(spouses):
                self.cursor.execute(f"SELECT FechaFallecimiento FROM {person_table} WHERE ID=?", (int(sp),))
                r = self.cursor.fetchone()
                if r and r[0] is None:
                    self.cursor.execute(f"UPDATE {person_table} SET EstadoCivil='Casado' WHERE ID=?", (int(sp),))
                    if self.cursor.rowcount:
                        summary["viudez_revertida"] += 1
            self.conn.commit()

        # 5) Recalcular EstadoCivil='Soltero' para 'impacted' si ya NO tienen ninguna unión (ni interna ni cross)
        for (pid, fam) in impacted:
            pt, rel_table, _ = self._tables_by_family(fam)
            has_union = False
            # internas
            self.cursor.execute(f"SELECT 1 FROM {rel_table} WHERE IdPadre=? OR IdMadre=?", (int(pid), int(pid)))
            if self.cursor.fetchone():
                has_union = True
            # cross
            if not has_union and self._table_exists("RelacionesCross"):
                self.cursor.execute(
                    "SELECT 1 FROM RelacionesCross WHERE (IdPersonaA=? AND FamA=?) OR (IdPersonaB=? AND FamB=?)",
                    (int(pid), int(fam), int(pid), int(fam))
                )
                if self.cursor.fetchone():
                    has_union = True
            if not has_union:
                self.cursor.execute(f"UPDATE {pt} SET EstadoCivil='Soltero' WHERE ID=?", (int(pid),))
                self.conn.commit()

        # 6) borrar eventos [SIM]
        try:
            self.cursor.execute("DELETE FROM HistorialEventos WHERE Detalle LIKE '%[SIM]%' OR Tipo LIKE '%[SIM]%'")
            summary["eventos_borrados"] += self.cursor.rowcount or 0
            self.conn.commit()
        except Exception:
            pass

        return summary
    
    def _ensure_hist_table(self):
        """Crea HistorialEventos si no existe (Access no soporta IF NOT EXISTS)."""
        try:
            self.cursor.execute("SELECT 1 FROM HistorialEventos WHERE 1=0")
            _ = self.cursor.fetchone()
        except Exception:
            try:
                self.cursor.execute(
                    "CREATE TABLE HistorialEventos ("
                    "IdPersona INTEGER, "
                    "Familia INTEGER, "
                    "Fecha DATETIME, "
                    "Tipo TEXT(50), "
                    "Detalle TEXT)"
                )
                self.conn.commit()
            except Exception:
                pass
    
    def list_events(self, fam:int|None=None, person_id:int|None=None,
                tipo:str|None=None, date_from=None, date_to=None, limit:int=500):
        """
        Devuelve lista de dicts: {id, fam, fecha, tipo, detalle} desde HistorialEventos,
        con filtros opcionales. Si la tabla no existe, retorna [].
        """
        # Verificar existencia de tabla
        try:
            self.cursor.execute("SELECT 1 FROM HistorialEventos WHERE 1=0")
        except Exception:
            return []

        q = "SELECT IdPersona, Familia, Fecha, Tipo, Detalle FROM HistorialEventos WHERE 1=1"
        params = []
        if fam in (1,2):
            q += " AND Familia=?"; params.append(int(fam))
        if person_id is not None:
            q += " AND IdPersona=?"; params.append(int(person_id))
        if tipo and tipo.strip():
            q += " AND Tipo=?"; params.append(tipo.strip())
        if date_from is not None:
            q += " AND Fecha >= ?"; params.append(date_from)
        if date_to is not None:
            q += " AND Fecha <= ?"; params.append(date_to)
        q += " ORDER BY Fecha DESC"

        self.cursor.execute(q, tuple(params))
        rows = self.cursor.fetchall()
        return [{"id": int(pid), "fam": int(ff), "fecha": fec, "tipo": tp, "detalle": det or ""} 
                for (pid, ff, fec, tp, det) in rows[:limit]]
        

    def get_person_name(self, pid:int, fam:int) -> str:
        person_table, _, _ = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT Nombre, Apellido, Apellido2 FROM {person_table} WHERE ID=?", (int(pid),))
        r = self.cursor.fetchone()
        if not r: return ""
        nom, a1, a2 = (r[0] or "").strip(), (r[1] or "").strip(), (r[2] or "").strip()
        return f"{nom} {a1} {a2}".strip()
    

    def _is_opposite_gender(self, pa, pb) -> bool:
        g1 = ((pa.getGender() or "").strip().lower())
        g2 = ((pb.getGender() or "").strip().lower())
        return (("masculino" in g1 and "femenino" in g2) or
                ("femenino" in g1 and "masculino" in g2))




conn = DBConnection()