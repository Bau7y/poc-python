from tkinter import *
from tkinter import ttk
from tkinter.font import *
from DataBaseConnection import *
from tkcalendar import DateEntry
import tkinter as tk
import math
from tkinter import messagebox


class PrincipalWindow(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.windowCnfg()
        self.createObjs()


    def windowCnfg(self):
        self["bg"] = "#000000"
        self.state("zoomed")
        self.title("Árbol genealógico")
        self.resizable(False, False)

    def createObjs(self):
        self.barraMnu = Menu(self, bg="#000000", fg="#ffffff")
        self.mnuArchivo = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.mnuVer = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.mnuBuscar = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.mnuSimulacion = Menu(self.barraMnu, tearoff=0, bg="#000000", fg="#ffffff")
        self.barraMnu.add_cascade(label="Archivo", menu=self.mnuArchivo, underline=0)
        self.barraMnu.add_cascade(label="Ver", menu=self.mnuVer, underline=0)
        self.barraMnu.add_cascade(label="Buscar", menu=self.mnuBuscar, underline=0)
        self.barraMnu.add_cascade(label="Simulación", menu=self.mnuSimulacion, underline=0)
        self.configure(menu=self.barraMnu)


class NewPersonWindow(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.personWindowCnfg()
        self.createObjs()
        self.placeObjs()

    def personWindowCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Nueva persona")

    def createObjs(self):
        genderList = ["Masculino", "Femenino", "Otro"]
        civilStateList = ["Soltero", "Casado", "Divorciado", "Viudo", "Union libre"]
        provinceList = ["Alajuela", "Heredia", "Cartago", "Limón", "San José", "Guanacaste", "Puntarenas"]
        self.nucleos = ["0", "1", "2", "3", "4"]
        self.lblName = Label(self, text="Nombre", bg="#FFFFFF", font=("Arial", 12))
        self.lblLastName = Label(self, text="Apellido", bg="#FFFFFF", font=("Arial", 12))
        self.lblLastName2 = Label(self, text="Segundo apellido", bg="#FFFFFF", font=("Arial", 12))
        self.lblId = Label(self, text="Cédula", bg="#FFFFFF", font=("Arial", 12))
        self.lblBirthDate = Label(self, text="Fecha de nacimiento", bg="#FFFFFF", font=("Arial", 12))
        self.lblDeathDate = Label(self, text="Fecha de fallecimiento", bg="#FFFFFF", font=("Arial", 12))
        self.lblGender = Label(self, text="Género", bg="#FFFFFF", font=("Arial", 12))
        self.lblProvince = Label(self, text="Provincia", bg="#FFFFFF", font=("Arial", 12))
        self.lblCivilState = Label(self, text="Estado civil", bg="#FFFFFF", font=("Arial", 12), fg="#000000")
        self.lblNucleo = Label(self, text="Núcleo Familiar", bg="#FFFFFF", font=("Arial", 12))

        self.txtName = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtLastName = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtLastName2 = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtId = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtDeathDate = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.calBirthDate = DateEntry(self, width=27, background='darkblue', foreground='white', borderwidth=2, selectmode="day", date_pattern="dd/mm/yyyy")
        self.cmbxGender = ttk.Combobox(self, state="readonly", values=genderList, width=27)
        self.cmbxProvince = ttk.Combobox(self, state="readonly", values=provinceList, width=27)
        self.cmbxCivilState = ttk.Combobox(self, state="readonly", values=civilStateList, width=27)
        self.cmbxNucleo = ttk.Combobox(self, state="readonly", values=self.nucleos, width=27)
        self.cmbxGender.set("...")
        self.cmbxProvince.set("...")
        self.cmbxCivilState.set("Soltero")
        self.txtId.insert(0, "0")
        self.txtLastName.insert(0, "...")
        self.txtLastName2.insert(0, "...")
        self.txtName.insert(0, "...")
        self.cmbxNucleo.set("0")

        self.btnSave = Button(self, text="Guardar", font=("Arial", 12))

    def placeObjs(self):
        self.lblName.place(x=50, y=50)
        self.lblLastName.place(x=50, y=100)
        self.lblLastName2.place(x=50, y=150)
        self.lblId.place(x=50, y=200)
        self.lblBirthDate.place(x=50, y=250)
        self.lblDeathDate.place(x=50, y=300)
        self.lblGender.place(x=50, y=350)
        self.lblProvince.place(x=50, y=400)
        self.lblCivilState.place(x=50, y=450)
        self.lblNucleo.place(x=50, y=500)

        self.txtName.place(x=250, y=50)
        self.txtLastName.place(x=250, y=100)
        self.txtLastName2.place(x=250, y=150)
        self.txtId.place(x=250, y=200)
        self.calBirthDate.place(x=250, y=250)
        self.txtDeathDate.place(x=250, y=300)
        self.cmbxGender.place(x=250, y=350)
        self.cmbxProvince.place(x=250, y=400)
        self.cmbxCivilState.place(x=250, y=450)
        self.cmbxNucleo.place(x=250, y=500)

        self.btnSave.place(x=250, y=550)

class VistaPersonasFam1(Toplevel):
    def __init__(self, fam, master = None):
        super().__init__(master)
        self.idFam = fam
        self.vistaPersonasCnfg()
        self.createObjs()
        self.placeObjs()
    
    def vistaPersonasCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("1100x500")
        self.title("Vista personas")
        self.focus_set()

    def createObjs(self):
        rowTitles = ("Cédula", "Nombre", "Apellido", "Segundo Apellido", "Fecha de nacimiento", "Fecha de fallecimiento", "Género", "Provincia", "Estado civil", "Nucleo Familiar")
        self.table = ttk.Treeview(self, columns=rowTitles, show="headings")
        self.table["columns"] = rowTitles
        self.table.column("Cédula", anchor=CENTER, width=100)
        self.table.column("Nombre", anchor=CENTER, width=100)
        self.table.column("Apellido", anchor=CENTER, width=100)
        self.table.column("Segundo Apellido", anchor=CENTER, width=100)
        self.table.column("Fecha de nacimiento", anchor=CENTER, width=100)
        self.table.column("Fecha de fallecimiento", anchor=CENTER, width=100)
        self.table.column("Género", anchor=CENTER, width=100)
        self.table.column("Provincia", anchor=CENTER, width=100)
        self.table.column("Estado civil", anchor=CENTER, width=100)
        self.table.column("Nucleo Familiar", anchor=CENTER, width=100)

        self.table.heading("Cédula", text="Cédula", anchor=CENTER)
        self.table.heading("Nombre", text="Nombre", anchor=CENTER)
        self.table.heading("Apellido", text="Apellido", anchor=CENTER)
        self.table.heading("Segundo Apellido", text="Segundo Apellido", anchor=CENTER)
        self.table.heading("Fecha de nacimiento", text="Fecha de nacimiento", anchor=CENTER)
        self.table.heading("Fecha de fallecimiento", text="Fecha de fallecimiento", anchor=CENTER)
        self.table.heading("Género", text="Género", anchor=CENTER)
        self.table.heading("Provincia", text="Provincia", anchor=CENTER)
        self.table.heading("Estado civil", text="Estado civil", anchor=CENTER)
        self.table.heading("Nucleo Familiar", text="Nucleo Familiar", anchor=CENTER)

        conn = DBConnection()
        if self.idFam == 1:
            listaPersonasFam = conn.getDataP1()
        else:
            listaPersonasFam = conn.getDataPer2()
        conn.closeConnection()

        for persona in listaPersonasFam:
            self.table.insert("", END, values=(persona.getId(), persona.getName(), persona.getLastName1(), persona.getLastName2(), persona.getBirthDate(), persona.getDeathDate(), persona.getGender(), persona.getProvince(), persona.getCivilState(), persona.getNucleo()))

    def placeObjs(self):
        self.table.place(x=50, y=50)
        

class Search(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.searchCnfg()
        self.createObjs()
        self.placeObjs()

    def searchCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("300x300+10+10")
        self.title("Buscar persona")
        self.focus_set()

    def createObjs(self):
        self.choice = IntVar()
        self.radFamChoice = tk.Radiobutton(self, text="Familia 1", variable=self.choice, value=1)
        self.radFamChoice2 = tk.Radiobutton(self, text="Familia 2", variable=self.choice, value=2)

        self.btnSelected = Button(self, text="Seleccionar", font=("Arial", 12))
        

    
    def placeObjs(self):
        self.radFamChoice.place(x=50, y=50)
        self.radFamChoice2.place(x=150, y=50)

        self.btnSelected.place(x=90, y=150)

class AfterSearch(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.afterSearchCnfg()
        self.createObjs()
        self.placeObjs()

    
    def afterSearchCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Datos de Familia")
        self.focus_set()

    def createObjs(self):
        questions = ("¿Cuál es la relación entre persona A y persona B?", "¿Quiénes son los primos de primer grado de X?", 
                     "¿Cuáles son todos los antepasados maternos de X?", "¿Cuáles descendientes de X están vivos actualmente?",
                     "¿Cuántas personas nacieron en los últimos 10 años?", "¿Cuáles parejas actuales tienen 2 o más hijos en común?",
                     "¿Cuántas personas fallecieron antes de cumplir 50 años?")
        self.lblReqId = Label(self, text="Ingrese la cédula de las personas:", bg="#FFFFFF", font=("Arial", 12))

        self.txtReqId = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtReqId2 = Entry(self, bg="#FFFFFF", font=("Arial", 12))

        self.btnSearch = Button(self, text="Buscar", font=("Arial", 12))
        self.btnAccept = Button(self, text="Aceptar", font=("Arial", 12))

        self.cmbxOptions = ttk.Combobox(self, state="readonly", values=questions, width=50)

    
    def placeObjs(self):
        self.cmbxOptions.place(x=50, y=50)
        self.btnAccept.place(x=400, y=50)


class FatherSonWindow(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.fatherSonCnfg()
        self.createObjs()
        self.placeObjs()

    def fatherSonCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Padre e hijo")
        self.focus_set()

    def createObjs(self):
        self.lblIdFather = Label(self, text="Cédula del padre", bg="#FFFFFF", font=("Arial", 12))
        self.lblIdSon = Label(self, text="Cédula del hijo", bg="#FFFFFF", font=("Arial", 12))
        self.txtIdFather = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.txtIdSon = Entry(self, bg="#FFFFFF", font=("Arial", 12))
        self.btnAccept = Button(self, text="Aceptar", font=("Arial", 12))

    def placeObjs(self):
        self.lblIdFather.place(x=50, y=50)
        self.lblIdSon.place(x=50, y=100)
        self.txtIdFather.place(x=250, y=50)
        self.txtIdSon.place(x=250, y=100)
        self.btnAccept.place(x=250, y=150)


class TimeLine(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.timelineCnfg()
        self.createObjs()
        self.placeObjs()

    def timelineCnfg(self):
        self["bg"] = "#FFFFFF"
        self.resizable(False, False)
        self.geometry("600x600")
        self.title("Línea de tiempo")
        self.focus_set()


    def createObjs(self):
        self.lblChoice = Label(self, text="Familia (1 o 2):", bg="#FFFFFF", font=("Arial", 12))
        self.fam_var = StringVar()
        self.txtChoice = Entry(self, bg="#FFFFFF", font=("Arial", 12), textvariable=self.fam_var, width=8)
        self.lblId = Label(self, text="Cédula:", bg="#FFFFFF", font=("Arial", 12))
        self.id_var = StringVar()
        self.txtId = Entry(self, bg="#FFFFFF", font=("Arial", 12), textvariable=self.id_var, width=12)
        self.btnWatch = Button(self, text="Ver", font=("Arial", 12))
        self.btnClose = Button(self, text="Cerrar", font=("Arial", 12), command=self.destroy)


    
    def placeObjs(self):
        self.lblChoice.place(x=50, y=50)
        self.txtChoice.place(x=150, y=50)
        self.lblId.place(x=50, y=100)
        self.txtId.place(x=150, y=100)
        self.btnWatch.place(x=50, y=150)
        self.btnClose.place(x=150, y=150)


class TreeWindow(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Árbol genealógico")
        self.geometry("1200x800")
        self.configure(bg="#101014")

        # ---- Panel de controles
        ctrl = tk.Frame(self, bg="#101014")
        ctrl.pack(side="top", fill="x")
        tk.Label(ctrl, text="Familia:", fg="#fff", bg="#101014").pack(side="left", padx=6)
        self.cmbFam = ttk.Combobox(ctrl, values=["1","2"], width=4, state="readonly"); self.cmbFam.current(0)
        self.cmbFam.pack(side="left")

        tk.Label(ctrl, text="Cédula raíz:", fg="#fff", bg="#101014").pack(side="left", padx=6)
        self.txtId = ttk.Entry(ctrl, width=12); self.txtId.pack(side="left")

        tk.Label(ctrl, text="Modo:", fg="#fff", bg="#101014").pack(side="left", padx=6)
        self.cmbModo = ttk.Combobox(ctrl, values=["Ancestros","Descendientes","Ambos"], width=14, state="readonly"); self.cmbModo.current(2)
        self.cmbModo.pack(side="left")

        tk.Label(ctrl, text="Profundidad:", fg="#fff", bg="#101014").pack(side="left", padx=6)
        self.spDepth = ttk.Spinbox(ctrl, from_=1, to=8, width=4); self.spDepth.set(4); self.spDepth.pack(side="left")

        self.btnDraw = ttk.Button(ctrl, text="Dibujar", command=self.draw_tree)
        self.btnDraw.pack(side="left", padx=10)

        self.btnCenter = ttk.Button(ctrl, text="Centrar", command=lambda: self._center())
        self.btnCenter.pack(side="left")

        # ---- Canvas con scroll
        wrap = tk.Frame(self, bg="#101014"); wrap.pack(side="top", fill="both", expand=True)
        self.canvas = tk.Canvas(wrap, bg="#0c0c12", highlightthickness=0, scrollregion=(0,0,4000,4000))
        self.canvas.pack(side="left", fill="both", expand=True)
        self.hbar = ttk.Scrollbar(wrap, orient="horizontal", command=self.canvas.xview)
        self.hbar.pack(side="bottom", fill="x")
        self.vbar = ttk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.vbar.pack(side="right", fill="y")
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        # zoom/pan
        self.scale = 1.0
        self.canvas.bind("<MouseWheel>", self._on_wheel)         # Windows
        self.canvas.bind("<Button-4>", self._on_wheel)           # Linux
        self.canvas.bind("<Button-5>", self._on_wheel)           # Linux
        self.canvas.bind("<ButtonPress-2>", self._start_pan)
        self.canvas.bind("<B2-Motion>", self._do_pan)
        self._pan_start = None

        # cache de nodos
        self._nodes = {}  # (id,fam) -> (x,y)

    # --------- interacción ----------
    def _on_wheel(self, e):
        delta = 1 if getattr(e, "delta", 0) > 0 or getattr(e, "num", 0) == 4 else -1
        factor = 1.1 if delta > 0 else 0.9
        self.scale *= factor
        self.canvas.scale("all", self.canvas.canvasx(e.x), self.canvas.canvasy(e.y), factor, factor)

    def _start_pan(self, e):
        self._pan_start = (e.x, e.y)

    def _do_pan(self, e):
        if not self._pan_start: return
        dx = self._pan_start[0] - e.x
        dy = self._pan_start[1] - e.y
        self._pan_start = (e.x, e.y)
        self.canvas.xview_scroll(int(dx/2), "units")
        self.canvas.yview_scroll(int(dy/2), "units")

    def _center(self):
        # centra en (2000,2000)
        self.canvas.xview_moveto(0.5)
        self.canvas.yview_moveto(0.5)

    # --------- dibujo ----------
    def draw_tree(self):
        # limpiar
        self.canvas.delete("all")
        self._nodes.clear()
        try:
            fam = int(self.cmbFam.get()); pid = int(self.txtId.get())
            depth = int(self.spDepth.get())
        except:
            messagebox.showerror("Error", "Ingrese familia (1/2), cédula y profundidad válidos.", parent=self); return

        modo = self.cmbModo.get()
        conn = DBConnection()
        try:
            # obtener capas por niveles
            levels = self._build_levels(conn, pid, fam, depth, modo)
        finally:
            conn.closeConnection()

        # layout simple por capas
        cx, cy = 2000, 2000
        h_gap, v_gap = 200, 140
        start_row = cy - (len(levels)-1)*v_gap/2
        for i, layer in enumerate(levels):
            y = start_row + i*v_gap
            if not layer: continue
            width = (len(layer)-1)*h_gap
            x0 = cx - width/2
            for j, node in enumerate(layer):
                x = x0 + j*h_gap
                self._draw_node(node, x, y)

        # aristas después de colocar nodos
        conn = DBConnection()
        try:
            self._draw_edges(conn)
        finally:
            conn.closeConnection()

        self._center()

    def _draw_node(self, node, x, y):
        pid, fam, name, dead = node
        self._nodes[(pid,fam)] = (x,y)
        r = 26
        fill = "#1976D2" if fam == 1 else "#2E7D32"
        outline = "#E0E0E0"
        if dead: fill = "#616161"
        tag = f"node_{pid}_{fam}"
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=2, tags=(tag,))
        label = f"{pid}\nF{fam}"
        self.canvas.create_text(x, y+42, text=label, fill="#ddd", font=("Segoe UI", 9), tags=(tag,))
        self.canvas.create_text(x, y-40, text=name[:14], fill="#fff", font=("Segoe UI", 9, "bold"), tags=(tag,))

        # Doble click: convertir este nodo en nueva raíz y redibujar
        def on_dbl(_e, _pid=pid, _fam=fam):
            try:
                self.cmbFam.set(str(_fam))
                self.txtId.delete(0, tk.END)
                self.txtId.insert(0, str(_pid))
                self.draw_tree()
            except Exception as ex:
                messagebox.showerror("Árbol", f"No se pudo recentrar: {ex}", parent=self)
        self.canvas.tag_bind(tag, "<Double-1>", on_dbl)

    def _draw_edges(self, conn: DBConnection):
        # Conecta padre -> hijo con líneas; une cónyuges con línea horizontal
        # Hijos: usar PH1 y PH2
        for fam_ph in (1,2):
            _, _, ph = conn._tables_by_family(fam_ph)
            conn.cursor.execute(f"SELECT IdPadre, IdHijo FROM {ph}")
            for (p, h) in conn.cursor.fetchall():
                # padre puede ser de F1 o F2; el hijo vive en fam_ph
                for fam_p in (1,2):
                    if (p, fam_p) in self._nodes and (h, fam_ph) in self._nodes:
                        x1,y1 = self._nodes[(p,fam_p)]
                        x2,y2 = self._nodes[(h,fam_ph)]
                        self._edge(x1,y1, x2,y2, arrow=True)
                        break

        # Cónyuges internos
        for fam in (1,2):
            _, rel, _ = conn._tables_by_family(fam)
            conn.cursor.execute(f"SELECT IdPadre, IdMadre FROM {rel}")
            for (pa, ma) in conn.cursor.fetchall():
                if (pa,fam) in self._nodes and (ma,fam) in self._nodes:
                    x1,y1 = self._nodes[(pa,fam)]
                    x2,y2 = self._nodes[(ma,fam)]
                    self._spouse_edge(x1,y1, x2,y2)

        # Cónyuges cross
        if conn._table_exists("RelacionesCross"):
            conn.cursor.execute("SELECT IdPersonaA, FamA, IdPersonaB, FamB FROM RelacionesCross")
            for (ida,fama, idb,famb) in conn.cursor.fetchall():
                if (ida,fama) in self._nodes and (idb,famb) in self._nodes:
                    x1,y1 = self._nodes[(ida,fama)]
                    x2,y2 = self._nodes[(idb,famb)]
                    self._spouse_edge(x1,y1, x2,y2)

    def _edge(self, x1,y1, x2,y2, arrow=False):
        midy = (y1+y2)/2
        self.canvas.create_line(x1, y1+26, x1, midy, x2, midy, x2, y2-26, smooth=True, fill="#BDBDBD", width=2, arrow=tk.LAST if arrow else tk.NONE)

    def _spouse_edge(self, x1,y1, x2,y2):
        self.canvas.create_line(x1, y1, x2, y2, fill="#FFC107", width=2)

    # --------- cálculo de niveles ----------
    def _build_levels(self, conn: DBConnection, pid:int, fam:int, depth:int, modo:str):
        """
        Devuelve lista de capas [[(pid,fam,name,dead), ...], ...]
        Ancestros: raíz en último nivel | Descendientes: raíz en primer nivel | Ambos: raíz centrada
        """
        # utilidades
        def basic(p,f):
            person_table, _, _ = conn._tables_by_family(f)
            conn.cursor.execute(f"SELECT Nombre, Apellido, Apellido2, FechaFallecimiento FROM {person_table} WHERE ID=?", (int(p),))
            r = conn.cursor.fetchone()
            if not r: return (str(p), False)
            name = f"{(r[0] or '').strip()} {(r[1] or '').strip()}".strip()
            dead = r[3] is not None
            return (name if name else str(p), dead)

        # Colecciones
        root_name, root_dead = basic(pid, fam)

        if modo == "Ancestros":
            # nivel 0: ancestros más lejanos, nivel N: raíz
            levels = [[] for _ in range(depth+1)]
            # raiz
            levels[-1].append((pid, fam, root_name, root_dead))
            # subir
            cur_level = [(pid, fam)]
            for step in range(depth):
                parents = []
                for (cid, cfam) in cur_level:
                    for (ppid, pfam) in conn._parents_of(cid, cfam):
                        if (ppid, pfam) not in parents:
                            parents.append((ppid, pfam))
                if not parents: break
                for (ppid, pfam) in parents:
                    n, d = basic(ppid, pfam)
                    levels[-2-step].append((ppid, pfam, n, d))
                cur_level = parents
            return [lv for lv in levels if lv]

        if modo == "Descendientes":
            # nivel 0: raíz, luego hijos, etc.
            levels = [[(pid, fam, root_name, root_dead)]]
            cur_level = [(pid, fam)]
            for step in range(depth):
                kids = []
                for (pp, pf) in cur_level:
                    for fam_ph in (1,2):
                        try:
                            for hid in conn._children_of(pp, fam_ph):
                                if (hid, fam_ph) not in kids:
                                    kids.append((hid, fam_ph))
                        except TypeError:
                            # por si la firma en tu _children_of no acepta fam_ph: usar la que tengas
                            pass
                if not kids: break
                layer = []
                for (hid, hf) in kids:
                    n, d = basic(hid, hf)
                    layer.append((hid, hf, n, d))
                levels.append(layer)
                cur_level = kids
            return levels

        # Ambos: ancestros arriba y descendientes abajo
        up = TreeWindow._compute_ancestors(conn, pid, fam, depth, basic)
        down = TreeWindow._compute_descendants(conn, pid, fam, depth, basic)
        # unir: up (sin raiz duplicada) + [root] + down (sin raiz duplicada)
        final = []
        final.extend(up)
        final.append([(pid, fam, root_name, root_dead)])
        final.extend(down)
        return final

    @staticmethod
    def _compute_ancestors(conn, pid, fam, depth, basic_fn):
        levels = []
        cur = [(pid, fam)]
        for step in range(depth):
            parents = []
            for (cid, cfam) in cur:
                for (ppid, pfam) in conn._parents_of(cid, cfam):
                    if (ppid, pfam) not in parents:
                        parents.append((ppid, pfam))
            if not parents: break
            layer = []
            for (ppid, pfam) in parents:
                n, d = basic_fn(ppid, pfam)
                layer.append((ppid, pfam, n, d))
            levels.insert(0, layer)  # ancestros “arriba”
            cur = parents
        return levels

    @staticmethod
    def _compute_descendants(conn, pid, fam, depth, basic_fn):
        levels = []
        cur = [(pid, fam)]
        for step in range(depth):
            kids = []
            for (pp, pf) in cur:
                for fam_ph in (1,2):
                    try:
                        for hid in conn._children_of(pp, fam_ph):
                            if (hid, fam_ph) not in kids:
                                kids.append((hid, fam_ph))
                    except TypeError:
                        pass
            if not kids: break
            layer = []
            for (hid, hf) in kids:
                n, d = basic_fn(hid, hf)
                layer.append((hid, hf, n, d))
            levels.append(layer)  # descendientes “abajo”
            cur = kids
        return levels