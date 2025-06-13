import re

def reqProvince(provinces):
    provinces = {
        "1": "San José",
        "2": "Alajuela",
        "3": "Cartago",
        "4": "Heredia",
        "5": "Guanacaste",
        "6": "Puntarenas",
        "7": "Limón"
    }
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


def userReg():
    user = {
        "cedula": reqId(),
        "nombre": input("Nombre: "),
        "genero": reqGender(),
        "fechaNacimiento": reqBirthDate(),
        "provincia": reqProvince()
    }
    return user;


def reqUserOpt():
    print("1. Registro de personas y esquema de vacunación\n2. Reportes\n3. Salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Solo se permiten numeros enteros...")


def menuHandler():
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                userReg()
            case 2:
                pass
            case 3:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...\n")

if __name__ == "__main__":
    menuHandler()