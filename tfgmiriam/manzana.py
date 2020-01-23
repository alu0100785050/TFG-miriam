from matplotlib import pyplot as p
from muro import Muro
from vacio import Vacio
import math
import shapefile


class Manzana:

    def __init__(self, esquinas_, id_):
        self.esquinas = esquinas_
        self.id = id_
        self.vacios = []
        self.muros = []
        self.longitud = self.getlong()

    def __getitem__(self, xy):
        return self.esquinas[xy]

    def getnumesq(self):
        n = 0
        for i in self:
            n = n + 1
        return n - 1

    def getlongpp(self, p, q):
        longitudpp = 0
        longitudpp = math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) + longitudpp
        return longitudpp

    def getlong(self):
        i = 0
        long = 0
        n = self.getnumesq()
        while i < n:
            long = math.sqrt((self[i + 1][0] - self[i][0]) ** 2 + (self[i + 1][1] - self[i][1]) ** 2) + long
            i = i + 1
        return long

    def setexcepcion(self, file):
        shp = shapefile.Reader(file)
        shapes = shp.shapes()
        for i, item in enumerate(self):
            for j in range(0, len(shapes), 3):
                try:
                    if int(self.getlongpp(item, shapes[j].points[:][0]) +
                           self.getlongpp(self[i + 1], shapes[j].points[:][0])) == int(
                           self.getlongpp(item, self[i + 1])):
                        if file == "../shapefiles/void":
                            self.vacios.append(Vacio(self.id,
                                                         shapes[j].points[:][0],
                                                         shapes[j + 1].points[:][0],
                                                         shapes[j + 2].points[:][0]))

                        elif file == "../shapefiles/wall":
                            self.muros.append(Muro(self.id,
                                                       shapes[j].points[:][0],
                                                       shapes[j + 1].points[:][0],
                                                       shapes[j + 2].points[:][0]))
                except IndexError:
                    continue

    def rellenar(self):
        # Declarar evento inicial
        relleno = [0, self.getlong()]

        # Añadir esquinas
        esq = {}
        for i in range(self.getnumesq()):
            esq["esq{0}".format(i)] = self.getlongpp(self.esquinas[i], self.esquinas[i+1])
            relleno.insert(i, esq["esq{0}".format(i)])
        print(esq)
        print(relleno)

        # Añadir muros/vacios
        self.setexcepcion("../shapefiles/void")
        self.setexcepcion("../shapefiles/wall")

        if self.vacios:
            ini = self.getlongpp(self.esquinas[0], self.vacios[0][0].inicio)
            fin = self.getlongpp(self.esquinas[0], self.vacios[0][0].dentro) + \
                  self.getlongpp(self.vacios[0][0].dentro, self.vacios[0][0].final)
            info = [self.vacios[0][0].manzana,
                    self.vacios[0][0].inicio,
                    self.vacios[0][0].dentro,
                    self.vacios[0][0].final,
                    self.vacios[0][0].longitud]
            evvacio = ["vacio", ini, fin, info]
            relleno.insert(1, evvacio)

        if self.muros:
            ini = self.getlongpp(self.esquinas[0], self.vacios[0][0].inicio)
            fin = self.getlongpp(self.esquinas[0], self.vacios[0][0].dentro) + \
                  self.getlongpp(self.vacios[0][0].dentro, self.vacios[0][0].final)
            info = [self.muros[0][0].manzana,
                    self.muros[0][0].inicio,
                    self.muros[0][0].dentro,
                    self.muros[0][0].final,
                    self.muros[0][0].longitud]
            evmuro = ["muro", ini, fin, info]
            relleno.insert(1, evmuro)

        # Añadir casas

    def mostrarvacios(self):
        for i in self.vacios:
            print("Vacios en Manzana " + str(self.id))
            print("Inicio " + str(i[0].inicio))
            print("Dentro " + str(i[0].dentro))
            print("Fin " + str(i[0].fin))

    def mostrarmuros(self):
        for i in self.muros:
            print("Muros en Manzana " + str(self.id))
            print("Inicio " + str(i[0].inicio))
            print("Dentro " + str(i[0].dentro))
            print("Fin " + str(i[0].fin))

    def mostrar(self):
        x = [x[0] for x in self.esquinas]
        y = [y[1] for y in self.esquinas]
        p.plot(x, y)
        p.show()
