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

build.reordenarEstructuras(VMuros)
build.reordenarEstructuras(VVacios)
build.preparaMuros(VManzanas, VMuros, mancom)
build.preparaVacios(VManzanas, VVacios, mancom)


# # Paso 2 - Rellenar con fachadas
for manzana in VManzanas:
    if manzana['id'] not in mancom:
        build.rellenaFachadas(VManzanas, manzana)
        build.construirCasas(manzana['fachadas'], manzana['casas'], manzana)

# build.profundidadMuros(VMuros, VManzanas, mancom)

for muro in VMuros.items():
    print(muro)

for vacio in VVacios.items():
    print(vacio)

for manzana in VManzanas:
    print(manzana['nvectores'])
    print(manzana['tipo'])
    print(manzana['x'])
    print(manzana['y'])

# utils.extraerInformacionPNG('../alturascasas/mdttorrianicorrected.png', VManzanas)

# utils.generateOBJmanzanas(VManzanas)
# utils.generateOBJmuros(VMuros, mancom)

for manzana in VManzanas:
    x, y = ([] for i in range(2))
    x = [x for x in manzana['x']]
    y = [y for y in manzana['y']]
    p.plot(x, y)
    for casa in manzana['casas']:
        xx, yy = ([] for i in range(2))
        xx, yy = casa['poligono'].exterior.xy
        p.plot(xx, yy)

p.show()

# Manzana 67 y 79 eliminadas


