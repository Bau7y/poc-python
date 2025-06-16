def reqName():
    name = input("Ingrese su nombre: ").replace(" ", "")
    return name;

def reqId():
    cedula = input("Ingrese su cédula: ").replace(" ", "")
    return cedula;


def reqUsers():
    listaUsers = []
    while(len(listaUsers) < 3):
        users = {
            "nombre": reqName(),
            "cedula": reqId()
        }
        if users["cedula"] not in [user["cedula"] for user in listaUsers]:
            print("Usuario registrado...\n")
            listaUsers.append(users)
        else:
            print("Usuario ya registrado...\n")
            continue
    return listaUsers;


def main():
    users = reqUsers()
    print(users)


if __name__ == "__main__":
    main()