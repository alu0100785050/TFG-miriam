import numpy as np


class Casa:

    def __init__(self, manzana_=0):
        alnormal = np.random.rand()
        self.longitud = 45.0207 + alnormal * 10.2515
        self.profundidad = 18.1218 + alnormal * 3.1631
        self.altura = 28.3898 + alnormal * 4.9329
        self.manzana = manzana_
