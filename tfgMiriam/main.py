import shapefile
shpma = shapefile.Reader("../shapefiles/manzana")
manzanas = []


def calculateVector(p, q, coord):
    x = 0
    x = (q[coord] - p[coord])
    return x


for coord in shpma.shapeRecords():
    count = 0
    vectoresx = []
    vectoresy = []
    xy = [i for i in coord.shape.points[:]]
    while count < len(xy)-1:
        vx = calculateVector(xy[count], xy[count+1], 0)
        vy = calculateVector(xy[count], xy[count+1], 1)
        vectoresx.append(vx)
        vectoresy.append(vy)
        count = count + 1
    xx = [i[0] for i in xy]
    yy = [i[1] for i in xy]
    manzana = {"x": xx, "y": yy, "dX": vectoresx, "dY": vectoresy}
    manzanas.append(manzana)

print(manzanas[0])