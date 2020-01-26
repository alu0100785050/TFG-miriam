import math


class Estructura:

    def __init__(self, manzana_, inicio_, dentro_, final_, segmento_):
        self.manzana = manzana_
        self.inicio = inicio_
        self.dentro = dentro_
        self.final = final_
        self.longitud = self.getLong()
        self.segmento = segmento_

    def __getitem__(self, item):
        return [self.inicio[item], self.dentro[item], self.final[item]]

    def getLong(self):
        self.long = math.sqrt((self.inicio[0] - self.dentro[0]) ** 2 + (self.inicio[1] - self.dentro[1]) ** 2) + \
                    math.sqrt((self.dentro[0] - self.final[0]) ** 2 + (self.dentro[1] - self.final[1]) ** 2)
        return self.long
