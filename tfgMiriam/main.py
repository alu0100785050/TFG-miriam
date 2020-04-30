from matplotlib import pyplot as p
import copy
import initialize
import build
import utils


manzanas, muros, vacios = ([] for i in range(3))


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

for muro in VMuros:
    print(muro)

for vacio in VVacios:
    print(vacio)

# Paso 2 - Rellenar con fachadas
for manzana in VManzanas:
    build.rellenaFachadas(VManzanas, manzana, utils.lmin, utils.lmax)
    build.generarProfundidad(manzana['fachadas'], manzana['casas'], manzana)
    print(manzana['id'], manzana['tipo'])

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

# Problemas con 11, 19, 22, 24, 29, 31


