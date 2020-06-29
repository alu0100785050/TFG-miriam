import copy
import initialize
import build
import utils
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

build.profundidadMuros(VMuros, VManzanas)

utils.extraerInformacionPNGmanzanas('../alturascasas/mdttorrianicorrected.png', VManzanas)
utils.extraerInformacionPNGmuros('../alturascasas/mdttorrianicorrected.png', VMuros)
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

##CALCULO CASAS##
#NO GENERADAS
casasnogeneradas = 0
for manzana in VManzanas:
    for fachada in manzana['fachadas']:
        if fachada['long'] < utils.lmin:
            casasnogeneradas = casasnogeneradas + 1

print('casas no generadas ' + str(casasnogeneradas))

# MAL GENERADAS
casasmalgeneradas = 0
casasmalgeneradasextra = 0
for manzana in VManzanas:

    casasmal = utils.getCasasMalGeneradas(manzana)
    casasmalgeneradas = casasmalgeneradas + casasmal

    if manzana['id'] in [67, 78, 79]:
        for casa in manzana['casas']:
            casasmalgeneradasextra = casasmalgeneradasextra + 1

print('casas mal generadas ' + str(casasmalgeneradas) + ' de las cuales 67 78 y 79 suman ' + str(casasmalgeneradasextra))

# #BIEN GENERADAS
casasgeneradas = 0
for manzana in VManzanas:
    for casa in manzana['casas']:
        casasgeneradas = casasgeneradas + 1

casasbiengeneradas = casasgeneradas - (casasmalgeneradas + casasmalgeneradasextra)
print('casas generadas totales ' + str(casasgeneradas))
print('casas bien generadas' + str(casasbiengeneradas))
