#clase de estrategias

class ReglaTurno:
    def __init__(self, conocimiento, estrategia, energia, rule):
        self.__conocimiento = conocimiento
        self.__estrategia = estrategia
        self.__energia = energia
        self.__rule = rule
    
    def SumaConocimientoEstrategia(self):
        return self.__conocimiento + self.__estrategia
    

    def SumaEstrategiaEnergia(self):
        return self.__estrategia + self.__energia
    

    def ConocimientoMenosEnergia(self):
        return (self.__conocimiento * 2) - self.__energia
    

    def SumaTodo(self):
        return self.__conocimiento + self.__estrategia + self.__energia
    
    
    def EstrategiaPorEnergia(self):
        return self.__estrategia * self.__energia
    
    def getRegla(self):
        return self.__rule
