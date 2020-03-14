from matplotlib import pyplot as p


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
