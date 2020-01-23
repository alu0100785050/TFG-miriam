import math


class Muro:

    def __init__(self, manzana_, inicio_, dentro_, final_):
        self.manzana = manzana_
        self.inicio = inicio_
        self.dentro = dentro_
        self.final = final_
        self.longitud = self.getlong()

    def __getitem__(self, item):
        return [self.inicio[item], self.dentro[item], self.final[item]]

    def getlong(self):
        self.long = math.sqrt((self.dentro[0] - self.inicio[0]) ** 2 + (self.dentro[1] - self.inicio[1]) ** 2) + \
                    math.sqrt((self.final[0] - self.dentro[0]) ** 2 + (self.final[1] - self.dentro[1]) ** 2)
        return self.long
