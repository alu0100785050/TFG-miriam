from matplotlib import pyplot as p
import copy
import initialize
import build
import utils
import pprint
import math
import shapefile

shpma = shapefile.Reader("../shapefilestotal/manzana.shp")
shpva = shapefile.Reader("../shapefilestotal/void.shp")
shpmu = shapefile.Reader("../shapefilestotal/wall.shp")

manzanas = []
muros, vacios = ({} for i in range(2))


# # Paso 0 - Inicializar manzanas, muros y vacios
initialize.inicManzanas(shpma, manzanas)
initialize.inicMuros(shpmu, muros, manzanas)
initialize.inicVacios(shpva, vacios, manzanas)

# # Paso 1 - Insertar vértices en muros/vacios
VManzanas = copy.deepcopy(manzanas)
VMuros = copy.deepcopy(muros)
VVacios = copy.deepcopy(vacios)

mantot, mansen, mancom = utils.descartarManzanasVariasEstructuras(VManzanas, VMuros, VVacios)

p1 = utils.eliminarPuntosDuplicados(VMuros)
p2 = utils.eliminarPuntosDuplicados(VVacios)

for m in p1.items():
    print(m)

for v in p2.items():
    print(v)

# build.reordenarEstructuras(VMuros)
# build.reordenarEstructuras(VVacios)
# build.preparaMuros(VManzanas, VMuros, mancom)
# build.preparaVacios(VManzanas, VVacios, mancom)

# # # # Paso 2 - Rellenar con fachadas
# for manzana in VManzanas:
#     if manzana['id'] not in mancom:
#         build.rellenaFachadas(VManzanas, manzana)
#         build.construirCasas(manzana['fachadas'], manzana['casas'], manzana)

# for manzana in VManzanas:
#     for key, muro in VMuros.items():
#         if manzana['id'] == key:
#             print(manzana['id'])
#             print(manzana['acumdist'])
#             print(manzana['nvectores'])
#             print(manzana['x'])
#             print(manzana['y'])
#             print(manzana['tipo'])
#             print(muro)
#
#     for key, vacio in VVacios.items():
#         if manzana['id'] == key:
#             print(manzana['id'])
#             print(manzana['acumdist'])
#             print(manzana['nvectores'])
#             print(manzana['x'])
#             print(manzana['y'])
#             print(manzana['tipo'])
#             print(vacio)

# build.profundidadMuros(VMuros, VManzanas, mancom)
# utils.extraerInformacionPNG('../alturascasas/mdttorrianicorrected.png', VManzanas)

# utils.generateOBJmanzanas(VManzanas)
# utils.generateOBJmuros(VMuros, mancom)

# xx, yy = ([] for i in range(2))
# for fachada in VManzanas[21]['fachadas']:
#     print(fachada)
#
#     xx.append(fachada['x'])
#     yy.append(fachada['y'])
# p.plot(xx, yy)
#
# for casa in VManzanas[21]['casas']:
#     print(casa)
#     xx, yy = ([] for i in range(2))
#     xx, yy = casa['poligono'].exterior.xy
#     p.plot(xx, yy)

# for manzana in VManzanas:
#     x, y = ([] for i in range(2))
#     x = [x for x in manzana['x']]
#     y = [y for y in manzana['y']]
#     p.plot(x, y)
#     for casa in manzana['casas']:
#         xx, yy = ([] for i in range(2))
#         xx, yy = casa['poligono'].exterior.xy
#         p.plot(xx, yy)
# #
# p.show()

# Manzana 67 y 79 eliminadas


