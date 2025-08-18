class Persona:
    def __init__(self, personId, name, birthDate, deathDate, gender, province, civilState):
        self.personId = personId
        self.name = name
        self.birthDate = birthDate
        self.deathDate = deathDate
        self.gender = gender
        self.province = province
        self.civilState = civilState

    #Métodos get

    def getId(self):
        return self.personId
    
    def getName(self):
        return self.name
    
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
    
    # Métodos set
    
    def setId(self, newId):
        self.personId = newId
    
    def setName(self, newName):
        self.name = newName
    
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