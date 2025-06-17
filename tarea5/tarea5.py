
def divisas(dicMonType):
    inputMonType = input("Digite el tipo de moneda: ").upper()
    for key, value in dicMonType.items():
        if inputMonType == key.upper():
            print(value)
        else:
            print("No se ha encontrado el tipo de moneda digitado...")


def evenAges(ages):
    for name, age in ages.items():
        if age % 2 == 0:
            print(f"{name} tiene {age} años y es par")


def reqAges():
    dicPeople = {}
    for i in range(0, int(input("Digite la cantidad de personas que desea registrar: "))):
        dicPeople[input("Digite el nombre de la persona: ")] = int(input("Digite la edad de la persona: "))
        print("\n")
    evenAges(dicPeople)


def reporte(sucursales):
    dicReportes = {}
    listaClientes = []
    for sucursal in sucursales:
        dicReportes["ganancias_netas"] = sucursal["ventas"] - sucursal["gastos"] + dicReportes.get("ganancias_netas", 0)
        dicReportes["horas_trabajadas"] = sucursal["horas"] + dicReportes.get("horas_trabajadas", 0)
        listaClientes.append(sucursal["clientes"])
        listaClientes.sort(reverse=True)
        dicReportes["top_clientes"] = sucursal["nombre"] if sucursal["clientes"] == listaClientes[0] else dicReportes.get("top_clientes", "N/A")
        dicReportes["menos_cliente"] = sucursal["nombre"] if sucursal["clientes"] == listaClientes[-1] else dicReportes.get("menos_cliente", "N/A")
    return dicReportes;


def reqUserOpt():
    print("1.Reporte\n2.Personas\n3.Divisas\n4.Salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Debe digitar una de las opciones...")


def menuHandler():
    sucursales = [{"nombre":"San José", "ventas":105, "clientes":30, "horas":90, "gastos":20},
              {"nombre":"Cartago", "ventas":130, "clientes":73, "horas":60, "gastos":18},
              {"nombre":"Heredia", "ventas":150, "clientes":45, "horas":85, "gastos":34},
              {"nombre":"Alajuela", "ventas":180, "clientes":18, "horas":45, "gastos":15},
              {"nombre":"Puntarenas", "ventas":95, "clientes":26, "horas":65, "gastos":41},
              {"nombre":"Guanacaste", "ventas":122, "clientes":20, "horas":18, "gastos":23},
              {"nombre":"Limon", "ventas":125, "clientes":89, "horas":38, "gastos":16}]
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                print(reporte(sucursales))
            case 2:
                reqAges()
            case 3:
                divisas({'Euro':'€', 'Dollar':'$', 'Yen':'¥'})
            case 4:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...")

if __name__ == "__main__":
    menuHandler()