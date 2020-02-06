from matplotlib import pyplot as p
from muro import Muro
from vacio import Vacio
from math import modf
import geopy.distance
import math
import shapefile


class Manzana:

    def __init__(self, esquinas_, id_):
        self.esquinas = esquinas_
        self.id = id_
        self.vacios = []
        self.muros = []
        self.longitud = self.getLong()
        self.relleno = [0]

    def __getitem__(self, xy):
        return self.esquinas[xy]

    def getNumEsquinas(self):
        n = 0
        for i in self:
            n = n + 1
        return n - 1

    def getLongPP(self, p, q):
        longitudpp = 0
        longitudpp = math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) + longitudpp
        return longitudpp

    def getLong(self):
        i = 0
        long = 0
        n = self.getNumEsquinas()
        while i < n:
            long = math.sqrt((self[i + 1][0] - self[i][0]) ** 2 + (self[i + 1][1] - self[i][1]) ** 2) + long
            i = i + 1
        return long

    def setEstructura(self, file):
        shp = shapefile.Reader(file)
        shapes = shp.shapes()
        for i, item in enumerate(self):
            for j in range(0, len(shapes), 3):
                try:
                    if int(self.getLongPP(item, shapes[j].points[:][0])
                           + self.getLongPP(self[i + 1], shapes[j].points[:][0])) \
                           == int(self.getLongPP(item, self[i + 1])):
                        if file == "../shapefiles/void":
                            self.vacios.append(Vacio(self.id,
                                                     [shapes[j].points[:][0],
                                                      shapes[j + 1].points[:][0],
                                                      shapes[j + 2].points[:][0]]))

                        elif file == "../shapefiles/wall":
                            self.muros.append(Muro(self.id,
                                                   [shapes[j].points[:][0],
                                                    shapes[j + 1].points[:][0],
                                                    shapes[j + 2].points[:][0]]))
                except IndexError:
                    continue

    def insertarEsquinas(self):
        # Añadir esquinas
        for i in range(self.getNumEsquinas()):
            ult = self.relleno[-1]
            esquina = self.getLongPP(self.esquinas[i], self.esquinas[i + 1]) + ult
            self.relleno.append(esquina)

    def insertarEstructura(self):
        # Añadir muros/vacios
        self.setEstructura("../shapefiles/void")
        self.setEstructura("../shapefiles/wall")
        if self.vacios:
            ini = self.getLongPP(self.vacios[0].final, self.esquinas[0])
            fin = ini + self.vacios[0].longitud
            info = [self.vacios[0]]

            # eventovacio = ["vacio", ini, fin, info]
            # self.relleno.insert(segmento, eventovacio)

        if self.muros:
            ini = self.getLongPP(self.muros[0].final, self.esquinas[0])
            fin = ini + self.muros[0].longitud
            info = [self.muros[0]]

            # eventomuro = ["vacio", ini, fin, info]
            # self.relleno.insert(segmento, eventomuro)
        #print(self.relleno)

    def rellenarManzana(self):
        self.insertarEsquinas()
        self.insertarEstructura()

    def mostrarVacios(self):
        for i in self.vacios:
            print("Vacios en Manzana " + str(self.id))
            print("Inicio " + str(i.inicio))
            print("Dentro " + str(i.dentro))
            print("Fin " + str(i.final))

    def mostrarMuros(self):
        for i in self.muros:
            print("Muros en Manzana " + str(self.id))
            print("Inicio " + str(i.inicio))
            print("Dentro " + str(i.dentro))
            print("Fin " + str(i.final))

    def mostrarManzana(self):
        x = [x[0] for x in self.esquinas]
        y = [y[1] for y in self.esquinas]
        p.plot(x, y)
        p.show()
