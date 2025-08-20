class Persona:
    def __init__(self, personId, name, lastName1, lastName2, birthDate, deathDate, gender, province, civilState, nucleo):
        self.personId = personId
        self.name = name
        self.lastName1 = lastName1
        self.lastName2 = lastName2
        self.birthDate = birthDate
        self.deathDate = deathDate
        self.gender = gender
        self.province = province
        self.civilState = civilState
        self.nucleo = nucleo

    #Métodos get

    def getId(self):
        return self.personId
    
    def getName(self):
        return self.name
    
    def getLastName1(self):
        return self.lastName1
    
    def getLastName2(self):
        return self.lastName2
    
    def getBirthDate(self):
        return self.birthDate
    
    def getDeathDate(self):
        return self.deathDate
    
    def getGender(self):
        return self.gender
    
    def getProvince(self):
        return self.province
    
    def getCivilState(self):
        return self.civilState
    
    def getNucleo(self):
        return self.nucleo
    
    # Métodos set
    
    def setId(self, newId):
        self.personId = newId
    
    def setName(self, newName):
        self.name = newName

    def setLastName1(self, newLastName1):
        self.lastName1 = newLastName1

    def setLastName2(self, newLastName2):
        self.lastName2 = newLastName2
    
    def setBirthDate(self, newBirthDate):
        self.birthDate = newBirthDate
    
    def setDeathDate(self, newDeathDate):
        self.deathDate = newDeathDate
    
    def setGender(self, newGender):
        self.gender = newGender

    def setProvince(self, newProvince):
        self.province = newProvince
    
    def setCivilState(self, newCivilState):
        self.civilState = newCivilState

    def setNucleo(self, newNucleo):
        self.nucleo = newNucleo