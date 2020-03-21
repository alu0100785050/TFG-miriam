from matplotlib import pyplot as p
from shapely.geometry.polygon import LinearRing, Polygon
import numpy as np

global lmin, lmax, pmin, pmax, amin, amax
lmin = 45.0207 - 2 * 10.2515
lmax = 45.0207 + 2 * 10.2515
pmin = 18.1218 - 2 * 3.1631
pmax = 18.1218 + 2 * 3.1631
amin = 28.3898 - 2 * 4.9329
amax = 28.3898 + 2 * 4.9329


def mostrarCasasManzana(casas, manzana):
    for casa in casas:
        for coordenadas in casa:
            poly = Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)])
            x, y = poly.exterior.xy

            fig = p.figure(1, figsize=(5, 5), dpi=90)
            ax = fig.add_subplot(111)
            ax.plot(x, y, color='#6699cc', alpha=0.7, linewidth=2, solid_capstyle='round', zorder=2)
            ax.set_title('Polygon')
    p.show()


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