import math
import shapefile
from matplotlib import pyplot as p

shpma = shapefile.Reader("../shapefiles/manzana")
shpva = shapefile.Reader("../shapefiles/void")
shpmu = shapefile.Reader("../shapefiles/wall")
manzanas, muros, vacios = ([] for i in range(3))
nmanzanas, nmuros, nvacios = (0, 0, 0)


# Funciones auxiliares
def calculateVector(p, q, coord):
    x = (q[coord] - p[coord])
    return x


def mostrarManzana(manzana):
    xx = [x for x in manzana['x']]
    yy = [y for y in manzana['y']]
    p.plot(xx, yy)
    p.show()


# Paso 0 del algoritmo
def initManzanas():
    for coord in shpma.shapeRecords():
        global nmanzanas
        nmanzanas = nmanzanas + 1
        count, nvect = (0, 0)
        vectoresx, vectoresy, distpq, tipovert, vertfach = ([] for i in range(5))
        acumdist = [0]

        xy = [i for i in coord.shape.points[:]]
        xx = [i[0] for i in xy]
        yy = [i[1] for i in xy]

        while count < len(xy) - 1:
            vx = calculateVector(xy[count], xy[count + 1], 0)  # X del vector
            vy = calculateVector(xy[count], xy[count + 1], 1)  # Y del vector
            nvect = nvect + 1
            vectoresx.append(vx)
            vectoresy.append(vy)
            modulo = math.sqrt(vx ** 2 + vy ** 2)  # Distancia de vértice a vértice
            distpq.append(modulo)
            acumdist.append(acumdist[-1] + modulo)  # Distancia de origen a punto
            tipovert.append("CC")  # Inicializar a CC
            count = count + 1

        manzana = {"x": xx, "y": yy, "dX": vectoresx, "dY": vectoresy, "dist": distpq, "acumdist": acumdist,
                   "nvectores": nvect, "tipo": tipovert, "verticefachada": vertfach}

        manzanas.append(manzana)


# Paso 0 del algoritmo
def initEstructuras(shpestr):
    threshold = 0.45  # Umbral para comprobar si muro en cierto segmento
    nman, puntos, distend, segin, segen = (0, 0, 0, 0, 0)
    estructura, segmentos, tipos = ([] for i in range(3))
    distinit = 10000

    for man in manzanas:  # Recorrer manzanas
        nman = nman + 1
        for index, (x, y) in enumerate(zip(man['x'][:-1], man['y'][:-1])):  # Recorrer coordenadas dentro de cada manzana
            for index2, coord in enumerate(shpestr.shapeRecords()):  # Recorrer estructuras
                for i in coord.shape.points[:]:  # Recorrer coorenadas dentro de cada estructura

                    dist = math.sqrt((x - i[0]) ** 2 + (y - i[1]) ** 2)  # Distancia de muro a vértice anterior
                    dist2 = math.sqrt((i[0] - man['x'][index + 1]) ** 2 + (
                            i[1] - man['y'][index + 1]) ** 2)  # Distancia de muro a vértice siguiente
                    dist3 = math.sqrt((x - man['x'][index + 1]) ** 2 + (
                            y - man['y'][index + 1]) ** 2)  # Distancia de vértice a vértice

                    if dist + dist2 - dist3 < threshold:  # Si es menor entonces pertenece a esa manzana en ese segmento
                        r = shpestr.record(index2)
                        tip = (r['tipo'])  # Tipo 0 = dentro, tipo 1 = inicio/final
                        part = man['acumdist'][index] + dist  # Distancia desde el inicio hasta dicho punto
                        estructura.append(part)
                        segmentos.append(index)
                        tipos.append(tip)
                        puntos = puntos + 1

                        if puntos == 3:  # Cuando se tenga los tres puntos de la estructura
                            for index, (punto, segmento, tipo) in enumerate(zip(estructura, segmentos, tipos)):  # Se recorren para establecer el inicio y el fin
                                # TODO si el inicio del muro/vacío está antes del origen de la manzana
                                # if tip == 0:
                                #     if seg[index + 1] == segmen:
                                #         distinit1 = estructura[index + 1]
                                #     else:
                                #         continue
                                # if tip == 1 and type[index - 1] == 0:
                                #     distinit1 = punto
                                # if tip == 1 and type[index - 1] == 1:
                                #     pass
                                # if tip == 1 and type[index + 1] == 1:
                                #     pass

                                if distinit > punto:
                                    distinit = punto
                                    seginicio = segmento
                                if distend < punto:
                                    distend = punto
                                    segfinal = segmento

                            if shpestr == shpmu:
                                muro = {"mzn": nman, "cumdinit": distinit, "cumdend": distend, "seginit": seginicio,
                                        "segend": segfinal}
                                muros.append(muro)
                                global nmuros
                                nmuros = nmuros + 1
                            elif shpestr == shpva:
                                vacio = {"mzn": nman, "cumdinit": distinit, "cumdend": distend, "seginit": seginicio,
                                         "segend": segfinal}
                                vacios.append(vacio)
                                global nvacios
                                nvacios = nvacios + 1

                            puntos = 0
                            distinit = 10000
                            distend = 0
                            segmentos.clear()
                            estructura.clear()


# Paso 1 del algoritmo
def verticesEstructuras():
    pass


# Paso 0 - Inicializar manzanas, muros y vacios
initManzanas()
initEstructuras(shpmu)
initEstructuras(shpva)

# Paso 1 - Insertar vértices en muros/vacios

print(muros)
print(vacios)
print(nmanzanas)
print(nmuros)
print(nvacios)
