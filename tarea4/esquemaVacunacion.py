import re
def reqScndUseropt():
    print("1.Mostrar el porcentaje de personas por provincia que han registrado su información de vacunación.\n2.Mostrar la cantidad de personas por género que han registrado su información de vacunación\n3.Mostrar el porcentaje de personas que han registrado su información de vacunación(Por rangos de edad)\n4.Mostrar la cantidad de personas que han registrado su información de vacunación por provincia, por género y por un tipo de vacuna\n5.Mostrar únicamente la lista de personas con las dos dosis de vacunación, de acuerdo con un rango de fechas\n6.Salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Debe digitar una de las opciones que se muestran en pantalla...")

def secondMnuHandler():
    while(True):
        userOpt = reqScndUseropt()
        match userOpt:
            case 1:
                print("1")
            case 2:
                print("2")
            case 3:
                print("3")
            case 4:
                print("4")
            case 5:
                print("5")
            case 6:
                print("Saliendo...")
                break
            case _:
                print("Debe digitar una de las opciones que se muestran en pantalla...")

def reqDosisDate(dosisQuantity):
    dosisDate = []
    for i in range(dosisQuantity):
        while(True):
            date = input(f"Fecha de la dosis {i + 1} (dd/mm/yyyy): ")
            if re.match("^\d{1,2}/\d{1,2}/\d{2,4}$", date):
                if re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{2, 4})$", date):
                    if date in dosisDate:
                        print("Fecha de la dosis ya registrada...")
                        continue
                    else:
                        dosisDate.append(date)
                        break
                print("Fecha de la dosis no válida...")
    return dosisDate


def reqDosisQuantity():
    dosisQuantity = 0
    while(dosisQuantity < 1 or dosisQuantity > 2):
        dosisQuantity = int(input("Cantidad de dosis (1, 2): "))
    return dosisQuantity;

def reqVaccineInfo(usersList, vaccines):
    while(True):
        for key, value in vaccines.items():
            print(f"{key}. {value}")
        try:
            vaccine = int(input("Vacuna: "))
            if vaccine >= 1 and vaccine <= 5:
                usersList[len(usersList) - 1]["vacuna"] = vaccines[str(vaccine)]
                usersList[len(usersList) - 1]["cantidad dosis"] = reqDosisQuantity()
                usersList[len(usersList) -1]["fecha(s) dosis"] = reqDosisDate(usersList[len(usersList) - 1]["cantidad dosis"])
                print("Usuario registrado...\n")
                return usersList;
        except:
            print("Debe digitar una de las opciones que se muestran en pantalla...")

def reqProvince(provinces):
    while(True):
        for key, value in provinces.items():
            print(f"{key}. {value}")
        try:
            province = int(input("Provincia: "))
            if province >= 1 and province <= 7:
                return provinces[str(province)]
        except:
            print("Debe digitar una de las opciones que se muestran en pantalla...")


def reqBirthDate():
    while(True):
        birthDate = input("Fecha de nacimiento (dd/mm/yyyy): ")
        if re.match("^\d{1,2}/\d{1,2}/\d{2,4}$", birthDate):
            if re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{2,4})$", birthDate):
                return birthDate;
        print("Fecha de nacimiento no válida...")


def reqGender():
    while(True):
        gender = input("Género (M/F): ").upper()
        if gender == "M" or gender == "F":
            return gender;
        print("Género no válido...")


def reqId():
    while(True):
        cedula = input("Cédula: ").replace("-", "").replace(" ", "")
        if re.match("^\d{9,11}$", cedula):
            return cedula;
        print("Cédula no válida...")


def userReg(provinces):
    user = {
        "cedula": reqId(),
        "nombre": input("Nombre: ").upper(),
        "genero": reqGender(),
        "fechaNacimiento": reqBirthDate(),
        "provincia": reqProvince(provinces)
    }
    return user;


def reqUserOpt():
    print("1. Registro de personas y esquema de vacunación\n2. Reportes\n3. Salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Solo se permiten numeros enteros...")


def menuHandler():
    users = []
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                users.append(userReg({"1": "San José", "2": "Alajuela", "3": "Cartago", "4": "Heredia", "5": "Guanacaste", "6": "Puntarenas", "7": "Limón"}))
                reqVaccineInfo(users, {"1": "AstraZeneca", "2": "Pfizer", "3": "Janssen", "4": "SINOVAC", "5": "Sputnik V"})
                print(users)
            case 2:
                secondMnuHandler()
            case 3:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...\n")

if __name__ == "__main__":
    menuHandler()