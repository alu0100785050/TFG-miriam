import math

from matplotlib import pyplot as p
import imageio
from shapely.ops import cascaded_union
import statistics
from collections import defaultdict

global lmin, lmax, pmin, pmax, amin, amax
lmin = 45.0207 - 2 * 10.2515
lmax = 45.0207 + 2 * 10.2515
pmin = 18.1218 - 2 * 3.1631
pmax = 18.1218 + 2 * 3.1631
amin = 28.3898 - 2 * 4.9329
amax = 28.3898 + 2 * 4.9329


def insertListCoor(value, pos, lis):
    if pos == len(lis) - 1:
        lis.insert(pos, value)
    elif pos == len(lis):
        lis[pos-1] = value
    else:
        lis.insert(pos + 1, value)


def getMinMax(list):
    max = 0
    min = 10000

    for item in list:
        if item >= max:
            max = item
        if item <= min:
            min = item

    return min, max


def doIntersect(polygon1, polygon2):
    if polygon1.intersects(polygon2):
        return True
    else:
        return False


def mergePolygons(polygon1, polygon2):
    polygons = [polygon1, polygon2]
    u = cascaded_union(polygons)

    return u


def calculateVector(p, q, coord):
    x = (q[coord] - p[coord])
    return x


def mostrarManzana(manzana):
    xx = [x for x in manzana['x']]
    yy = [y for y in manzana['y']]
    p.plot(xx, yy)
    p.show()


def ajustarLongitud(lfac, lmax, lmin):
    if lfac > lmax or lfac < lmin:
        lfac = lmax


def ajustarProfundidad(pcasa, pmax, pmin):
    if pcasa > pmax or pcasa < pmin:
        pcasa = pmin


def ajustarAltura(acasa, amax, amin):
    if acasa > amax or acasa < amin:
        acasa = amin


def intersect(x0a, y0a, dxa, dya, x0b, y0b, dxb, dyb):
    t = (dyb * (x0b - x0a) - dxb * (y0b - y0a)) / (dxa * dyb - dxb * dya)

    return [x0a + dxa * t, y0a + dya * t]


def getSegmentosMuro(manzanas, muro):
    listasegm = []

    for manzana in manzanas:
        if manzana['id'] == muro:
            for index, tipo in enumerate(manzana['tipo']):
                if tipo is "CM":
                    listasegm.append(index)

    return listasegm


def generateOBJmanzanas(manzanas):
    f = open("manzanas.obj", "a")
    ncube = 0
    vertotales = 0

    for manzana in manzanas:
        for casa in manzana['casas']:
            f.write('o Cube' + str(ncube) + '\n')
            ncube = ncube + 1

            x, y = casa['poligono'].exterior.xy

            for xx, yy in zip(x[:-1], y[:-1]):
                f.write('v' + str(' '))
                f.write(str(xx / 2.2119) + str(' '))
                f.write(str(yy / 2.2119) + str(' '))
                f.write(str(casa['alturaterreno']))
                f.write('\n')

            for xx, yy in zip(x[:-1], y[:-1]):
                f.write('v' + str(' '))
                f.write(str(xx / 2.2119) + str(' '))
                f.write(str(yy / 2.2119) + str(' '))
                f.write(str(casa['alturacasa'] + casa['alturaterreno']))
                f.write('\n')

            nvert = len(x) - 1

            if nvert == 4:
                vertotales = vertotales + 8
                f.write('f ' + str(vertotales - 7) + ' ' + str(vertotales - 6) + ' ' +
                        str(vertotales - 5) + ' ' + str(vertotales - 4) + '\n')
                f.write('f ' + str(vertotales - 3) + ' ' + str(vertotales - 2) + ' ' +
                        str(vertotales - 1) + ' ' + str(vertotales) + '\n')

                for index in range(3):
                    f.write('f ' + str(vertotales - 7 + index) + ' ' + str(vertotales - 6 + index) + ' ' + str(
                        vertotales - 2 + index) + ' ' + str(vertotales - 3 + index) + '\n')

                f.write('f ' + str(vertotales - 4) + ' ' + str(vertotales - 7) + ' ' + str(vertotales - 3) + ' ' +
                        str(vertotales) + '\n')

            if nvert == 6:
                vertotales = vertotales + 12
                f.write('f ' + str(vertotales - 11) + ' ' + str(vertotales - 10) + ' ' +
                        str(vertotales - 9) + ' ' + str(vertotales - 8) + ' ' +
                        str(vertotales - 7) + ' ' + str(vertotales - 6) + '\n')
                f.write('f ' + str(vertotales - 5) + ' ' + str(vertotales - 4) + ' ' +
                        str(vertotales - 3) + ' ' + str(vertotales - 2) + ' ' +
                        str(vertotales - 1) + ' ' + str(vertotales) + '\n')

                for index in range(5):
                    f.write('f ' + str(vertotales - 11 + index) + ' ' + str(vertotales - 10 + index) + ' ' +
                            str(vertotales - 4 + index) + ' ' + str(vertotales - 5 + index) + '\n')

                f.write('f ' + str(vertotales - 6) + ' ' + str(vertotales - 11) + ' ' + str(vertotales - 5) + ' ' +
                        str(vertotales) + '\n')

    f.close()


def generateOBJmuros(muros, manoaptas):
    f = open("muros.obj", "a")
    ncube = 0
    vertotales = 0

    for muro in muros:
        if muro['mzn'] not in manoaptas:
            numvert = 0
            f.write('o Cube' + str(ncube) + '\n')
            ncube = ncube + 1

            for x, y in zip(muro['x'], muro['y']):
                numvert = numvert + 1
                f.write('v' + str(' '))
                f.write(str(x) + str(' '))
                f.write(str(y) + str(' '))
                f.write(str('0'))
                f.write('\n')
                vertotales = vertotales + 1

            for x, y in zip(muro['x'], muro['y']):
                f.write('v' + str(' '))
                f.write(str(x) + str(' '))
                f.write(str(y) + str(' '))
                f.write(str(15))
                f.write('\n')
                vertotales = vertotales + 1

            f.write('f ')
            for vert in range(vertotales - (numvert * 2), vertotales - numvert, 1):
                f.write(str(vert + 1) + str(' '))
            f.write(str('\n'))

            f.write('f ')
            for vert in range(vertotales - numvert, vertotales, 1):
                f.write(str(vert + 1) + str(' '))
            f.write(str('\n'))

            for vert in range(numvert - 1):
                f.write('f ')
                f.write(str(vertotales - numvert * 2 + vert + 1) + str(' ') + str(
                    vertotales - numvert * 2 + vert + 2) + str(' '))
                f.write(str(vertotales - numvert + vert + 2) + str(' ') + str(vertotales - numvert + vert + 1))
                f.write(str('\n'))

            f.write('f ' + str(vertotales - numvert * 2 + 1) + str(' ') + str(vertotales - numvert) + str(' ') +
                    str(vertotales) + str(' ') + str(vertotales - numvert + 1))
            f.write(str('\n'))

            f.write('f ' + str(vertotales - numvert - (numvert // 2) + 1) + str(' ') + str(
                vertotales - numvert - (numvert // 2)) + str(' ') +
                    str(vertotales - numvert + numvert // 2) + str(' ') + str(vertotales - numvert + numvert // 2 + 1))
            f.write(str('\n'))

    f.close()


def descartarManzanasVariasEstructuras(manzanas, muros, vacios):
    manzanasSencillas = []
    manzanasTotal = []
    manzanasComplejas = []

    for manzana in manzanas:
        manzanasTotal.append(manzana['id'])

    for key, muro in muros.items():
        if key not in manzanasSencillas:
            manzanasSencillas.append(key)
        else:
            manzanasComplejas.append(key)

        for key2, vacio in vacios.items():
            if key2 == key:
                if key not in manzanasComplejas:
                    manzanasComplejas.append(key)

    return manzanasTotal, manzanasSencillas, manzanasComplejas


def extraerInformacionPNG(imagen, manzanas):
    zs = []
    alturas = imageio.imread(imagen)

    for manzana in manzanas:
        for casa in manzana['casas']:
            xx, yy = casa['poligono'].exterior.xy
            zs.clear()

            for x, y in zip(xx, yy):
                z = alturas[round(-y) + 1, round(x) + 1]
                zs.append(z)

            zmean = statistics.mean(zs)
            casa['alturaterreno'] = zmean / 2


def elementosIguales(elementos):
    return all(x == elementos[0] for x in elementos)


def listarDuplicados(x, acumdist, distsegpunto, manzanas, manzana):
    tally = defaultdict(list)
    for num, item in enumerate(x):
        for num2, item2 in enumerate(x[num+1:], num+1):
            if item == item2:
                if abs(int(acumdist[num]) - int(acumdist[num2])) <= 2 or abs(int(acumdist[num]) - int(acumdist[num2])) == int(manzanas[manzana]['acumdist'][-1]):
                    tally[int(item)].append(num)
                    tally[int(item)].append(num2)
                if distsegpunto[num] > 2 and distsegpunto[num] > distsegpunto[num2]:
                    tally[int(item)].append(num)
                    tally[int(item)].append(num2)

    return tally


def eliminarPuntosDuplicados(estructura, manzanas):
    runned = []

    for key, item in estructura.items():
        dup = listarDuplicados(item['x'], item['acumdist'], item['distsegpunto'], manzanas, key)
        runned.append(key)

        for key, pos in dup.items():
            if len(pos) >= 2:
                if int(item['distsegpunto'][pos[0]]) > int(item['distsegpunto'][pos[1]]) and int(item['distsegpunto'][pos[0]]) > 2:
                    item['acumdist'][pos[0]] = None
                    item['x'][pos[0]] = None
                    item['y'][pos[0]] = None
                    item['distsegpunto'][pos[0]] = None
                    item['seg'][pos[0]] = None
                    item['orden'][pos[0]] = None
                else:
                    item['acumdist'][pos[1]] = None
                    item['x'][pos[1]] = None
                    item['y'][pos[1]] = None
                    item['distsegpunto'][pos[1]] = None
                    item['seg'][pos[1]] = None
                    item['orden'][pos[1]] = None

        item['acumdist'] = list(filter(None.__ne__, item['acumdist']))
        item['x'] = list(filter(None.__ne__, item['x']))
        item['y'] = list(filter(None.__ne__, item['y']))
        item['seg'] = list(filter(None.__ne__, item['seg']))
        item['orden'] = list(filter(None.__ne__, item['orden']))
        item['distsegpunto'] = list(filter(None.__ne__, item['distsegpunto']))

    return estructura