from matplotlib import pyplot as p
import pprint
import copy
import initialize
import build
import utils


manzanas, muros, vacios, fachadas, casas = ([] for i in range(5))


# Paso 0 - Inicializar manzanas, muros y vacios
initialize.initManzanas(initialize.shpma, manzanas)
initialize.initEstructuras(initialize.shpmu, manzanas, muros)
initialize.initEstructuras(initialize.shpva, manzanas, vacios)


# Paso 1 - Insertar vértices en muros/vacios
VManzanas = copy.deepcopy(manzanas)
VMuros = copy.deepcopy(muros)
VVacios = copy.deepcopy(vacios)

for manzana in VManzanas:
    build.preparaEstructura(VManzanas, VMuros, manzana)
    build.preparaEstructura(VManzanas, VVacios, manzana)


# Paso 2 - Rellenar con fachadas
build.rellenaFachadas(VManzanas, VManzanas[21], utils.lmin, utils.lmax, fachadas)

# longtotal= 0
# x,y = ([] for i in range(2))
# for fachada in fachadas:
#     longtotal = fachada['long'] + longtotal
#     print(fachada)
#     x.append(fachada['x'])
#     y.append(fachada['y'])
#     p.plot(x, y)
#
# p.show()
# print(longtotal)


# Paso 3 - Generar las casas a partir de las fachadas
build.generarProfundidad(fachadas, VManzanas[21])

