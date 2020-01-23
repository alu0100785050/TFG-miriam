from ciudad import Ciudad
from casa import Casa

# Creación ciudad
laguna = Ciudad("../shapefiles/manzana")

# laguna[6].rellenar()

laguna[6].setexcepcion("../shapefiles/void")
laguna[6].setexcepcion("../shapefiles/wall")

print(laguna[6].esquinas)
print(laguna[6].longitud)
print(laguna[6].getnumesq())