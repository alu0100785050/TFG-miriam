import math


class Estructura:

    def __init__(self, manzana_, coordenadas_):
        self.manzana = manzana_
        self.coordenadas = coordenadas_
        # self.inicio = inicio_
        # self.final = final_
        # self.dentro = dentro_
        self.longitud = 0

    def __getitem__(self, item):
        return [self.coordenadas]

    def getLong(self):
        self.longitud = math.sqrt((self.inicio[0] - self.dentro[0]) ** 2 + (self.inicio[1] - self.dentro[1]) ** 2) + \
                    math.sqrt((self.dentro[0] - self.final[0]) ** 2 + (self.dentro[1] - self.final[1]) ** 2)
        return self.longitud
