import math
import utils
import shapefile


shpma = shapefile.Reader("../shapefilestotal/manzana")
shpva = shapefile.Reader("../shapefilestotal/void")
shpmu = shapefile.Reader("../shapefilestotal/wall")


def initManzanas(shpma, manzanas):
    global nmanzanas
    nmanzanas  = 0
    for index, coord in enumerate(shpma.shapeRecords()):
        nmanzanas = nmanzanas + 1
        count, nvect = (0, 0)
        vectoresx, vectoresy, distpq, tipovert = ([] for i in range(4))
        acumdist = [0]

        xy = [i for i in coord.shape.points[:]]
        xx = [i[0] for i in xy]
        yy = [i[1] for i in xy]

        while count < len(xy) - 1:
            vx = utils.calculateVector(xy[count], xy[count + 1], 0)  # X del vector
            vy = utils.calculateVector(xy[count], xy[count + 1], 1)  # Y del vector
            nvect = nvect + 1
            vectoresx.append(vx)
            vectoresy.append(vy)
            modulo = math.sqrt(vx ** 2 + vy ** 2)
            distpq.append(modulo)
            acumdist.append(acumdist[-1] + modulo)
            tipovert.append("CC")
            count = count + 1

        manzana = {"id": index, "x": xx, "y": yy, "dX": vectoresx, "dY": vectoresy, "dist": distpq,
                   "acumdist": acumdist,
                   "nvectores": nvect, "tipo": tipovert, "fachadas": [], "casas": []}
        manzanas.append(manzana)


def initEstructuras(shpestr, manzanas, estr):
    threshold = 0.45
    global nmuros, nvacios
    puntos, distend, segin, segen, nmuros, nvacios = (0, 0, 0, 0, 0, 0)
    estructura, segmentos, tipos = ([] for i in range(3))
    distinit = 10000

    for man in manzanas:
        for index, (x, y) in enumerate(zip(man['x'][:-1], man['y'][:-1])):
            for index2, coord in enumerate(shpestr.shapeRecords()):
                for i in coord.shape.points[:]:

                    dist = math.sqrt((x - i[0]) ** 2 + (y - i[1]) ** 2)
                    dist2 = math.sqrt((i[0] - man['x'][index + 1]) ** 2 + (i[1] - man['y'][index + 1]) ** 2)
                    dist3 = math.sqrt((x - man['x'][index + 1]) ** 2 + (y - man['y'][index + 1]) ** 2)

                    if dist + dist2 - dist3 < threshold:
                        r = shpestr.record(index2)
                        tip = (r['tipo'])
                        part = man['acumdist'][index] + dist
                        estructura.append(part)
                        segmentos.append(index)
                        tipos.append(tip)
                        puntos = puntos + 1

                        if puntos == 3:
                            for index, (punto, segmento, tipo) in enumerate(zip(estructura, segmentos, tipos)):
                                if distinit > punto:
                                    distinit = punto
                                    seginicio = segmento
                                if distend < punto:
                                    distend = punto
                                    segfinal = segmento

                            if shpestr == shpmu:
                                muro = {"mzn": man['id'], "cumdinit": distinit, "cumdend": distend,
                                        "seginit": seginicio,
                                        "segend": segfinal, "tipoestr": "muro"}
                                estr.append(muro)
                                nmuros = nmuros + 1
                            elif shpestr == shpva:
                                vacio = {"mzn": man['id'], "cumdinit": distinit, "cumdend": distend,
                                         "seginit": seginicio,
                                         "segend": segfinal, "tipoestr": "vacio"}
                                estr.append(vacio)
                                nvacios = nvacios + 1

                            puntos = 0
                            distinit = 10000
                            distend = 0
                            segmentos.clear()
                            estructura.clear()
