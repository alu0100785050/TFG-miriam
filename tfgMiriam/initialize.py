import math
import utils


def inicManzanas(shpma, manzanas):
    global nmanzanas
    nmanzanas = 0
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


def inicMuros(shpmu, muros, manzanas):
    tipos = []
    coords = []

    for obj in shpmu:
        tipos.append(obj.record['tipo'])
        coords.append(obj.shape.points)

    for man in manzanas:
        for index, x in enumerate(man['x'][:-1], 0):
            for tipo, coord in zip(tipos, coords):
                if coord and man['id'] not in [67, 78, 79]:

                    dist = math.sqrt((man['x'][index] - coord[0][0]) ** 2 + (man['y'][index] - coord[0][1]) ** 2)
                    dist2 = math.sqrt(
                        (coord[0][0] - man['x'][index + 1]) ** 2 + (coord[0][1] - man['y'][index + 1]) ** 2)
                    dist3 = math.sqrt(
                        (man['x'][index] - man['x'][index + 1]) ** 2 + (man['y'][index] - man['y'][index + 1]) ** 2)

                    if dist + dist2 - dist3 <= 1:

                        if man['id'] == 33:
                            if tipo is None:
                                tipo = 1

                        part = man['acumdist'][index] + dist

                        if man['id'] not in muros.keys():
                            muros[man['id']] = {}
                            muros[man['id']]['x'] = []
                            muros[man['id']]['y'] = []
                            muros[man['id']]['seg'] = []
                            muros[man['id']]['orden'] = []
                            muros[man['id']]['acumdist'] = []
                            muros[man['id']]['distsegpunto'] = []

                        muros[man['id']]['seg'].append(index)
                        muros[man['id']]['x'].append(coord[0][0])
                        muros[man['id']]['y'].append(coord[0][1])
                        muros[man['id']]['acumdist'].append(part)
                        muros[man['id']]['distsegpunto'].append(dist)

                        if tipo == 1:
                            muros[man['id']]['orden'].append(1)

                        elif tipo == 0:
                            muros[man['id']]['orden'].append(0)


def inicVacios(shpva, vacios, manzanas):
    tipos = []
    coords = []

    for obj in shpva:
        tipos.append(obj.record['tipo'])
        coords.append(obj.shape.points)

    for man in manzanas:
        for index, x in enumerate(man['x'][:-1], 0):
            for tipo, coord in zip(tipos, coords):

                if coord and man['id'] not in [67, 78, 79]:
                    dist = math.sqrt((man['x'][index] - coord[0][0]) ** 2 + (man['y'][index] - coord[0][1]) ** 2)
                    dist2 = math.sqrt(
                        (coord[0][0] - man['x'][index + 1]) ** 2 + (coord[0][1] - man['y'][index + 1]) ** 2)
                    dist3 = math.sqrt(
                        (man['x'][index] - man['x'][index + 1]) ** 2 + (man['y'][index] - man['y'][index + 1]) ** 2)

                    if dist + dist2 - dist3 <= 1:

                        part = man['acumdist'][index] + dist

                        if man['id'] not in vacios.keys():
                            vacios[man['id']] = {}
                            vacios[man['id']]['x'] = []
                            vacios[man['id']]['y'] = []
                            vacios[man['id']]['seg'] = []
                            vacios[man['id']]['orden'] = []
                            vacios[man['id']]['acumdist'] = []
                            vacios[man['id']]['distsegpunto'] = []

                        vacios[man['id']]['x'].append(coord[0][0])
                        vacios[man['id']]['y'].append(coord[0][1])
                        vacios[man['id']]['seg'].append(index)
                        vacios[man['id']]['acumdist'].append(part)
                        vacios[man['id']]['distsegpunto'].append(dist)

                        if tipo == 1:
                            vacios[man['id']]['orden'].append(1)

                        elif tipo == 0:
                            vacios[man['id']]['orden'].append(0)