from matplotlib import pyplot as p
import pprint
import copy
import initialize
import build


manzanas, muros, vacios, fachadas, casas = ([] for i in range(5))

global lmin, lmax, pmin, pmax, amin, amax
lmin = 45.0207 - 2 * 10.2515
lmax = 45.0207 + 2 * 10.2515
pmin = 18.1218 - 2 * 3.1631
pmax = 18.1218 + 2 * 3.1631
amin = 28.3898 - 2 * 4.9329
amax = 28.3898 + 2 * 4.9329


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
build.rellenaFachadas(VManzanas, VManzanas[1], lmin, lmax, fachadas)

longtotal= 0
x,y = ([] for i in range(2))
for fachada in fachadas:
    longtotal = fachada['long'] + longtotal
    print(fachada)
    x.append(fachada['x'])
    y.append(fachada['y'])
    p.plot(x, y)

p.show()
print(longtotal)
pprint.pprint(VManzanas[1])


# Paso 3 - Generar las casas a partir de las fachadas
# fix.generarCasas(fachadas, VManzanas[2])
# for casa in casas:
#     print(casa)
