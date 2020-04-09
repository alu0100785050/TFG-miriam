from matplotlib import pyplot as p
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
build.rellenaFachadas(VManzanas, VManzanas[9], utils.lmin, utils.lmax, fachadas)

x,y = ([] for i in range(2))
for fachada in fachadas:
   #print(fachada)
    x.append(fachada['x'])
    y.append(fachada['y'])
    p.plot(x, y)

# Paso 3 - Generar las casas a partir de las fachadas
build.generarProfundidad(fachadas, casas, VManzanas[9])

for index, casa in enumerate(casas):
    x, y = casa['poligono'].exterior.xy
    p.plot(x, y)
p.show()

# for index, casa in enumerate(casas[:-1]):
#
#     if utils.doIntersect(casa['poligono'], casas[index+1]['poligono']):
#         newP = utils.mergePolygons(casa['poligono'], casas[index+1]['poligono'])
#         x, y = newP.exterior.xy
#         p.plot(x,y)
#         p.show()

