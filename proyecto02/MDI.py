#Para que este programa funcione con la base de datos, se necesita instalar el modulo pyodbc que se usa en el archivo DataBaseConnection.py
#Seguidamente se deberá instalar Access DataBase Engine x64 Redistributable y tener Microsoft Access instalado
#https://www.microsoft.com/en-us/download/details.aspx?id=54920
#para que el calendario funcione se debe instalar el módulo tkcalendar 
from WindowCnfg import *
from tkinter import messagebox
import csv, datetime as dt
from DataBaseConnection import DBConnection
import os


def open_events_screen():
    win = EventsWindow()
    win._refresh_job = None   # id del after

    def refresh():
        # --- Filtros de la UI ---
        fam = None
        fsel = win.cmbFam.get()
        if fsel in ("1", "2"):
            fam = int(fsel)

        tipo = None if win.cmbTipo.get() == "Todos" else win.cmbTipo.get()

        pid = None
        pid_txt = win.txtId.get().strip()
        if pid_txt.isdigit():
            pid = int(pid_txt)

        # --- Leer eventos y poblar tabla ---
        conn = DBConnection()
        try:
            rows = conn.list_events(fam=fam, person_id=pid, tipo=tipo, limit=500)

            # Solo [SIM] si está marcado
            if win.chkSimVar.get():
                rows = [r for r in rows if ("[SIM]" in r["detalle"]) or ("[SIM]" in r["tipo"])]

            # Limpiar tabla
            for item in win.tree.get_children():
                win.tree.delete(item)

            # Insertar filas
            for r in rows:
                nombre = conn.get_person_name(r["id"], r["fam"])
                win.tree.insert(
                    "", "end",
                    values=(str(r["fecha"]), r["tipo"], r["id"], nombre, r["fam"], r["detalle"])
                )
        finally:
            conn.closeConnection()

    def export_csv():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        docs_dir = os.path.join(base_dir, "docs")
        try:
            os.makedirs(docs_dir, exist_ok=True)
        except Exception:
            pass

        path = os.path.join(docs_dir, "eventos_export.csv")

        items = [win.tree.item(i, "values") for i in win.tree.get_children()]
        if not items:
            messagebox.showwarning("Exportar", "No hay datos para exportar.", parent=win)
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Fecha", "Tipo", "Cedula", "Nombre", "Familia", "Detalle"])
            for v in items:
                w.writerow(list(v))

        messagebox.showinfo("Exportar", f"Archivo generado:\n{path}", parent=win)

    # --- AUTO-REFRESH: cada 2s si hay simulación corriendo; 8s si está pausada ---
    def schedule_auto_refresh():
        if getattr(win, "_refresh_job", None):
            try:
                win.after_cancel(win._refresh_job)
            except Exception:
                pass
        refresh()
        interval = 2000 if ('SIM_RUNNING' in globals() and SIM_RUNNING) else 8000
        win._refresh_job = win.after(interval, schedule_auto_refresh)

    def on_close():
        # quitar timer
        if getattr(win, "_refresh_job", None):
            try:
                win.after_cancel(win._refresh_job)
            except Exception:
                pass
            win._refresh_job = None
        # quitar gancho global
        try:
            if 'EVENTS_REFRESH' in globals():
                del globals()['EVENTS_REFRESH']
        except Exception:
            pass
        win.destroy()

    # Botones
    win.btnBuscar.configure(command=refresh)
    win.btnExport.configure(command=export_csv)

    # Gancho global para refresco inmediato desde simulation_tick
    globals()['EVENTS_REFRESH'] = refresh

    # Arrancar ciclo de auto-refresh
    schedule_auto_refresh()

    # Cierre ordenado
    win.protocol("WM_DELETE_WINDOW", on_close)
    win.grab_set()

def simulation_tick(root):
    global _SIM_AFTER_ID, SIM_YEAR
    if not SIM_RUNNING:
        return

    # Fecha simulada = 1 de enero del año SIM
    sim_date = dt.date(SIM_YEAR, 1, 1)

    conn = DBConnection()
    try:
        unions_cross = conn.auto_create_unions_cross(prob_attempt=0.50, max_pairs=4,
                                                     sim_date=sim_date, mark_sim=True)

        total_deaths = 0
        for fam in (1, 2):
            conn.tick_birthdays(fam)  # no persiste edad
            total_deaths += conn.tick_deaths(fam, prob=0.05, sim_date=sim_date)

        births_cross = conn.tick_births_cross(prob_per_couple=0.35, sim_date=sim_date)

        root.winfo_toplevel().title(
            f"Árbol genealógico | Año SIM:{SIM_YEAR}  Cross Unions:{unions_cross}  Cross Births:{births_cross}  Fallec:{total_deaths}"
        )
        if 'EVENTS_REFRESH' in globals():
            globals()['EVENTS_REFRESH']()
    except Exception as e:
        print("Simulación error:", e)
    finally:
        conn.closeConnection()

    # siguiente tick: avanza un año
    SIM_YEAR += 1
    if SIM_RUNNING:
        _SIM_AFTER_ID = root.after(SIM_INTERVAL_MS, lambda: simulation_tick(root))


def start_simulation(root):
    global SIM_RUNNING, _SIM_AFTER_ID, SIM_YEAR
    if SIM_RUNNING:
        return
    # Año inicial: toma el año actual si no está fijado
    if SIM_YEAR is None:
        SIM_YEAR = dt.date.today().year
    SIM_RUNNING = True
    _SIM_AFTER_ID = root.after(1, lambda: simulation_tick(root))
    root.winfo_toplevel().title(f"Árbol genealógico | Simulación iniciada (Año SIM {SIM_YEAR})")


def stop_simulation(root):
    global SIM_RUNNING, _SIM_AFTER_ID
    SIM_RUNNING = False
    if _SIM_AFTER_ID is not None:
        try: root.after_cancel(_SIM_AFTER_ID)
        except Exception: pass
        _SIM_AFTER_ID = None
    root.winfo_toplevel().title("Árbol genealógico | Simulación en pausa")

def run(timeLine):
    try:
        fam = int(timeLine.fam_var.get().strip())
        pid = int(timeLine.id_var.get().strip())
        if fam not in (1, 2): raise ValueError
    except:
        messagebox.showerror("Error", "La familia y/o la persona deben ser numéricas.", parent=timeLine); return
    
    conn = DBConnection()
    try:
        rows = conn.build_person_timeline(pid, fam)
    finally:
        conn.closeConnection()

    if not rows:
        messagebox.showinfo("Línea de tiempo", "Sin eventos para esa persona.", parent=timeLine); return

    # Arma texto con AÑO - Tipo - Detalle
    out = []
    for r in rows:
        f = r["fecha"]
        try:
            y = (f.year if hasattr(f, "year") else dt.datetime.strptime(str(f), "%Y-%m-%d %H:%M:%S").year)
        except:
            y = str(f)
        out.append(f"{y} — {r['tipo']}: {r['detalle']}")
    messagebox.showinfo("Línea de tiempo", "\n".join(out), parent=timeLine)
    timeLine.txtId.delete(0, END)


def showFam2():
    fam2 = VistaPersonasFam1(2)
    fam2.grab_set()


def showFam1():
    fam1 = VistaPersonasFam1(1)
    fam1.grab_set()


def showTimeLine():
    timeLine = TimeLine()
    timeLine.grab_set()
    timeLine.btnWatch.configure(command=lambda: run(timeLine))

def showTree():
    tree = TreeWindow()
    tree.grab_set()

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

        # Inserta vínculo padre-hijo (en PH de la familia seleccionada)
        created = conn.insert_parent_child_PH(parent_id, child_id, fam)
        if not created:
            messagebox.showinfo("Información", "La relación padre/hijo ya existía.", parent=win)
        else:
            # <-- NUEVO: si el hijo ya tiene otro progenitor, crear unión (interna o cross)
            other_parent_id = conn.get_other_parent_for_child(child_id, parent_id, fam)
            if other_parent_id is not None:
                made = conn.ensure_union_if_shared_child(parent_id, other_parent_id, fam)
                if made:
                    messagebox.showinfo("Éxito", "Relación de pareja creada por descendencia.", parent=win)

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

def resetValues():
    answer = messagebox.askyesno("Borrar datos", "¿Está seguro que desea borrar los datos?")
    if answer:
        conn = DBConnection()
        conn.resetAllData()
        conn.closeConnection()
        messagebox.showinfo("Éxito", "Se restablecieron todos los eventos de la familia 1 y 2")

def clear_sim_data(root):
    if messagebox.askyesno("Borrar datos de simulación", "Esto eliminará Nacimientos/Uniones/Defunciones creados durante la simulación. ¿Continuar?"):
        conn = DBConnection()
        try:
            res = conn.reset_sim_changes()
        except AttributeError:
            messagebox.showerror("Error", "No hay datos de simulación para borrar", parent=root)
        finally:
            conn.closeConnection()
        msg = (
            f"Personas borradas: {res['personas_borradas']}\n"
            f"PH borrados: {res['ph_borrados']}\n"
            f"Uniones cross borradas: {res['cross_borradas']}\n"
            f"Fallecimientos revertidos: {res['fallecimientos_revertidos']}\n"
            f"Viudez revertida: {res['viudez_revertida']}\n"
            f"Eventos [SIM] borrados: {res['eventos_borrados']}"
        )
        messagebox.showinfo("Limpieza completada", msg, parent=root)



def mnuHandler():
    screen.mnuArchivo.add_command(label="Añadir a Familia 1", underline=0, command=newPerson)
    screen.mnuArchivo.add_command(label="Añadir a Familia 2", underline=0, command=newPersonFam2)
    screen.mnuArchivo.add_separator()
    screen.mnuArchivo.add_command(label="Anexar Padres Familia 1", command=addParentsFam1)
    screen.mnuArchivo.add_command(label="Anexar Padres Familia 2", command=addParentsFam2)
    screen.mnuArchivo.add_separator()
    screen.mnuArchivo.add_command(label="Reiniciar", underline=0, command=resetValues)
    screen.mnuArchivo.add_command(label="Salir", command=screen.quit)

    screen.mnuVer.add_command(label="Ver Familia 1", underline=0, command=showFam1)
    screen.mnuVer.add_command(label="Ver Familia 2", underline=0, command=showFam2)
    screen.mnuVer.add_separator()
    screen.mnuVer.add_command(label="Ver Linea de Tiempo", underline=0, command=showTimeLine)
    screen.mnuVer.add_separator()
    screen.mnuVer.add_command(label="Ver Árbol Genealógico", underline=0, command=showTree)

    screen.mnuSimulacion.add_command(label="Iniciar", underline=0, command= lambda: start_simulation(screen))
    screen.mnuSimulacion.add_separator()
    screen.mnuSimulacion.add_command(label="Detener", underline=0, command= lambda: stop_simulation(screen))
    screen.mnuSimulacion.add_separator()
    screen.mnuSimulacion.add_command(label="Borrar Datos Simulacion", underline=0, command= lambda: clear_sim_data(screen))
    screen.mnuSimulacion.add_separator()
    screen.mnuSimulacion.add_command(label="Historial (en vivo)", underline=0, command=open_events_screen)

    screen.mnuBuscar.add_command(label="Buscar", underline=0, command=showSearch)


if __name__ == "__main__":
    SIM_INTERVAL_MS = 10_000  # 10 segundos
    SIM_RUNNING = False
    _SIM_AFTER_ID = None
    SIM_YEAR = None
    screen = PrincipalWindow()
    mnuHandler()
    screen.after(SIM_INTERVAL_MS, lambda: simulation_tick(screen))
    mainloop()