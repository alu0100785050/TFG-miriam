import utils
import numpy as np
import math
from shapely.geometry.polygon import Polygon
import copy

np.random.seed(458)


def reordenarEstructuras(estructuras):
    for key, value in estructuras.items():
        VValues = copy.deepcopy(value)
        originalindex = np.argsort(value['acumdist'])
        for index, i in enumerate(originalindex):
            value['acumdist'][index] = VValues['acumdist'][i]
            value['x'][index] = VValues['x'][i]
            value['y'][index] = VValues['y'][i]
            value['orden'][index] = VValues['orden'][i]
            value['seg'][index] = VValues['seg'][i]

        if value['orden'] == [1, 1, 0]:
            for key in value.keys():
                value[key][0], value[key][1], value[key][2] = \
                    value[key][1], value[key][2], value[key][0]

        if value['orden'] == [0, 1, 1]:
            for key in value.keys():
                value[key][0], value[key][1], value[key][2] = \
                    value[key][2], value[key][0], value[key][1]


def preparaMuros(VManzanas, VMuros, manzana):
    acumdist = [0]
    for key, muro in VMuros.items():
        if manzana['id'] == key:
            VSeg = copy.deepcopy(VMuros[key]['seg'])
            vectoresx, vectoresy, distpq, tipovert = ([] for i in range(4))

            tmpX = VManzanas[manzana['id']]['x'][1:]
            tmpY = VManzanas[manzana['id']]['y'][1:]
            tipovert = VManzanas[manzana['id']]['tipo']
            linit = VMuros[key]['acumdist'][0]
            lend = VMuros[key]['acumdist'][2]
            sinit = VMuros[key]['seg'][0]
            send = VMuros[key]['seg'][2]

            distinit = linit - VManzanas[manzana['id']]['acumdist'][sinit]
            insertinit = sinit

            if int(distinit) <= 2:
                tipovert[insertinit] = 'CM'
            else:
                ux = VManzanas[manzana['id']]['dX'][sinit]
                uy = VManzanas[manzana['id']]['dY'][sinit]
                normu = VManzanas[manzana['id']]['dist'][sinit]
                px = VManzanas[manzana['id']]['x'][sinit]
                py = VManzanas[manzana['id']]['y'][sinit]
                nuevox = px + distinit * (ux / normu)
                nuevoy = py + distinit * (uy / normu)

                tmpX.insert(insertinit, nuevox)
                tmpY.insert(insertinit, nuevoy)
                tipovert.insert(insertinit + 1, 'CM')
                insertinit = sinit + 1

            distend = lend - VManzanas[manzana['id']]['acumdist'][send]
            insertend = send + (insertinit - sinit)

            if int(distend) <= 2:
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

                if VSeg[0] == VSeg[2]:
                    tmpX.insert(insertend - 1, nuevox)
                    tmpY.insert(insertend - 1, nuevoy)
                else:
                    tmpX.insert(insertend, nuevox)
                    tmpY.insert(insertend, nuevoy)

                if VSeg[0] == VSeg[2]:
                    tipovert.insert(insertend, 'FM')
                else:
                    tipovert.insert(insertend + 1, 'FM')

                insertend = insertend + 1

            tmpX.insert(0, manzana['x'][-1])
            tmpY.insert(0, manzana['y'][-1])
            VManzanas[manzana['id']]['x'] = tmpX
            VManzanas[manzana['id']]['y'] = tmpY

            if VSeg[0] == VSeg[2] and linit > lend:
                insertinit, insertend = insertend, insertinit

            if insertend < insertinit:
                tipovert[0:insertend] = ['CM'] * (insertend)
                tipovert[insertinit + 1:] = ['CM'] * (len(tipovert) - 1 - insertinit)
            else:
                tipovert[insertinit:insertend] = ['CM'] * (insertend - insertinit)

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


def preparaVacios(VManzanas, VVacios, manzana):
    acumdist = [0]
    for key, vacio in VVacios.items():
        if manzana['id'] == key:
            vectoresx, vectoresy, distpq, tipovert = ([] for i in range(4))

            tmpX = VManzanas[manzana['id']]['x'][1:]
            tmpY = VManzanas[manzana['id']]['y'][1:]
            tipovert = VManzanas[manzana['id']]['tipo']
            linit = VVacios[key]['acumdist'][0]
            lend = VVacios[key]['acumdist'][2]
            sinit = VVacios[key]['seg'][0]
            send = VVacios[key]['seg'][2]

            distinit = linit - VManzanas[manzana['id']]['acumdist'][sinit]
            insertinit = sinit

            if int(distinit) <= 2:
                tipovert[sinit] = 'CV'
            else:
                ux = VManzanas[manzana['id']]['dX'][sinit]
                uy = VManzanas[manzana['id']]['dY'][sinit]
                normu = VManzanas[manzana['id']]['dist'][sinit]
                px = VManzanas[manzana['id']]['x'][sinit]
                py = VManzanas[manzana['id']]['y'][sinit]
                nuevox = px + distinit * (ux / normu)
                nuevoy = py + distinit * (uy / normu)

                tmpX.insert(insertinit, nuevox)
                tmpY.insert(insertinit, nuevoy)
                tipovert.insert(insertinit + 1, 'CV')
                insertinit = sinit + 1

            distend = lend - VManzanas[manzana['id']]['acumdist'][send]
            insertend = send + (insertinit - sinit)

            if int(distend) <= 2:
                if tipovert[send] in ('FM', 'CC'):
                    tipovert[send] = 'FV'
            else:
                ux = VManzanas[manzana['id']]['dX'][send]
                uy = VManzanas[manzana['id']]['dY'][send]
                normu = VManzanas[manzana['id']]['dist'][send]
                px = VManzanas[manzana['id']]['x'][send]
                py = VManzanas[manzana['id']]['y'][send]
                nuevox = px + distend * (ux / normu)
                nuevoy = py + distend * (uy / normu)

                tmpX.insert(insertend, nuevox)
                tmpY.insert(insertend, nuevoy)
                tipovert.insert(insertend + 1, 'FV')

                insertend = insertend + 1

            tmpX.insert(0, manzana['x'][-1])
            tmpY.insert(0, manzana['y'][-1])
            VManzanas[manzana['id']]['x'] = tmpX
            VManzanas[manzana['id']]['y'] = tmpY

            if insertend < insertinit:
                tipovert[0:insertend] = ['CV'] * (insertend)
                tipovert[insertinit + 1:] = ['CV'] * (len(tipovert) - 1 - insertinit)
            else:
                tipovert[insertinit:insertend] = ['CV'] * (insertend - insertinit)

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

            VVacios[key]['seg'][0] = insertinit
            VVacios[key]['seg'][-1] = insertend


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
                print("No se puede construir una fachada más pequeña que el mínimo establecido en la manzana " + str(
                    mzn['id']))

                fachada = {"x": xx, "y": yy, "long": di, "seg": segmento, "mzn": mzn['id'], "tipo": tipo,
                           "esquina": False}
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
        if fachada['long'] > utils.lmin:
            if fachadas[index]['seg'] != fachadas[index - 1]['seg']:
                if fachadas[index]['esquina'] == False and fachadas[index - 1]['esquina'] == False:
                    if fachadas[index - 1]['tipo'] in ('FM', 'FV', 'CC') and fachadas[index]['tipo'] in ('FM', 'FV', 'CC'):

                        if math.fabs(fachadas[index-1]['long'] - fachadas[index]['long']) > 40:
                            pcas = utils.pmin
                        else:
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
                            [(fachadas[index - 1]['x'], fachadas[index - 1]['y']),
                             (fachadas[index]['x'], fachadas[index]['y']),
                             (fachadas[index + 1]['x'], fachadas[index + 1]['y']), (xx2, yy2),
                             (puntoesquina[0], puntoesquina[1]),
                             (xx, yy)])

                        acas = np.random.normal(28.3898, 4.9329)
                        utils.ajustarAltura(acas, utils.amax, utils.amin)

                        casa = {"mzn": mzn['id'], "longitudcasa": lcas, "profundidadcasa": pcas, "alturacasa": acas/2,
                                "xfachada1": fachadas[index - 1]['x'],
                                "yfachada1": fachadas[index - 1]['y'], "xfachada2": fachadas[index]['x'],
                                "yfachada2": fachadas[index]['y'],
                                "xfachada3": fachadas[index + 1]['x'], "yfachada3": fachadas[index + 1]['y'],
                                "x1": xx, "y1": yy, "x2": xx2, "y2": yy2, "puntoesquina": puntoesquina, "poligono": polygon}

                        fachadas[index - 1].update(esquina=True)
                        fachadas[index].update(esquina=True)
                        casas.insert(index, casa)

    for index, fachada in enumerate(fachadas[:-1]):
        if fachada['long'] > utils.lmin:
            if fachadas[index]['esquina'] == False:
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

                    casa = {"mzn": mzn['id'], "longitudcasa": fachadas[index]['long'], "profundidadcasa": pcas,
                            'alturacasa': acas/2,
                            "xfachada1": fachadas[index]['x'], "yfachada1": fachadas[index]['y'],
                            "xfachada2": fachadas[index + 1]['x'], "yfachada2": fachadas[index + 1]['y'],
                            "x1": xx, "y1": yy, "x2": xx2, "y2": yy2, "poligono": polygon}

                    casas.insert(index, casa)

    mzn['casas'] = casas


def profundidadMuros(muros, manzanas):
    listy = []
    listx = []

    for key, muro in muros.items():
        listy.clear()
        listx.clear()

        for manzana in manzanas:
            if key == manzana['id']:
                seg = utils.getSegmentosMuro(manzanas, key, muro)
                muro['x'].clear()
                muro['y'].clear()

                for index in seg:
                    muro['x'].append(manzana['x'][index])
                    muro['y'].append(manzana['y'][index])

                muro['x'].append(manzana['x'][seg[-1]+1])
                muro['y'].append(manzana['y'][seg[-1]+1])

        if key not in [67, 78, 79]:
            for i, index in reversed(list(enumerate(seg))):
                xvector = manzanas[key]['dX'][index]
                yvector = manzanas[key]['dY'][index]
                perp = [yvector, -xvector]
                mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                vx = np.divide(perp[0], mod) * 12
                vy = np.divide(perp[1], mod) * 12

                if index == seg[0]:
                    xx = muro['x'][0] + vx
                    yy = muro['y'][0] + vy
                    muro['x'].append(xx)
                    muro['y'].append(yy)

                elif index == seg[-1]:
                    xx = muro['x'][-1] + vx
                    yy = muro['y'][-1] + vy
                    muro['x'].append(xx)
                    muro['y'].append(yy)

                    xvector = manzanas[key]['dX'][seg[-1]]
                    yvector = manzanas[key]['dY'][seg[-1]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][i + 1] + vx
                    yy = muro['y'][i + 1] + vy

                    xvector2 = manzanas[key]['dX'][seg[i - 1]]
                    yvector2 = manzanas[key]['dY'][seg[i - 1]]
                    perp2 = [yvector2, -xvector2]
                    mod2 = math.sqrt(perp2[1] ** 2 + perp2[0] ** 2)
                    vx2 = np.divide(perp2[0], mod2) * 12
                    vy2 = np.divide(perp2[1], mod2) * 12
                    xx2 = muro['x'][i - 1] + vx2
                    yy2 = muro['y'][i - 1] + vy2

                    dx1 = manzanas[key]['dX'][seg[i]]
                    dy1 = manzanas[key]['dY'][seg[i]]
                    dx2 = manzanas[key]['dX'][seg[i - 1]]
                    dy2 = manzanas[key]['dY'][seg[i - 1]]

                    puntoesquina = utils.intersect(xx, yy, dx1, dy1, xx2, yy2, dx2, dy2)

                    muro['x'].append(puntoesquina[0])
                    muro['y'].append(puntoesquina[1])

                else:
                    xvector = manzanas[key]['dX'][seg[i]]
                    yvector = manzanas[key]['dY'][seg[i]]
                    perp = [yvector, -xvector]
                    mod = math.sqrt(perp[1] ** 2 + perp[0] ** 2)

                    vx = np.divide(perp[0], mod) * 12
                    vy = np.divide(perp[1], mod) * 12
                    xx = muro['x'][i+1] + vx
                    yy = muro['y'][i+1] + vy

                    xvector2 = manzanas[key]['dX'][seg[i-1]]
                    yvector2 = manzanas[key]['dY'][seg[i-1]]
                    perp2 = [yvector2, -xvector2]
                    mod2 = math.sqrt(perp2[1] ** 2 + perp2[0] ** 2)
                    vx2 = np.divide(perp2[0], mod2) * 12
                    vy2 = np.divide(perp2[1], mod2) * 12
                    xx2 = muro['x'][i-1] + vx2
                    yy2 = muro['y'][i-1] + vy2

                    dx1 = manzanas[key]['dX'][seg[i]]
                    dy1 = manzanas[key]['dY'][seg[i]]
                    dx2 = manzanas[key]['dX'][seg[i-1]]
                    dy2 = manzanas[key]['dY'][seg[i-1]]

                    puntoesquina = utils.intersect(xx, yy, dx1, dy1, xx2, yy2, dx2, dy2)

                    muro['x'].append(puntoesquina[0])
                    muro['y'].append(puntoesquina[1])

    for key, muro in muros.items():
        pol = []
        for x, y in zip(muro['x'], muro['y']):
            pol.append((x,y))

        polygon = Polygon(pol)
        muro.update(poligono=polygon)