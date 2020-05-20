from matplotlib import pyplot as p
import copy
import initialize
import build
import utils
import pprint


manzanas, muros, vacios = ([] for i in range(3))


# Paso 0 - Inicializar manzanas, muros y vacios
initialize.initManzanas(initialize.shpma, manzanas)
initialize.initEstructuras(initialize.shpmu, manzanas, muros)
initialize.initEstructuras(initialize.shpva, manzanas, vacios)


# Paso 1 - Insertar vértices en muros/vacios
VManzanas = copy.deepcopy(manzanas)
VMuros = copy.deepcopy(muros)
VVacios = copy.deepcopy(vacios)

mantot, mansen, mancom = utils.descartarManzanasVariasEstructuras(VManzanas, VMuros, VVacios)

for manzana in VManzanas:
    if manzana['id'] not in mancom:
        build.preparaEstructura(VManzanas, VMuros, manzana)
        build.preparaEstructura(VManzanas, VVacios, manzana)


# Paso 2 - Rellenar con fachadas
for manzana in VManzanas:
    if manzana['id'] not in mancom:
        build.rellenaFachadas(VManzanas, manzana, utils.lmin, utils.lmax)
        build.construirCasas(manzana['fachadas'], manzana['casas'], manzana)
#
# build.profundidadMuros(VMuros, VManzanas, mancom)

utils.extraerInformacionPNG('../alturascasas/mdttorrianicorrected.png', VManzanas)

utils.generateOBJmanzanas(VManzanas)
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


