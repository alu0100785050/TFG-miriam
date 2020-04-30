from matplotlib import pyplot as p
from shapely.ops import cascaded_union
import numpy as np


global lmin, lmax, pmin, pmax, amin, amax
lmin = 45.0207 - 2 * 10.2515
lmax = 45.0207 + 2 * 10.2515
pmin = 18.1218 - 2 * 3.1631
pmax = 18.1218 + 2 * 3.1631
amin = 28.3898 - 2 * 4.9329
amax = 28.3898 + 2 * 4.9329


def insertListCoor(value, pos, lis):
    if pos == len(lis)-1:
        lis.append(value)
    else:
        lis.insert(pos+1, value)


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
    t = (dyb*(x0b-x0a)-dxb*(y0b-y0a)) / (dxa*dyb-dxb*dya)

    return [x0a+dxa*t, y0a+dya*t]