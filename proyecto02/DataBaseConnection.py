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
            return ("Personas", "RelacionesFam1", "PadreHijo1")
        else:
            return ("Personas2", "RelacionesFam2", "PadreHijo2")
        

    def _normalize_couple(self, a: int, b: int):
        return (a, b) if a <= b else (b, a)
    
    
    def _col_exists(self, table: str, column: str) -> bool:
        cols = [r.column_name.lower() for r in self.cursor.columns(table=table)]
        return column.lower() in cols
    
    
    def _to_date(self, d):
        """
        Convierte un valor proveniente de Access a date() de Python si es posible.
        Acepta objetos date/datetime o strings en formatos comunes.
        """
        if d is None or d == "":
            return None
        if isinstance(d, dt.date):
            return d
        if isinstance(d, dt.datetime):
            return d.date()
        s = str(d).strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
            try:
                return dt.datetime.strptime(s, fmt).date()
            except Exception:
                pass
        # Último intento si Access entrega tipo COM raro:
        try:
            return d.date()
        except Exception:
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
        person_table, rel_table, _ = self._tables_by_family(fam)
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
    

    # ------- Cumpleaños (+1 año simulado) -------
    def tick_birthdays(self, fam:int) -> int:
        """
        Sin campo 'Edad' en BD: no persistimos nada y devolvemos 0.
        La edad se calculará al vuelo con _calc_age_from_birth cuando haga falta.
        """
        return 0

    # ------- Fallecimientos aleatorios -------
    def tick_deaths(self, fam:int, prob:float=0.05):
        """
        Marca aleatoriamente fallecimientos con probabilidad 'prob' por persona viva.
        Asigna FechaFallecimiento = hoy.
        """
        person_table, _, _ = self._tables_by_family(fam)

        self.cursor.execute(f"SELECT ID, FechaFallecimiento FROM {person_table}")
        rows = self.cursor.fetchall()

        today = dt.date.today()
        deaths = 0
        for (pid, fdef) in rows:
            if fdef:  # ya fallecido
                continue
            if random.random() < prob:
                # marca fallecimiento
                self.cursor.execute(
                    f"UPDATE {person_table} SET FechaFallecimiento=? WHERE ID=?",
                    (today, int(pid))
                )
                deaths += 1

        if deaths:
            self.conn.commit()
        return deaths

    # ------- Nacimientos (hijos de parejas activas) -------
    def list_couples(self, fam:int):
        """
        Devuelve lista de tuplas (padre_id, madre_id) de RelacionesFam{fam}
        que no estén fallecidos ambos.
        """
        person_table, rel_table, _ = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT IdPadre, IdMadre FROM {rel_table}")
        couples = []
        for (p, m) in self.cursor.fetchall():
            # Chequeo básico: que existan y no estén ambos fallecidos
            self.cursor.execute(f"SELECT FechaFallecimiento FROM {person_table} WHERE ID=?", (int(p),))
            pd = self.cursor.fetchone()
            self.cursor.execute(f"SELECT FechaFallecimiento FROM {person_table} WHERE ID=?", (int(m),))
            md = self.cursor.fetchone()
            if pd and md and not (pd[0] and md[0]):
                couples.append((int(p), int(m)))
        return couples

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
        """
        Valida reglas mínimas de unión:
        - >=18 años
        - Diferencia de edad <= 15
        - Compatibilidad >=70 (placeholder razonable)
        - Evitar genética riesgosa básica (hermanos)
        """
        ea = self._calc_age_from_birth(pa.getBirthDate())
        eb = self._calc_age_from_birth(pb.getBirthDate())
        if ea is None or eb is None:
            return False
        if ea < 18 or eb < 18:
            return False
        if abs(ea - eb) > 15:
            return False

        # Compatibilidad simple (puedes mejorar luego)
        comp = 50
        if (pa.getProvince() or "").strip().lower() == (pb.getProvince() or "").strip().lower():
            comp += 25
        if (pa.getCivilState() or "").lower().startswith("solt") and (pb.getCivilState() or "").lower().startswith("solt"):
            comp += 15
        comp += random.randint(0, 20)
        if comp < 70:
            return False

        # Evitar hermanos: comparten al menos un IdPadre en PadreHijo
        _, _, ph_table = self._tables_by_family(fam)
        self.cursor.execute(f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=?", (int(pa.getId()),))
        padres_a = {r[0] for r in self.cursor.fetchall()}
        self.cursor.execute(f"SELECT IdPadre FROM {ph_table} WHERE IdHijo=?", (int(pb.getId()),))
        padres_b = {r[0] for r in self.cursor.fetchall()}
        if padres_a & padres_b:
            return False

        return True

    def tick_births(self, fam:int, prob_per_couple:float=0.15):
        """
        Con probabilidad por pareja, genera un hijo:
        - ID autogenerado (elige un aleatorio que no choque).
        - Nombre autogenerado, sexo aleatorio.
        - Nucleo: hereda el de la pareja (del padre).
        - Provincia: de uno de los padres.
        """
        person_table, _, ph_table = self._tables_by_family(fam)
        couples = self.list_couples(fam)
        births = 0

        for (padre_id, madre_id) in couples:
            # Carga objetos Persona (ya tienes searchPerson)
            pa = self.searchPerson(padre_id, fam)
            ma = self.searchPerson(madre_id, fam)
            if pa is None or ma is None:
                continue

            # Elegibles para "unirse" (regla del proyecto)
            if not self._are_eligible_to_unite(pa, ma, fam):
                continue

            if random.random() >= prob_per_couple:
                continue

            # Construir persona bebé
            new_id = random.randint(10_000_000, 99_999_999)
            # Verifica que no exista
            self.cursor.execute(f"SELECT 1 FROM {person_table} WHERE ID=?", (int(new_id),))
            if self.cursor.fetchone():
                continue  # intenta luego, evita colisión

            nombres_m = ["Ana","María","Laura","Sofía","Lucía"]
            nombres_h = ["Juan","Carlos","Pedro","José","Diego"]
            genero = random.choice(["Masculino","Femenino"])
            nombre = random.choice(nombres_h if genero.startswith("M") else nombres_m)

            hoy = dt.date.today()
            provincia = random.choice([pa.getProvince(), ma.getProvince()])
            nucleo = pa.getNucleo()  # o decide otra lógica

            bebe = Persona(
                personId=new_id,
                name=nombre,
                lastName1=pa.getLastName1(),
                lastName2=ma.getLastName2(),
                birthDate=hoy,  # actual
                deathDate=None,
                gender=genero,
                province=provincia,
                civilState="Soltero",
                nucleo=nucleo
            )
            # Inserta en Personas{fam}
            if fam == 1:
                self.dataInsertFam1(bebe)
            else:
                self.dataInsertFam2(bebe)

            # Inserta vínculo en PadreHijo{fam} con ambos padres
            self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(padre_id), int(new_id)))
            self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(madre_id), int(new_id)))
            self.conn.commit()
            births += 1

        return births
    
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

    def auto_create_unions_cross(self, prob_attempt: float = 0.40, max_pairs: int = 3) -> int:
        """
        Crea hasta 'max_pairs' parejas entre familias (F1<->F2) según afinidad.
        Marca FechaUnion y TipoUnion='Afinidad Cross'.
        También actualiza EstadoCivil a 'Casado' (ajústalo si prefieres 'Unión libre').
        """
        self._ensure_relaciones_cross()
        singles1 = self._list_eligible_singles_cross(1)
        singles2 = self._list_eligible_singles_cross(2)
        if not singles1 or not singles2:
            return 0

        random.shuffle(singles1)
        random.shuffle(singles2)
        created = 0

        for a, b in zip(singles1, singles2):
            if created >= max_pairs:
                break
            if random.random() > prob_attempt:
                continue
            # Reglas (edad, diferencia, compatibilidad, no hermanos dentro de su propia fam)
            if not self._are_eligible_to_unite(a, b, 1):  # usa PH1 para evitar hermanos (cross no comparte PH)
                continue

            # Evitar duplicado cross (cualquier orden)
            self.cursor.execute(
                """SELECT 1 FROM RelacionesCross
                   WHERE (IdPersonaA=? AND FamA=1 AND IdPersonaB=? AND FamB=2)
                      OR (IdPersonaA=? AND FamA=2 AND IdPersonaB=? AND FamB=1)""",
                (int(a.getId()), int(b.getId()), int(b.getId()), int(a.getId()))
            )
            if self.cursor.fetchone():
                continue

            # Insertar unión cross
            self.cursor.execute(
                "INSERT INTO RelacionesCross (IdPersonaA, FamA, IdPersonaB, FamB, FechaUnion, TipoUnion) VALUES (?, 1, ?, 2, ?, ?)",
                (int(a.getId()), int(b.getId()), datetime.now(), "Afinidad Cross")
            )
            # Cambiar estado civil (opcional)
            self.cursor.execute("UPDATE Personas SET EstadoCivil=? WHERE ID=?", ("Casado", int(a.getId())))
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

    def tick_births_cross(self, prob_per_couple: float = 0.25) -> int:
        """
        Genera nacimientos para parejas CROSS:
        - El bebé nace en la familia del padre (por convención).
        - Se insertan dos vínculos en PadreHijo{fam_bebe}: (padre->hijo) y (madre->hijo).
          (Nota: el ID de la madre es de la otra familia, pero nos sirve para inferir parentescos por ID único de cédula).
        """
        births = 0
        couples = self.list_cross_couples()
        if not couples:
            return births

        for (ida, fama, idb, famb) in couples:
            pa = self.searchPerson(ida, fama)
            pb = self.searchPerson(idb, famb)
            if pa is None or pb is None:
                continue
            # Reglas de elegibilidad (usa fam del padre para chequeo básico de consanguinidad)
            base_fam_for_rules = 1  # indiferente, solo necesita una PH para la verificación de hermanos
            if not self._are_eligible_to_unite(pa, pb, base_fam_for_rules):
                continue
            if random.random() >= prob_per_couple:
                continue

            father_id, father_fam, mother_id, mother_fam = self._assign_roles_cross(pa, pb)
            bebe_fam = father_fam  # convención: bebé nace en la familia del padre
            person_table, _, ph_table = self._tables_by_family(bebe_fam)

            # Generar datos del bebé
            new_id = random.randint(10_000_000, 99_999_999)
            self.cursor.execute(f"SELECT 1 FROM {person_table} WHERE ID=?", (int(new_id),))
            if self.cursor.fetchone():
                continue

            nombres_m = ["Ana","María","Laura","Sofía","Lucía"]
            nombres_h = ["Juan","Carlos","Pedro","José","Diego"]
            genero = random.choice(["Masculino","Femenino"])
            nombre = random.choice(nombres_h if genero.startswith("M") else nombres_m)
            hoy = dt.date.today()

            # Apellidos: 1° del padre, 2° de la madre (estilo CR)
            if father_fam == 1:
                padre = pa
                madre = pb
            else:
                padre = pb
                madre = pa

            last1 = padre.getLastName1()
            last2 = madre.getLastName2()

            provincia = random.choice([pa.getProvince(), pb.getProvince()])
            nucleo = padre.getNucleo()

            bebe = Persona(
                personId=new_id,
                name=nombre,
                lastName1=last1,
                lastName2=last2,
                birthDate=hoy,
                deathDate=None,
                gender=genero,
                province=provincia,
                civilState="Soltero",
                nucleo=nucleo
            )

            # Inserta en la familia del bebé
            if bebe_fam == 1:
                self.dataInsertFam1(bebe)
            else:
                self.dataInsertFam2(bebe)

            # Vincula en PH de la familia del bebé con ambos padres (IDs globales de cédula)
            self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(father_id), int(new_id)))
            self.cursor.execute(f"INSERT INTO {ph_table} (IdPadre, IdHijo) VALUES (?, ?)", (int(mother_id), int(new_id)))
            self.conn.commit()
            births += 1

        return births


conn = DBConnection()