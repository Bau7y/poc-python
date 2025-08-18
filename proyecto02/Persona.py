class Persona:
    def __init__(self, personId, name):
        self.personId = personId
        self.name = name

    def getId(self):
        return self.personId
    
    def setId(self, newId):
        self.personId = newId

    def getName(self):
        return self.name
    
    def setName(self, newName):
        self.name = newName