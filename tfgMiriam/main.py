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

x,y = ([] for i in range(2))
for fachada in fachadas:
    x.append(fachada['x'])
    y.append(fachada['y'])
    p.plot(x, y)


# Paso 3 - Generar las casas a partir de las fachadas
build.generarProfundidad(fachadas, casas, VManzanas[21])
iniciox,inicioy,finx,finy = ([] for i in range(4))
for casa in casas:
    iniciox.append(casa['inicioX'])
    inicioy.append(casa['inicioY'])
    finx.append(casa['finX'])
    finy.append(casa['finY'])
    p.plot(iniciox, inicioy, 'ro')
    p.plot(finx, finy, 'ro')


p.show()

