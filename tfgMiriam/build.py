import utils
import numpy as np
import math
from shapely.geometry.polygon import Polygon

np.random.seed(458)


def reordenarEstructuras(estructura, manzanas):
    for key, value in estructura.items():
        if value['orden'] == [1, 1, 0]:
            if value['acumdist'][2] > value['acumdist'][1] > value['acumdist'][0]:
                value['orden'][0], value['orden'][1], value['orden'][2] = \
                    value['orden'][1], value['orden'][2], value['orden'][0]

                value['acumdist'][0], value['acumdist'][1], value['acumdist'][2] = \
                    value['acumdist'][1], value['acumdist'][2], value['acumdist'][0]

                value['x'][0], value['x'][1], value['x'][2] = \
                    value['x'][1], value['x'][2], value['x'][0]

                value['y'][0], value['y'][1], value['y'][2] = \
                    value['y'][1], value['y'][2], value['y'][0]

                value['seg'][0], value['seg'][1], value['seg'][2] = \
                    value['seg'][1], value['seg'][2], value['seg'][0]

            elif value['acumdist'][1] > value['acumdist'][2] or value['acumdist'][2] > value['acumdist'][1]:
                value['orden'][1], value['orden'][2] = \
                    value['orden'][2], value['orden'][1]

                value['acumdist'][1], value['acumdist'][2] = \
                    value['acumdist'][2], value['acumdist'][1]

                value['x'][1], value['x'][2] = \
                    value['x'][2], value['x'][1]

                value['y'][1], value['y'][2] = \
                    value['y'][2], value['y'][1]

        elif value['orden'] == [0, 1, 1]:
            if value['acumdist'][0] > value['acumdist'][1]:
                value['orden'][0], value['orden'][1] = \
                    value['orden'][1], value['orden'][0]

                value['acumdist'][0], value['acumdist'][1] = \
                    value['acumdist'][1], value['acumdist'][0]

                value['x'][0], value['x'][1] = \
                    value['x'][1], value['x'][0]

                value['y'][0], value['y'][1] = \
                    value['y'][1], value['y'][0]

            elif value['acumdist'][0] < value['acumdist'][1]:
                value['orden'][0], value['orden'][1], value['orden'][2] = \
                    value['orden'][2], value['orden'][0], value['orden'][1]

                value['acumdist'][0], value['acumdist'][1], value['acumdist'][2] = \
                    value['acumdist'][2], value['acumdist'][0], value['acumdist'][1]

                value['x'][0], value['x'][1], value['x'][2] = \
                    value['x'][2], value['x'][0], value['x'][1]

                value['y'][0], value['y'][1], value['y'][2] = \
                    value['y'][2], value['y'][0], value['y'][1]

        # if value['seg'][2] == value['seg'][1] + 1:
        #     if value['seg'][-1] != 0:
        #         value['seg'][-1] = value['seg'][-1] - 1
                #value['acumdist'][-1] = manzanas[key]['acumdist'][value['seg'][-1]]


def preparaMuros(VManzanas, VMuros, mancom, manzana):

    if manzana['id'] not in mancom:
        acumdist = [0]
        for key, muro in VMuros.items():
            if manzana['id'] == key:
                vectoresx, vectoresy, distpq, tipovert = ([] for i in range(4))

                tmpX = VManzanas[manzana['id']]['x'][1:]
                tmpY = VManzanas[manzana['id']]['y'][1:]
                tipovert = VManzanas[manzana['id']]['tipo']
                linit = VMuros[key]['acumdist'][0]
                lend = VMuros[key]['acumdist'][2]
                sinit = VMuros[key]['seg'][0]
                send = VMuros[key]['seg'][2]

                distinit = linit - VManzanas[manzana['id']]['acumdist'][sinit]

                if int(distinit) <= 2:
                    tipovert[sinit] = 'CM'
                    insertinit = sinit
                else:
                    ux = VManzanas[manzana['id']]['dX'][sinit]
                    uy = VManzanas[manzana['id']]['dY'][sinit]
                    normu = VManzanas[manzana['id']]['dist'][sinit]
                    px = VManzanas[manzana['id']]['x'][sinit]
                    py = VManzanas[manzana['id']]['y'][sinit]
                    nuevox = px + distinit * (ux / normu)
                    nuevoy = py + distinit * (uy / normu)

                    utils.insertListCoor(nuevox, sinit, tmpX)
                    utils.insertListCoor(nuevoy, sinit, tmpY)
                    utils.insertListCoor('CM', sinit, tipovert)
                    insertinit = sinit + 1

                distend = lend -VManzanas[manzana['id']]['acumdist'][send]
                insertend = send + (insertinit - sinit)

                if int(distend) < 2:
                    if tipovert[insertend] in ('FV', 'CC'):
                        tipovert[insertend] = 'FM'
                else:
                    ux = VManzanas[manzana['id']]['dX'][send]
                    uy = VManzanas[manzana['id']]['dY'][send]
                    normu = VManzanas[manzana['id']]['dist'][send]
                    px = VManzanas[manzana['id']]['x'][send]
                    py = VManzanas[manzana['id']]['y'][send]
                    nuevox = px + distend * (ux / normu)
                    nuevoy = py + distend * (uy / normu)

                    utils.insertListCoor(nuevox, send, tmpX)
                    utils.insertListCoor(nuevoy, send, tmpY)

                    if insertend == insertinit:
                        tipovert[send+1] = 'FM'
                    else:
                        utils.insertListCoor('FM', send, tipovert)

                    insertend = insertend + 1

                tmpX.insert(0, tmpX[-1])
                tmpY.insert(0, tmpY[-1])
                VManzanas[manzana['id']]['x'] = tmpX
                VManzanas[manzana['id']]['y'] = tmpY

                tipovert[insertinit:insertend-1] = ['CM'] * (insertend - insertinit)

                for index, value in enumerate(manzana['x'][:-1]):
                    x = (VManzanas[manzana['id']]['x'][index + 1] - VManzanas[manzana['id']]['x'][index])
                    y = (VManzanas[manzana['id']]['y'][index + 1] - VManzanas[manzana['id']]['y'][index])
                    vectoresx.append(x)
                    vectoresy.append(y)
                    modulo = math.sqrt(x ** 2 + y ** 2)
                    distpq.append(modulo)
                    acumdist.append(acumdist[-1] + modulo)

                VManzanas[manzana['id']]['dX'] = vectoresx
                VManzanas[manzana['id']]['dY'] = vectoresy
                VManzanas[manzana['id']]['dist'] = distpq
                VManzanas[manzana['id']]['acumdist'] = acumdist
                VManzanas[manzana['id']]['tipo'] = tipovert
                VManzanas[manzana['id']]['nvectores'] = len(VManzanas[manzana['id']]['dX'])

                VMuros[key]['seg'][0] = insertinit
                VMuros[key]['seg'][-1] = insertend

# def preparaMuros(VManzanas, VMuros, mancom):
#     vectoresx, vectoresy, distpq, tipovert = ([] for i in range(4))
#
#     for manzana in VManzanas:
#         nvect = 0
#
#         if manzana['id'] not in mancom:
#             acumdist = [0]
#             for key, muro in VMuros.items():
#                 if manzana['id'] == key:
#                     tmpX = manzana['x'][1:]
#                     tmpY = manzana['y'][1:]
#                     tipo = manzana['tipo']
#                     linit = muro['acumdist'][0]
#                     lend = muro['acumdist'][2]
#                     sinit = muro['seg'][0]
#                     send = muro['seg'][2]
#
#                     distinit = linit - manzana['acumdist'][sinit+1]
#
#                     if distinit < 2:
#                         tipo[sinit] = 'CM'
#                         insertinit = sinit
#
#                     else:
#                         ux = manzana['dX'][sinit]
#                         uy = manzana['dY'][sinit]
#                         normu = manzana['dist'][sinit]
#                         px = manzana['x'][sinit]
#                         py = manzana['y'][sinit]
#                         nuevox = px + distinit * (ux / normu)
#                         nuevoy = py + distinit * (uy / normu)
#
#                         utils.insertListCoor(nuevox, sinit, tmpX)
#                         utils.insertListCoor(nuevoy, sinit, tmpY)
#                         utils.insertListCoor('CM', sinit, tipo)
#                         insertinit = sinit + 1
#
#                     distend = lend - manzana['acumdist'][send+1]
#                     insertend = send + (insertinit - sinit)
#
#                     if distend < 2:
#                         if tipo[insertend] in ('FV', 'CC'):
#                             tipo[insertend] = 'FM'
#                     else:
#                         ux = manzana['dX'][send]
#                         uy = manzana['dY'][send]
#                         normu = manzana['dist'][send]
#                         px = manzana['x'][send]
#                         py = manzana['y'][send]
#                         nuevox = px + distend * (ux / normu)
#                         nuevoy = py + distend * (uy / normu)
#
#                         utils.insertListCoor(nuevox, send, tmpX)
#                         utils.insertListCoor(nuevoy, send, tmpY)
#                         if insertinit == insertend:
#                             utils.insertListCoor('FM', send+1, tipo)
#                         else:
#                             utils.insertListCoor('FM', send, tipo)
#
#                         insertend = insertend + 1
#
#                     tmpX.insert(0, tmpX[-1])
#                     tmpY.insert(0, tmpY[-1])
#
#                     tipo[insertinit:insertend - 1] = ['CM'] * (insertend - insertinit - 1)
#
#                     manzana['x'] = tmpX
#                     manzana['y'] = tmpY
#                     for index, value in enumerate(tipo[:-1]):
#                         x = (manzana['x'][index + 1] - manzana['x'][index])
#                         y = (manzana['y'][index + 1] - manzana['y'][index])
#                         nvect = nvect + 1
#                         vectoresx.append(x)
#                         vectoresy.append(y)
#                         modulo = math.sqrt(x ** 2 + y ** 2)
#                         distpq.append(modulo)
#                         acumdist.append(acumdist[-1] + modulo)
#
#                     manzana.update(dX=vectoresx, dY=vectoresy, dist=distpq, acumdist=acumdist, nvectores=nvect, tipo=tipo)
#
#                     muro['seg'][0] = insertinit
#                     muro['seg'][-1] = insertend


def preparaVacios(VManzanas, VVacios, mancom):
    vectoresx, vectoresy, distpq, tipovert = ([] for i in range(4))

    for manzana in VManzanas:
        nvect = 0
        if manzana['id'] not in mancom:
            acumdist = [0]
            for key, vacio in VVacios.items():
                if manzana['id'] == key:
                    tmpX = manzana['x'][1:]
                    tmpY = manzana['y'][1:]
                    tipo = manzana['tipo']
                    linit = vacio['acumdist'][0]
                    lend = vacio['acumdist'][2]
                    sinit = vacio['seg'][0]
                    send = vacio['seg'][2]

                    distinit = linit - manzana['acumdist'][sinit+1]

                    if distinit < 2:
                        tipo[sinit] = 'CV'
                        insertinit = sinit

                    else:
                        ux = manzana['dX'][sinit]
                        uy = manzana['dY'][sinit]
                        normu = manzana['dist'][sinit]
                        px = manzana['x'][sinit]
                        py = manzana['y'][sinit]
                        nuevox = px + distinit * (ux / normu)
                        nuevoy = py + distinit * (uy / normu)

                        utils.insertListCoor(nuevox, sinit-1, tmpX)
                        utils.insertListCoor(nuevoy, sinit-1, tmpY)
                        utils.insertListCoor('CV', sinit, tipo)
                        insertinit = sinit + 1

                    distend = lend - manzana['acumdist'][send+1]
                    insertend = send + (insertinit - sinit)

                    if distend < 2:
                        if tipo[insertend] in ('FM', 'CC'):
                            tipo[insertend] = 'FV'
                    else:
                        ux = manzana['dX'][send]
                        uy = manzana['dY'][send]
                        normu = manzana['dist'][send]
                        px = manzana['x'][send]
                        py = manzana['y'][send]
                        nuevox = px + distend * (ux / normu)
                        nuevoy = py + distend * (uy / normu)

                        utils.insertListCoor(nuevox, send, tmpX)
                        utils.insertListCoor(nuevoy, send, tmpY)
                        if insertinit == insertend:
                            utils.insertListCoor('FV', send+1, tipo)
                        else:
                            utils.insertListCoor('FV', send, tipo)
                        insertend = insertend + 1

                    tmpX.insert(0, tmpX[-1])
                    tmpY.insert(0, tmpY[-1])

                    tipo[insertinit:insertend - 1] = ['CV'] * (insertend - insertinit-1)

                    manzana['x'] = tmpX
                    manzana['y'] = tmpY
                    for index, value in enumerate(tipo[:-1]):
                        x = (manzana['x'][index + 1] - manzana['x'][index])
                        y = (manzana['y'][index + 1] - manzana['y'][index])
                        nvect = nvect + 1
                        vectoresx.append(x)
                        vectoresy.append(y)
                        modulo = math.sqrt(x ** 2 + y ** 2)
                        distpq.append(modulo)
                        acumdist.append(acumdist[-1] + modulo)

                    manzana.update(dX=vectoresx, dY=vectoresy, dist=distpq, acumdist=acumdist, nvectores=nvect, tipo=tipo)

                    vacio['seg'][0] = insertinit
                    vacio['seg'][-1] = insertend


def rellenaFachadas(VManzanas, mzn):
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

    for key, muro in muros.items():

        listy.clear()
        listx.clear()
        if key not in mancom:
            for manzana in manzanas:
                 if key == manzana['id']:
                    muro['x'].clear()
                    muro['y'].clear()
                    for index, tipo in enumerate(manzana['tipo']):
                        if tipo is 'CM':
                            muro['x'].append(manzana['x'][index])
                            muro['y'].append(manzana['y'][index])

                        if tipo is 'FM' and manzana['tipo'][index-1] is 'CM':
                            muro['x'].append(manzana['x'][index])
                            muro['y'].append(manzana['y'][index])

            seg = utils.getSegmentosMuro(manzanas, key)
            for index, element in reversed(list(enumerate(muro['x']))):

                if index == len(muro['x'])-1:
                    xvector = manzanas[key]['dX'][seg[-1]]
                    yvector = manzanas[key]['dY'][seg[-1]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][index] + vx
                    yy = muro['y'][index] + vy

                    muro['x'].append(xx)
                    muro['y'].append(yy)

                elif index == 0:
                    xvector = manzanas[key]['dX'][seg[0]]
                    yvector = manzanas[key]['dY'][seg[0]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][index] + vx
                    yy = muro['y'][index] + vy

                    muro['x'].append(xx)
                    muro['y'].append(yy)

                else:
                    xvector = manzanas[key]['dX'][seg[index-1]]
                    yvector = manzanas[key]['dY'][seg[index-1]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][index - 1] + vx
                    yy = muro['y'][index - 1] + vy

                    xvector2 = manzanas[key]['dX'][seg[index]]
                    yvector2 = manzanas[key]['dY'][seg[index]]
                    perp2 = [yvector2, -xvector2]
                    mod2 = math.sqrt(perp2[1] ** 2 + perp2[0] ** 2)
                    vx2 = np.divide(perp2[0], mod2) * 12
                    vy2 = np.divide(perp2[1], mod2) * 12
                    xx2 = muro['x'][index + 1] + vx2
                    yy2 = muro['y'][index + 1] + vy2

                    dx1 = manzanas[key]['dX'][seg[index-1]]
                    dy1 = manzanas[key]['dY'][seg[index-1]]
                    dx2 = manzanas[key]['dX'][seg[index]]
                    dy2 = manzanas[key]['dY'][seg[index]]

                    puntoesquina = utils.intersect(xx, yy, dx1, dy1, xx2, yy2, dx2, dy2)

                    muro['x'].append(puntoesquina[0])
                    muro['y'].append(puntoesquina[1])
