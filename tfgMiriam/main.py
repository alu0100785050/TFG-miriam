import math
import numpy as np
import shapefile
import copy
from matplotlib import pyplot as p

shpma = shapefile.Reader("../shapefiles/manzana")
shpva = shapefile.Reader("../shapefiles/void")
shpmu = shapefile.Reader("../shapefiles/wall")
manzanas, muros, vacios, fachadas, casas = ([] for i in range(5))
nmanzanas, nmuros, nvacios = (0, 0, 0)
lmin = 45.0207 - 2 * 10.2515
lmax = 45.0207 + 2 * 10.2515
pmin = 18.1218 - 2 * 3.1631
pmax = 18.1218 + 2 * 3.1631
amin = 28.3898 - 2 * 4.9329
amax = 28.3898 + 2 * 4.9329

print("Profundidad")
print(pmin,pmax)
print("LOngitud")
print(lmin,lmax)


# Funciones auxiliares
def calculateVector(p, q, coord):
    x = (q[coord] - p[coord])
    return x


def mostrarManzana(manzana):
    xx = [x for x in manzana['x']]
    yy = [y for y in manzana['y']]
    p.plot(xx, yy)
    p.show()


def ajustarLongitud(lfac):
    if lfac > lmax or lfac < lmin:
        lfac = lmax


def ajustarProfundidad(pcasa):
    if pcasa > pmax or pcasa < pmin:
        pcasa = pmin


# Paso 0 del algoritmo
def initManzanas():
    for index, coord in enumerate(shpma.shapeRecords()):
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

        manzana = {"id": index, "x": xx, "y": yy, "dX": vectoresx, "dY": vectoresy, "dist": distpq,
                   "acumdist": acumdist,
                   "nvectores": nvect, "tipo": tipovert, "verticefachada": vertfach}
        manzanas.append(manzana)


# Paso 0 del algoritmo
def initEstructuras(shpestr):
    threshold = 0.45  # Umbral para comprobar si muro en cierto segmento
    puntos, distend, segin, segen = (0, 0, 0, 0)
    estructura, segmentos, tipos = ([] for i in range(3))
    distinit = 10000

    for man in manzanas:  # Recorrer manzanas
        for index, (x, y) in enumerate(zip(man['x'][:-1], man['y'][:-1])):  # Recorrer coordenadas dentro de cada manzana
            for index2, coord in enumerate(shpestr.shapeRecords()):  # Recorrer estructuras
                for i in coord.shape.points[:]:  # Recorrer coorenadas dentro de cada estructura

                    dist = math.sqrt((x - i[0]) ** 2 + (y - i[1]) ** 2)  # Distancia de muro a vértice anterior
                    dist2 = math.sqrt((i[0] - man['x'][index + 1]) ** 2 + (i[1] - man['y'][index + 1]) ** 2)  # Distancia de muro a vértice siguiente
                    dist3 = math.sqrt((x - man['x'][index + 1]) ** 2 + (y - man['y'][index + 1]) ** 2)  # Distancia de vértice a vértice

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
                                muro = {"mzn": man['id'], "cumdinit": distinit, "cumdend": distend,
                                        "seginit": seginicio,
                                        "segend": segfinal}
                                muros.append(muro)
                                global nmuros
                                nmuros = nmuros + 1
                            elif shpestr == shpva:
                                vacio = {"mzn": man['id'], "cumdinit": distinit, "cumdend": distend,
                                         "seginit": seginicio,
                                         "segend": segfinal}
                                vacios.append(vacio)
                                global nvacios
                                nvacios = nvacios + 1

                            puntos = 0
                            distinit = 10000
                            distend = 0
                            segmentos.clear()
                            estructura.clear()


# Paso 1 del algoritmo - hace que inicio y final del muro sean un vértice
def preparaEstructura(VManzanas, nmanzanas, VEstructuras, mzn):
    tolerancia = 5
    count, nvect = (0, 0)
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

            distinit = linit - VManzanas[mzn['id']]['acumdist'][sinit]  # Distancia inicio muro/inicio vértice
            insertinit = sinit

            if distinit < tolerancia:
                if VEstructuras == VMuros:
                    tipo[sinit] = 'CM'
                elif VEstructuras == VVacios:
                    tipo[sinit] = 'CV'
            else:
                ux = VManzanas[mzn['id']]['dX'][sinit]
                uy = VManzanas[mzn['id']]['dY'][sinit]
                normu = VManzanas[mzn['id']]['dist'][sinit]
                px = VManzanas[mzn['id']]['x'][sinit]
                py = VManzanas[mzn['id']]['y'][sinit]
                nuevox = px + distinit * (ux / normu)
                nuevoy = py + distinit * (uy / normu)

                tmpX.insert(sinit, nuevox)
                tmpY.insert(sinit, nuevoy)

                insertinit = insertinit + 1

                if VEstructuras == VMuros:
                    tipo.insert(insertinit, 'CM')
                elif VEstructuras == VVacios:
                    tipo.insert(insertinit, 'CV')

            distend = lend - VManzanas[mzn['id']]['acumdist'][send]
            insertend = send + (insertinit - sinit)

            if distend < tolerancia:
                if VEstructuras == VMuros:
                    if tipo[send] in ('FV', 'CC'):
                        tipo[send] = 'FM'
                elif VEstructuras == VVacios:
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

                tmpX.insert(send+1, nuevox)
                tmpY.insert(send+1, nuevoy)

                insertend = insertend + 1

                if VEstructuras == VMuros:
                    if tipo[send] == 'CM':
                        tipo.insert(send+1, 'FM')
                    else:
                        tipo.insert(insertend, 'FM')
                elif VEstructuras == VVacios:
                    if tipo[send] == 'CV':
                        tipo.insert(send+1, 'FV')
                    else:
                        tipo.insert(insertend, 'FV')

            tmpX.insert(0, tmpX[-1])
            tmpY.insert(0, tmpY[-1])

            # TONTA AÑADIR AQUI NUEVOS X'S E Y'S POR CADA CM Y CV AÑADIDO TONTA
            if VEstructuras == VMuros:
                tipo[insertinit+1:insertend] = ['CM'] * ((insertend-1) - insertinit)
            elif VEstructuras == VVacios:
                tipo[insertinit+1:insertend-1] = ['CV'] * ((insertend-1) - insertinit)
            # TONTA AÑADIR AQUI NUEVOS X'S E Y'S POR CADA CM Y CV AÑADIDO TONTA

            # Recalcular campos en manzanas
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

            mzn.update(dX=vectoresx, dY=vectoresy, dist=distpq, acumdist=acumdist, nvectores=nvect,
                       tipo=tipo)

            estructura['seginit'] = insertinit
            estructura['segend'] = insertend


# Paso 2 del algoritmo - rellenar manzanas con fachadas
def rellenaFachadas(VManzanas, nmanzanas, mzn):
    nsegmentos = VManzanas[mzn['id']]['nvectores']
    nfachadas, x, y, segmento= (0, 0, 0, 0)
    longitud, tipo = ([] for i in range(2))

    while segmento < nsegmentos:
        nfachadas = nfachadas + 1

        if VManzanas[mzn['id']]['tipo'][segmento] in ('FM', 'FV', 'CC'):
            dp = 0  # Distancia recorrida en segmento
            di = VManzanas[mzn['id']]['dist'][segmento]  # Distancia a completar
            cdp = VManzanas[mzn['id']]['acumdist'][segmento]  # Distancia desde origen

            if di < lmin:  # Si la distancia a completar es menor que la longitud minima requerida
                nfachadas = nfachadas + 1
                xvector = VManzanas[mzn['id']]['dX'][segmento]
                yvector = VManzanas[mzn['id']]['dY'][segmento]
                vx = np.divide(xvector, VManzanas[mzn['id']]['dist'][segmento]) * dp
                vy = np.divide(yvector, VManzanas[mzn['id']]['dist'][segmento]) * dp
                xx = VManzanas[mzn['id']]['x'][segmento] + vx
                yy = VManzanas[mzn['id']]['y'][segmento] + vy
                tipo = VManzanas[mzn['id']]['tipo'][segmento]
                cdp = cdp + di
                print("No se puede construir una fachada más pequeña que el mínimo establecido")

                fachada = {"x": xx, "y": yy, "long": di, "seg": segmento, "mzn": mzn['id'], "tipo": tipo}
                fachadas.insert(nfachadas, fachada)
                segmento = segmento + 1

            else:
                while dp < di:  # Mientras quede distancia para completar en la distancia recorrida

                    lfac = np.random.normal(45.0207, 10.2515)  # Calcular longitud
                    ajustarLongitud(lfac)
                    dist1 = di - dp - lmin

                    if lfac > dist1:  # Si la longitud es mayor que la distancia que queda para rellenar
                        lfac = dist1  # Asignamos esa distancia a la longitud, ya que no se puede rellenar más
                        dist2 = di - dp

                        if lmin <= dist2 <= lmax:  # Si la distancia que queda para rellenar está entre los límites
                            lfac = dist2

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

                    fachada = {"x": xx, "y": yy, "long": lfac, "seg": segmento, "mzn": mzn['id'], "tipo": tipo}
                    fachadas.insert(nfachadas, fachada)

                segmento = segmento + 1

        else:  # Si hay un CM, CV, se guarda una fachada con el tamaño del muro o vacío
            longitud = 0
            seg = segmento

            # if VManzanas[mzn['id']]['tipo'][segmento] == 'CM':
            #     for muro in VMuros:
            #         if muro['mzn'] == mzn['id']:
            #             print("yes")
            #             longitud = muro['cumdend'] - muro['cumdinit']
            #             nfachadas = nfachadas + 1
            #
            #             xx = VManzanas[mzn['id']]['x'][segmento]
            #             yy = VManzanas[mzn['id']]['y'][segmento]
            #             tipo = VManzanas[mzn['id']]['tipo'][segmento]
            #             dp = dp + longitud
            #             cdp = cdp + longitud
            #
            #             fachada = {"x": xx, "y": yy, "long": longitud, "seg": seg, "mzn": mzn['id'], "tipo": tipo}
            #             fachadas.insert(nfachadas, fachada)
            # while VManzanas[mzn['id']]['tipo'][segmento] == 'CM':
            #     segmento = segmento + 1
            #
            # if VManzanas[mzn['id']]['tipo'][segmento] == 'CV':
            #     for vacio in VVacios:
            #         if vacio['mzn'] == mzn['id']:
            #             longitud = vacio['cumdend'] - vacio['cumdinit']
            #             nfachadas = nfachadas + 1
            #
            #             xx = VManzanas[mzn['id']]['x'][segmento]
            #             yy = VManzanas[mzn['id']]['y'][segmento]
            #             tipo = VManzanas[mzn['id']]['tipo'][segmento]
            #             dp = dp + longitud
            #             cdp = cdp + longitud
            #
            #             fachada = {"x": xx, "y": yy, "long": longitud, "seg": seg, "mzn": mzn['id'], "tipo": tipo}
            #             fachadas.insert(nfachadas, fachada)
            #
            # while VManzanas[mzn['id']]['tipo'][segmento] == 'CV':
            #     segmento = segmento + 1

            cdp = VManzanas[mzn['id']]['acumdist'][segmento]
            longitud = VManzanas[mzn['id']]['dist'][segmento]

            nfachadas = nfachadas + 1
            xx = VManzanas[mzn['id']]['x'][segmento]
            yy = VManzanas[mzn['id']]['y'][segmento]
            tipo = VManzanas[mzn['id']]['tipo'][segmento]

            dp = dp + longitud
            cdp = cdp + longitud
            segmento = segmento + 1

            fachada = {"x": xx, "y": yy, "long": longitud, "seg": seg, "mzn": mzn['id'], "tipo": tipo}
            fachadas.insert(nfachadas, fachada)


# Paso 3 del algoritmo - generar casas a partir de las fachadas
def generarCasas(fachadas):
    for index, fachada in enumerate(fachadas):
        if fachada['tipo'] in 'CC' and fachadas[index - 1]['seg'] != fachadas[index]['seg']:
            pcasa = np.random.normal(18.1218, 3.1631)
            ajustarProfundidad(pcasa)
            if (fachadas[index+1]['long'] - pcasa) < lmin:
                pcasa = pmin
                fachadas[index+1]['long'] = fachadas[index+1]['long'] - pcasa
                print(fachadas[index+1]['long'])
            else:
                fachadas[index+1]['long'] = fachadas[index+1]['long'] - pcasa
                print(fachadas[index+1]['long'])

# EJECUCIÓN
# Paso 0 - Inicializar manzanas, muros y vacios
initManzanas()
initEstructuras(shpmu)
initEstructuras(shpva)

# Paso 1 - Insertar vértices en muros/vacios
VManzanas = copy.deepcopy(manzanas)
VMuros = copy.deepcopy(muros)
VVacios = copy.deepcopy(vacios)

for manzana in VManzanas:
    preparaEstructura(VManzanas, nmanzanas, VMuros, manzana)
    preparaEstructura(VManzanas, nmanzanas, VVacios, manzana)

# Paso 2 - Rellenar con fachadas
rellenaFachadas(VManzanas, nmanzanas, VManzanas[0])

# x,y = ([] for i in range(2))
# for fachada in fachadas:
#     print(fachada)
    # x.append(fachada['x'])
    # y.append(fachada['y'])
#     p.plot(x, y)
# p.show()

# Paso 3 - Generar las casas a partir de las fachadas
generarCasas(fachadas)