import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from variables_de_entorno.class_obtener_env import Obtener_Variables_entorno

from pymongo import MongoClient
from typing import List, Dict, Any
from bson import ObjectId


class MongoDBHandler:
    def __init__(self, ruta_archivo_env=".env"):
        self.config = Obtener_Variables_entorno(ruta_archivo_env)
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        try:
            conn = self.config.obtener_variable_entorno("connectionStringMongo")
            if not conn:
                raise ValueError("No se encontró la cadena de conexión de MongoDB en las variables de entorno")
            
            self.client = MongoClient(conn)
            self.db = self.client['Atawall']
            self.collection = self.db['PublicationEntity']
            
        except Exception as e:
            NameError(f'Error al establecer conexion: {e}')

    def get_publications(self, type_: int, name: str) -> List[Dict[str, Any]]:
        compra = 0
        venta = 1

        if type_ == compra: 
            query = {"Type": venta, "Name": {"$regex": name, "$options": "i"}}
            publications = list(self.collection.find(query))
            
        elif type_ == venta: 
            query = {"Type": compra, "Name": {"$regex": name, "$options": "i"}}
            publications = list(self.collection.find(query))
            
        else: 
            raise NameError(f'Parámetro fuera de rango, get_publicacion --> type_: {type_}')

        # Convertir los ObjectId a string antes de devolver los resultados
        for publication in publications:
            publication['_id'] = str(publication['_id'])

        return publications

    def close_connection(self):
        if self.client:
            self.client.close()

