import utils
import numpy as np
import math
from shapely.geometry.polygon import Polygon

np.random.seed(458)


def preparaEstructura(VManzanas, VEstructuras, mzn):
    tolerancia = 10
    count, nvect, insertinit, insertend = (0, 0, 0, 0)
    vectoresx, vectoresy, distpq, tipovert, vertfach = ([] for i in range(5))
    acumdist = [0]

    for estructura in VEstructuras:
        if estructura['mzn'] == mzn['id']:
            tmpX = VManzanas[mzn['id']]['x'][1:]
            tmpY = VManzanas[mzn['id']]['y'][1:]
            tipo = VManzanas[mzn['id']]['tipo']
            linit = estructura['cumdinit']
            lend = estructura['cumdend']
            sinit = estructura['seginit']
            send = estructura['segend']

            distinit = linit - VManzanas[mzn['id']]['acumdist'][sinit]
            insertinit = sinit

            if distinit < tolerancia:
                if estructura['tipoestr'] == "muro":
                    tipo[sinit] = 'CM'
                elif estructura['tipoestr'] == "vacio":
                    tipo[sinit] = 'CV'
            else:
                ux = VManzanas[mzn['id']]['dX'][sinit]
                uy = VManzanas[mzn['id']]['dY'][sinit]
                normu = VManzanas[mzn['id']]['dist'][sinit]
                px = VManzanas[mzn['id']]['x'][sinit]
                py = VManzanas[mzn['id']]['y'][sinit]
                nuevox = px + distinit * (ux / normu)
                nuevoy = py + distinit * (uy / normu)

                utils.insertListCoor(nuevox, insertinit-1, tmpX)
                utils.insertListCoor(nuevoy, insertinit-1, tmpY)

                if estructura['tipoestr'] == "muro":
                    tipo.insert(sinit+1, 'CM')
                elif estructura['tipoestr'] == "vacio":
                    tipo.insert(sinit+1, 'CV')

                insertinit = insertinit + 1

            distend = lend - VManzanas[mzn['id']]['acumdist'][send]
            insertend = send + (insertinit - sinit)

            if distend < tolerancia:
                if estructura['tipoestr'] == "muro":
                    if tipo[send] in ('FV', 'CC'):
                        tipo[send] = 'FM'
                elif estructura['tipoestr'] == "vacio":
                    if tipo[send] in ('FM', 'CC'):
                        tipo[send] = 'FV'
            else:
                ux = VManzanas[mzn['id']]['dX'][send]
                uy = VManzanas[mzn['id']]['dY'][send]
                normu = VManzanas[mzn['id']]['dist'][send]
                px = VManzanas[mzn['id']]['x'][send]
                py = VManzanas[mzn['id']]['y'][send]
                nuevox = px + distend * (ux / normu)
                nuevoy = py + distend * (uy / normu)

                utils.insertListCoor(nuevox, insertend-1, tmpX)
                utils.insertListCoor(nuevoy, insertend-1, tmpY)

                if estructura['tipoestr'] == "muro":
                    if insertend == insertinit:
                        tipo.insert(insertend+1, 'FM')
                    else:
                        tipo.insert(insertend, 'FM')
                elif estructura['tipoestr'] == "vacio":
                    if insertend == insertinit:
                        tipo.insert(insertend+1, 'FV')
                    else:
                        tipo.insert(insertend, 'FV')

                insertend = insertend + 1

            tmpX.insert(0, tmpX[-1])
            tmpY.insert(0, tmpY[-1])

            if estructura['tipoestr'] == "muro":
                tipo[insertinit+1:insertend - 1] = ['CM'] * (insertend-1 - insertinit)
            elif estructura['tipoestr'] == "vacio":
                tipo[insertinit+1:insertend - 1] = ['CV'] * (insertend-1 - insertinit)

            VManzanas[mzn['id']]['x'] = tmpX
            VManzanas[mzn['id']]['y'] = tmpY
            while count < len(tmpX) - 1:
                x = (VManzanas[mzn['id']]['x'][count + 1] - VManzanas[mzn['id']]['x'][count])
                y = (VManzanas[mzn['id']]['y'][count + 1] - VManzanas[mzn['id']]['y'][count])
                nvect = nvect + 1
                vectoresx.append(x)
                vectoresy.append(y)
                modulo = math.sqrt(x ** 2 + y ** 2)  # Distancia de vértice a vértice
                distpq.append(modulo)
                acumdist.append(acumdist[-1] + modulo)  # Distancia de origen a punto
                count = count + 1

            mzn.update(dX=vectoresx, dY=vectoresy, dist=distpq, acumdist=acumdist, nvectores=nvect, tipo=tipo)

            estructura['seginit'] = insertinit
            estructura['segend'] = insertend


def rellenaFachadas(VManzanas, mzn, lmin, lmax):
    fachadas = []
    nsegmentos = VManzanas[mzn['id']]['nvectores']
    nfachadas, x, y, segmento, dp = (0, 0, 0, 0, 0)

    for index, segmento in enumerate(range(nsegmentos)):
        nfachadas = nfachadas + 1

        if VManzanas[mzn['id']]['tipo'][segmento] in ('FM', 'FV', 'CC'):
            dp = 0
            di = VManzanas[mzn['id']]['dist'][segmento]
            cdp = VManzanas[mzn['id']]['acumdist'][segmento]

            if di < utils.lmin:
                nfachadas = nfachadas + 1
                xvector = VManzanas[mzn['id']]['dX'][segmento]
                yvector = VManzanas[mzn['id']]['dY'][segmento]
                vx = np.divide(xvector, VManzanas[mzn['id']]['dist'][segmento]) * dp
                vy = np.divide(yvector, VManzanas[mzn['id']]['dist'][segmento]) * dp
                xx = VManzanas[mzn['id']]['x'][segmento] + vx
                yy = VManzanas[mzn['id']]['y'][segmento] + vy
                tipo = VManzanas[mzn['id']]['tipo'][segmento]
                cdp = cdp + di
                print("No se puede construir una fachada más pequeña que el mínimo establecido en la manzana " + str(mzn['id']))

                fachada = {"x": xx, "y": yy, "long": di, "seg": segmento, "mzn": mzn['id'], "tipo": tipo, "esquina": False}
                fachadas.insert(nfachadas, fachada)

            else:
                while dp < di:
                    lfac = np.random.normal(45.0207, 10.2515)
                    utils.ajustarLongitud(lfac, utils.lmax, utils.lmin)
                    dist1 = di - dp

                    if 0 < dist1 < utils.lmin:
                        nfachadas = nfachadas + 1
                        lfac = fachadas[-1]['long'] + dist1
                        fachadas[-1].update(long=lfac)

                        dp = dp + dist1
                        cdp = cdp + dist1

                    else:

                        nfachadas = nfachadas + 1
                        xvector = VManzanas[mzn['id']]['dX'][segmento]
                        yvector = VManzanas[mzn['id']]['dY'][segmento]
                        vx = np.divide(xvector, VManzanas[mzn['id']]['dist'][segmento]) * dp
                        vy = np.divide(yvector, VManzanas[mzn['id']]['dist'][segmento]) * dp
                        xx = VManzanas[mzn['id']]['x'][segmento] + vx
                        yy = VManzanas[mzn['id']]['y'][segmento] + vy
                        tipo = VManzanas[mzn['id']]['tipo'][segmento]

                        cdp = cdp + lfac
                        dp = dp + lfac

                        fachada = {"x": xx, "y": yy, "long": lfac, "seg": segmento, "mzn": mzn['id'], "tipo": tipo,
                                   "esquina": False}
                        fachadas.insert(nfachadas, fachada)

        else:
            seg = segmento

            cdp = VManzanas[mzn['id']]['acumdist'][segmento]
            longitud = VManzanas[mzn['id']]['dist'][segmento]

            nfachadas = nfachadas + 1
            xx = VManzanas[mzn['id']]['x'][segmento]
            yy = VManzanas[mzn['id']]['y'][segmento]
            tipo = VManzanas[mzn['id']]['tipo'][segmento]

            dp = dp + longitud
            cdp = cdp + longitud
            segmento = segmento + 1

            fachada = {"x": xx, "y": yy, "long": longitud, "seg": seg, "mzn": mzn['id'], "tipo": tipo, "esquina": False}
            fachadas.insert(nfachadas, fachada)

    mzn['fachadas'] = fachadas


def construirCasas(fachadas, casas, mzn):
    casas = []
    for index, fachada in enumerate(fachadas[:-1]):

        if fachadas[index]['seg'] != fachadas[index -1]['seg']:
            if fachadas[index]['esquina'] == False and fachadas[index - 1]['esquina'] == False:
                if fachadas[index - 1]['tipo'] in ('FM', 'FV', 'CC') and fachadas[index]['tipo'] in ('FM', 'FV', 'CC'):
                    pcas = np.random.normal(18.1218, 3.1631)
                    utils.ajustarProfundidad(pcas, utils.pmax, utils.pmin)
                    lcas = fachadas[index - 1]['long'] + fachadas[index]['long']

                    xvector = mzn['dX'][fachadas[index - 1]['seg']]
                    yvector = mzn['dY'][fachadas[index - 1]['seg']]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)
                    vx = np.divide(perp[0], mod) * pcas
                    vy = np.divide(perp[1], mod) * pcas
                    xx = fachadas[index - 1]['x'] + vx
                    yy = fachadas[index - 1]['y'] + vy

                    xvector2 = mzn['dX'][fachada['seg']]
                    yvector2 = mzn['dY'][fachada['seg']]
                    perp2 = [yvector2, -xvector2]
                    mod2 = math.sqrt(perp2[1] ** 2 + perp2[0] ** 2)
                    vx2 = np.divide(perp2[0], mod2) * pcas
                    vy2 = np.divide(perp2[1], mod2) * pcas
                    xx2 = fachadas[index + 1]['x'] + vx2
                    yy2 = fachadas[index + 1]['y'] + vy2

                    dx1 = mzn['dX'][fachadas[index - 1]['seg']]
                    dy1 = mzn['dY'][fachadas[index - 1]['seg']]
                    dx2 = mzn['dX'][fachadas[index]['seg']]
                    dy2 = mzn['dY'][fachadas[index]['seg']]

                    puntoesquina = utils.intersect(xx, yy, dx1, dy1, xx2, yy2, dx2, dy2)

                    polygon = Polygon(
                        [(fachadas[index - 1]['x'], fachadas[index - 1]['y']), (fachadas[index]['x'], fachadas[index]['y']),
                         (fachadas[index + 1]['x'], fachadas[index + 1]['y']), (xx2, yy2), (puntoesquina[0], puntoesquina[1]),
                         (xx, yy)])

                    acas = np.random.normal(28.3898, 4.9329)
                    utils.ajustarAltura(acas, utils.amax, utils.amin)

                    casa = {"mzn": mzn['id'], "longitudcasa": lcas, "profundidadcasa": pcas, "alturacasa": acas,
                            "xfachada1": fachadas[index - 1]['x'],
                            "yfachada1": fachadas[index - 1]['y'], "xfachada2": fachadas[index]['x'],
                            "yfachada2": fachadas[index]['y'],
                            "xfachada3": fachadas[index + 1]['x'], "yfachada3": fachadas[index + 1]['y'],
                            "x1": xx, "y1": yy, "x2": xx2, "y2": yy2, "puntoesquina": puntoesquina, "poligono": polygon}

                    fachadas[index - 1].update(esquina=True)
                    fachadas[index].update(esquina=True)
                    casas.insert(index, casa)

        else:
            if fachadas[index]['seg'] == fachadas[index+1]['seg']:
                if fachadas[index]['tipo'] in ('FM', 'FV', 'CC'):
                    pcas = np.random.normal(18.1218, 3.1631)
                    utils.ajustarProfundidad(pcas, utils.pmax, utils.pmin)

                    xvector = mzn['dX'][fachadas[index]['seg']]
                    yvector = mzn['dY'][fachadas[index]['seg']]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * pcas
                    vy = np.divide(perp[1], mod) * pcas
                    xx = fachadas[index]['x'] + vx
                    yy = fachadas[index]['y'] + vy
                    xx2 = fachadas[index + 1]['x'] + vx
                    yy2 = fachadas[index + 1]['y'] + vy

                    polygon = Polygon(
                        [(fachadas[index]['x'], fachadas[index]['y']),
                         (fachadas[index + 1]['x'], fachadas[index + 1]['y']),
                         (xx2, yy2), (xx, yy)])

                    acas = np.random.normal(28.3898, 4.9329)
                    utils.ajustarAltura(acas, utils.amax, utils.amin)

                    casa = {"mzn": mzn['id'], "longitudcasa": fachadas[index]['long'], "profundidadcasa": pcas, 'alturacasa': acas,
                            "xfachada1": fachadas[index]['x'], "yfachada1": fachadas[index]['y'],
                            "xfachada2": fachadas[index+1]['x'], "yfachada2": fachadas[index+1]['y'],
                            "x1": xx, "y1": yy, "x2": xx2, "y2": yy2, "poligono": polygon}

                    casas.insert(index, casa)

    mzn['casas'] = casas


def profundidadMuros(muros, manzanas, mancom):
    listy = []
    listx = []

    for muro in muros:

        listy.clear()
        listx.clear()
        if muro['mzn'] not in mancom:
            for manzana in manzanas:
                 if muro['mzn'] == manzana['id']:
                    for index, tipo in enumerate(manzana['tipo']):
                        if tipo is 'CM':
                            muro['x'].append(manzana['x'][index])
                            muro['y'].append(manzana['y'][index])

                        if tipo is 'FM' and manzana['tipo'][index-1] is 'CM':
                            muro['x'].append(manzana['x'][index])
                            muro['y'].append(manzana['y'][index])

            seg = utils.getSegmentosMuro(manzanas, muro)
            for index, element in reversed(list(enumerate(muro['x']))):

                if index == len(muro['x'])-1:
                    xvector = manzanas[muro['mzn']]['dX'][seg[-1]]
                    yvector = manzanas[muro['mzn']]['dY'][seg[-1]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][index] + vx
                    yy = muro['y'][index] + vy

                    muro['x'].append(xx)
                    muro['y'].append(yy)

                elif index == 0:
                    xvector = manzanas[muro['mzn']]['dX'][seg[0]]
                    yvector = manzanas[muro['mzn']]['dY'][seg[0]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][index] + vx
                    yy = muro['y'][index] + vy

                    muro['x'].append(xx)
                    muro['y'].append(yy)

                else:
                    xvector = manzanas[muro['mzn']]['dX'][seg[index-1]]
                    yvector = manzanas[muro['mzn']]['dY'][seg[index-1]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][index - 1] + vx
                    yy = muro['y'][index - 1] + vy

                    xvector2 = manzanas[muro['mzn']]['dX'][seg[index]]
                    yvector2 = manzanas[muro['mzn']]['dY'][seg[index]]
                    perp2 = [yvector2, -xvector2]
                    mod2 = math.sqrt(perp2[1] ** 2 + perp2[0] ** 2)
                    vx2 = np.divide(perp2[0], mod2) * 12
                    vy2 = np.divide(perp2[1], mod2) * 12
                    xx2 = muro['x'][index + 1] + vx2
                    yy2 = muro['y'][index + 1] + vy2

                    dx1 = manzanas[muro['mzn']]['dX'][seg[index-1]]
                    dy1 = manzanas[muro['mzn']]['dY'][seg[index-1]]
                    dx2 = manzanas[muro['mzn']]['dX'][seg[index]]
                    dy2 = manzanas[muro['mzn']]['dY'][seg[index]]

                    puntoesquina = utils.intersect(xx, yy, dx1, dy1, xx2, yy2, dx2, dy2)

                    muro['x'].append(puntoesquina[0])
                    muro['y'].append(puntoesquina[1])
