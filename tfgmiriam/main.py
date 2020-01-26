from ciudad import Ciudad
import shapefile


# Creación ciudad
laguna = Ciudad("../shapefiles/manzana")

# for i in laguna:
#     i.setEstructura("../shapefiles/wall")
#     i.setEstructura("../shapefiles/void")
#     i.rellenarManzana()
#     i.mostrarVacios()
#     i.mostrarMuros()

laguna[29].rellenarManzana()

