import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import math

class CalculadoraDistancia:
    R = 6371  # Radio de la tierra en kilómetros

    @staticmethod
    def calcular_distancia(lat1, lon1, lat2, lon2):
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = CalculadoraDistancia.R * c
        return distancia