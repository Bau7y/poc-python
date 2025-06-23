#clase de estrategias

class ReglaTurno:
    def __init__(self, conocimiento, estrategia, energia):
        self.__conocimiento = conocimiento
        self.__estrategia = estrategia
        self.__energia = energia
    
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
