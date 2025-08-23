#
class Uniones:
    def __init__(self, date, civilSt):
        self.date = date
        self.civilSt = civilSt

    def setDate(self, newDate):
        self.date = newDate

    def setCivilSt(self, newCivilSt):
        self.civilSt = newCivilSt

    def getDate(self):
        return self.date
    
    def getCivilSt(self):
        return self.civilSt
    