def reqName():
    name = input("Ingrese su nombre: ").replace(" ", "")
    return name;

def reqId():
    cedula = input("Ingrese su cédula: ").replace(" ", "")
    return cedula;


def reqUsers():
    listaUsers = []
    for i in range(3):
        users = {
            "nombre": reqName(),
            "cedula": reqId()
        }
        listaUsers.append(users)
    return listaUsers;


def main():
    users = reqUsers()
    print(users)
    

if __name__ == "__main__":
    main()