import math
import numpy as np
import shapefile
from matplotlib import pyplot as p

shpma = shapefile.Reader("../shapefiles/manzana")
shpva = shapefile.Reader("../shapefiles/void")
shpmu = shapefile.Reader("../shapefiles/wall")
manzanas, muros, vacios, fachadas = ([] for i in range(4))
nmanzanas, nmuros, nvacios, nfachadas = (0, 0, 0, 0)
lmin = 45.0207 - 2 * 10.2515
lmax = 45.0207 + 2 * 10.2515


# Funciones auxiliares
def calculateVector(p, q, coord):
    x = (q[coord] - p[coord])
    return x


def mostrarManzana(manzana):
    xx = [x for x in manzana['x']]
    yy = [y for y in manzana['y']]
    p.plot(xx, yy)
    p.show()


def ajustar(lfac):
    if lfac > lmax or lfac < lmin:
        lfac = lmin


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
    tolerancia = 0.5
    count, nvect = (0, 0)
    vectoresx, vectoresy, distpq, tipovert, vertfach = ([] for i in range(5))
    acumdist = [0]
    for estructura in VEstructuras:
        if estructura['mzn'] == mzn['id']:
            # Guardar información
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
                if VEstructuras == muros:
                    tipo[sinit] = 'CM'
                elif VEstructuras == vacios:
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
                if VEstructuras == muros:
                    tipo.insert(sinit, 'CM')
                elif VEstructuras == vacios:
                    tipo.insert(sinit, 'CV')
                insertinit = insertinit + 1

            distend = lend - VManzanas[mzn['id']]['acumdist'][send]
            insertend = send

            if distend < tolerancia:
                if VEstructuras == muros:
                    if tipo[insertend] in ('FV', 'CC'):
                        tipo[insertend] = 'FM'
                elif VEstructuras == vacios:
                    if tipo[insertend] in ('FM', 'CC'):
                        tipo[insertend] = 'FV'
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

                if VEstructuras == muros:
                    if tipo[send] == 'CM':
                        tipo[send+1] = 'FM'
                    else:
                        tipo[send] = 'FM'
                elif VEstructuras == vacios:
                    if tipo[send] == 'CV':
                        tipo[send+1] = 'FV'
                    else:
                        tipo[send] = 'FV'

                insertend = insertend + 1

            tmpX.insert(0, tmpX[-1])
            tmpY.insert(0, tmpY[-1])
            if VEstructuras == muros:
                tipo[insertinit:insertend - 1] = ['CM'] * ((insertend - 1) - insertinit)
            elif VEstructuras == vacios:
                tipo[insertinit:insertend - 1] = ['CV'] * ((insertend - 1) - insertinit)

            # Recalcular campos en manzanas
            VManzanas[mzn['id']]['x'] = tmpX
            VManzanas[mzn['id']]['y'] = tmpY
            while count < len(tmpX) - 1:
                x = (VManzanas[mzn['id']]['x'][count] - VManzanas[mzn['id']]['x'][count + 1])
                y = (VManzanas[mzn['id']]['y'][count] - VManzanas[mzn['id']]['y'][count + 1])
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
    segmentos, longitud, tipo = ([] for i in range(3))

    while segmento < nsegmentos-1:
        nfachadas = nfachadas + 1
        segmentos.append(nfachadas)

        if VManzanas[mzn['id']]['tipo'][segmento] in ('FM', 'FV', 'CC'):
            dp = 0  # Distancia recorrida en segmento
            di = VManzanas[mzn['id']]['dist'][segmento]  # Distancia a completar
            cdp = VManzanas[mzn['id']]['acumdist'][segmento]  # Distancia desde origen

            if di < lmin:  # Si la distancia a completar es menor que la longitud minima requerida
                nfachadas = nfachadas + 1
                x = VManzanas[mzn['id']]['x'][segmento]
                y = VManzanas[mzn['id']]['y'][segmento]
                tipo = VManzanas[mzn['id']]['tipo'][segmento]
                cdp = cdp + di
                print("No se puede construir una fachada más pequeña que el mínimo establecido")

                fachada = {"x": x, "y": y, "long": di, "seg": segmento, "mzn": mzn['id'], "tipo": tipo}
                fachadas.insert(nfachadas, fachada)
                segmento = segmento + 1

            else:
                while dp < di:  # Mientras quede distancia para completar en la distancia recorrida

                    lfac = np.random.normal(45.0207, 10.2515)  # Calcular longitud
                    ajustar(lfac)
                    dist1 = di - dp - lmin

                    if lfac > dist1:  # Si la longitud es mayor que la distancia que queda para rellenar
                        lfac = dist1  # Asignamos esa distancia a la longitud, ya que no se puede rellenar más
                        dist2 = di - dp

                        if lmin <= dist2 <= lmax:  # Si la distancia que queda para rellenar está entre los límites
                            lfac = dist2

                    nfachadas = nfachadas + 1
                    x = VManzanas[mzn['id']]['x'][segmento]
                    y = VManzanas[mzn['id']]['y'][segmento]
                    tipo = VManzanas[mzn['id']]['tipo'][segmento]
                    dp = dp + lfac

                    fachada = {"x": x, "y": y, "long": lfac, "seg": segmento, "mzn": mzn['id'], "tipo": tipo}
                    fachadas.insert(nfachadas, fachada)

                segmento = segmento + 1

        else:  # Si hay un CM, CV, se guarda una fachada con el tamaño del muro o vacío
            longtotal = 0
            seg = segmento
            while VManzanas[mzn['id']]['tipo'][segmento] in ('CV', 'CM'):
                longtotal = VManzanas[mzn['id']]['dist'][segmento+1] + longtotal
                cdp = VManzanas[mzn['id']]['acumdist'][segmento]

                nfachadas = nfachadas + 1
                x = VManzanas[mzn['id']]['x'][segmento]
                y = VManzanas[mzn['id']]['y'][segmento]
                tipo = VManzanas[mzn['id']]['tipo'][segmento]
                cdp = cdp + longtotal
                segmento = segmento + 1

            fachada = {"x": x, "y": y, "long": longtotal + VManzanas[mzn['id']]['dist'][segmento+1], "seg": seg, "mzn": mzn['id'], "tipo": tipo}
            fachadas.insert(nfachadas, fachada)

    VManzanas[mzn['id']]['verticefachada'] = segmentos


# EJECUCIÓN
# Paso 0 - Inicializar manzanas, muros y vacios
initManzanas()
initEstructuras(shpmu)
initEstructuras(shpva)

# Paso 1 - Insertar vértices en muros/vacios
VManzanas = manzanas
VMuros = muros
VVacios = vacios

for manzana in VManzanas:
    preparaEstructura(VManzanas, nmanzanas, VMuros, manzana)
    preparaEstructura(VManzanas, nmanzanas, VVacios, manzana)

# Paso 2 - Rellenar con fachadas
rellenaFachadas(VManzanas, nmanzanas, VManzanas[23])
longtotal = 0

for fachada in fachadas:
    print(fachada)
    longtotal = fachada['long'] + longtotal
#     # print(fachada, file=open("output.txt", "a"))


print(VManzanas[23]['acumdist'])
print(VManzanas[23]['dist'])
print(longtotal)
print(VVacios)
print(VMuros)
