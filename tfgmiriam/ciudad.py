from manzana import Manzana
from matplotlib import pyplot as p
import shapefile


class Ciudad:
    manzanas = []

    def __init__(self, shpmanzanas):
        shpma = shapefile.Reader(shpmanzanas)
        k = 0

        for esq in shpma.shapeRecords():
            xy = [i for i in esq.shape.points[:]]
            self.manzanas.append(Manzana(xy, k))
            k = k + 1

    def __getitem__(self, n_man):
        return self.manzanas[n_man]

    def getnumm(self):
        n = 0
        for i in self.manzanas:
            n = n + 1
        return n

    def mostrar(self):
        for xy in self.manzanas:
            x = [i[0] for i in xy]
            y = [i[1] for i in xy]
            p.plot(x, y)
        p.show()


