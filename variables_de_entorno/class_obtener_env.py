from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

class Obtener_Variables_entorno:
    
    """
    Clase para obtener variables de entorno desde un archivo .env
    Attributes:
        ruta_archivo_env (str): La ruta del archivo .env
        _dotenv: El objeto dotenv para cargar las variables de entorno
    """
    
    def __init__(self, ruta_archivo_env):
        """
        Constructor de la clase.
        Parameters:
            ruta_archivo_env (str): La ruta del archivo .env
        """
        self.ruta_archivo_env = ruta_archivo_env
        self._dotenv = load_dotenv(ruta_archivo_env)
        
    def obtener_variable_entorno(self, nombre_clave):
        """
        Método para obtener una variable de entorno específica.
        - Parameters:
            nombre_clave (str): El nombre de la variable de entorno a obtener.
        - Returns:
            str: El valor de la variable de entorno si está definida, o None si no lo está.
        """
        return os.getenv(nombre_clave, default = None)     
    

if __name__ == '__main__':
    
    ruta_archivo_env = ".env"
    configuracion = Obtener_Variables_entorno(ruta_archivo_env)
    clave_api = configuracion.obtener_variable_entorno("GOOGLE_API_KEY")

    print(f"Clave API de Google: {clave_api}")