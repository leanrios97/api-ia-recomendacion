import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import pandas as pd
from bson import ObjectId
from typing import List, Dict, Any

from recommendation.logic.calcularDistancia import CalculadoraDistancia

from concurrent.futures import ThreadPoolExecutor

class ProductDistanceHandler:
    def __init__(self, data: List[Dict[str, Any]], reference_lat: float, reference_long: float):
        self.data = data
        self.reference_lat = reference_lat
        self.reference_long = reference_long
        self.df = None

    def calculate_distance_for_product(self, product):
        id = product['_id']
        lat_pub = product['Coordinates']['Lat']
        long_pub = product['Coordinates']['Long']
        distancia = CalculadoraDistancia.calcular_distancia(
            self.reference_lat, self.reference_long, lat_pub, long_pub
        )
        return {'_id': id, 'distance_km': distancia}

    def calculate_distances(self):
        with ThreadPoolExecutor() as executor:
            distances = list(executor.map(self.calculate_distance_for_product, self.data))
        
        self.df = pd.DataFrame(distances)

    def sort_df(self, column: str):
        try:
            self.df = self.df.sort_values(by=column, ascending=True)
            
        except Exception as e:
            raise ValueError(f'Error al ordenar el dataframe --> sort_df: {e}')

    def filter_by_distance(self, limit_distance: float) -> List[Dict[str, Any]]:
        df_filter = self.df[self.df['distance_km'] <= limit_distance]

        if df_filter.empty:
            return {'message': 'No se encontraron productos para la recomendación'}

        filter_ids = df_filter['_id'].astype(str).tolist()
        filtered_data = [item for item in self.data if str(item['_id']) in filter_ids]

        # Convertir ObjectId a string antes de retornar
        for item in filtered_data:
            if isinstance(item['_id'], ObjectId):
                item['_id'] = str(item['_id'])
            if isinstance(item.get('CategoryId'), ObjectId):
                item['CategoryId'] = str(item['CategoryId'])
            if isinstance(item.get('UserId'), ObjectId):
                item['UserId'] = str(item['UserId'])

        return filtered_data



    def process_data(self, limit_distance: float) -> List[Dict[str, Any]]:
        
        self.calculate_distances()
        self.sort_df('distance_km')
        return self.filter_by_distance(limit_distance)