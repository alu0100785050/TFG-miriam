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

VMuros = utils.eliminarPuntosDuplicados(VMuros, VManzanas)
VVacios = utils.eliminarPuntosDuplicados(VVacios, VManzanas)

build.reordenarEstructuras(VMuros)
build.reordenarEstructuras(VVacios)

for manzana in VManzanas:
    build.preparaMuros(VManzanas, VMuros, manzana)
    build.preparaVacios(VManzanas, VVacios, manzana)

# Paso 2 - Rellenar con fachadas
for manzana in VManzanas:
    if manzana['id'] not in [67, 78, 79]:
        build.rellenaFachadas(VManzanas, manzana)
        build.construirCasas(manzana['fachadas'], manzana['casas'], manzana)

# for manzana in VManzanas:
#     for key, muro in VMuros.items():
#         if manzana['id'] == key:
#             print("MANZANAAAAAAAA---------AQUIIIIIIIII------")
#             print(manzana['id'])
#             print(manzana['x'])
#             print(manzana['y'])
#             print(manzana['tipo'])
#             print('DISTANCIA ACUMULADA ' + str(manzana['acumdist']))
#             print('NUMERO DE VECTORES ' + str(manzana['nvectores']))
#             print('VECTORES X ' + str(manzana['dX']))
#             print('VECTORES Y ' + str(manzana['dY']))
#             print("MUROOOOOOO------AQUIIIIIII--------")
#             print(muro['x'])
#             print(muro['y'])
#             print(muro['orden'])
#             print(muro['acumdist'])
#             print(muro['seg'])

build.profundidadMuros(VMuros, VManzanas)

for manzana in VManzanas:
    for key, muro in VMuros.items():
        if manzana['id'] == key:
            print("MUROOOOOOO {} ------AQUIIIIIII--------".format(key))
            print(muro['x'])
            print(muro['y'])
            print(muro['orden'])
            print(muro['acumdist'])
            print(muro['seg'])

utils.extraerInformacionPNG('../alturascasas/mdttorrianicorrected.png', VManzanas)
utils.generateOBJmanzanas(VManzanas)
utils.generateOBJmuros(VMuros, mancom)

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


