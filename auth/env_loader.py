import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class EnvLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_env_variables(self):
        print(f"EnvLoader, path .env: {self.file_path}")
        try:
            with open(self.file_path) as f:
                for line in f:
                    key, value = line.strip().split("=")
                    os.environ[key] = value

        except FileNotFoundError:
            print("El archivo .env no se encontró.")
            
        except Exception as e:
            print("Ocurrió un error al cargar las variables de entorno:", e)