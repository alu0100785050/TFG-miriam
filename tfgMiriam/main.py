from matplotlib import pyplot as p
import copy
import initialize
import build
import utils
import pprint
import math


manzanas, muros, vacios = ([] for i in range(3))


# Paso 0 - Inicializar manzanas, muros y vacios
initialize.initManzanas(initialize.shpma, manzanas)
# initialize.initEstructuras(initialize.shpmu, manzanas, muros)
# initialize.initEstructuras(initialize.shpva, manzanas, vacios)
#
#
# # Paso 1 - Insertar vértices en muros/vacios
VManzanas = copy.deepcopy(manzanas)
# VMuros = copy.deepcopy(muros)
# VVacios = copy.deepcopy(vacios)
#
# mantot, mansen, mancom = utils.descartarManzanasVariasEstructuras(VManzanas, VMuros, VVacios)
#
# for manzana in VManzanas:
#     if manzana['id'] not in mancom:
#         build.preparaEstructura(VManzanas, VMuros, manzana)
#         build.preparaEstructura(VManzanas, VVacios, manzana)
#
#
# # Paso 2 - Rellenar con fachadas
# for manzana in VManzanas:
#     if manzana['id'] not in mancom:
#         build.rellenaFachadas(VManzanas, manzana, utils.lmin, utils.lmax)
#         build.construirCasas(manzana['fachadas'], manzana['casas'], manzana)
#
# build.profundidadMuros(VMuros, VManzanas, mancom)

muros = {}
for obj in initialize.shpmu.shapeRecords():
    if obj.shape.points:
        for man in VManzanas:
            if man['id'] not in [67, 79]:
                for index, x in enumerate(man['x'][:-1], 0):

                    dist = math.sqrt((man['x'][index] - obj.shape.points[0][0]) ** 2 + (man['y'][index] - obj.shape.points[0][1]) ** 2)
                    dist2 = math.sqrt((obj.shape.points[0][0] - man['x'][index + 1]) ** 2 + (obj.shape.points[0][1] - man['y'][index + 1]) ** 2)
                    dist3 = math.sqrt((man['x'][index] - man['x'][index + 1]) ** 2 + (man['y'][index] - man['y'][index + 1]) ** 2)

                    if dist + dist2 - dist3 <= 0.5:

                        if man['id'] not in muros.keys():
                            muros[man['id']] = {}

                        if obj.record['tipo'] == 1:
                            if 'inicio/fin' not in muros[man['id']].keys():
                                muros[man['id']]['inicio/fin'] = []

                                if 'seginicio' not in muros[man['id']].keys():
                                    muros[man['id']]['seginicio'] = []

                                muros[man['id']]['seginicio'] = index
                                muros[man['id']]['inicio/fin'].append([obj.shape.points[0][0], obj.shape.points[0][1]])

                            else:
                                if 'segfin' not in muros[man['id']].keys():
                                    muros[man['id']]['segfin'] = []

                                muros[man['id']]['segfin'] = index
                                muros[man['id']]['inicio/fin'].append([obj.shape.points[0][0], obj.shape.points[0][1]])

                        else:
                            if 'medio' not in muros[man['id']].keys():
                                muros[man['id']]['medio'] = []

                            muros[man['id']]['medio'].append([obj.shape.points[0][0], obj.shape.points[0][1]])

for muro in muros.items():
    print(muro)

utils.mostrarManzana(VManzanas[40])

# utils.extraerInformacionPNG('../alturascasas/mdttorrianicorrected.png', VManzanas)

# utils.generateOBJmanzanas(VManzanas)
# utils.generateOBJmuros(VMuros, mancom)

# for manzana in VManzanas:
#     x, y = ([] for i in range(2))
#     x = [x for x in manzana['x']]
#     y = [y for y in manzana['y']]
#     p.plot(x, y)
#     for casa in manzana['casas']:
#         xx, yy = ([] for i in range(2))
#         xx, yy = casa['poligono'].exterior.xy
#         p.plot(xx, yy)
#
# p.show()

# Manzana 67 y 79 eliminadas


