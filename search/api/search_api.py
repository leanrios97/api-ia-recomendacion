import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import APIRouter, HTTPException
import json

from auth.auth_verifier import AuthVerifier
from models.userCredentials import UserCredentials
from variables_de_entorno.class_obtener_env import Obtener_Variables_entorno
from api_gemini.class_gemini import configurationGemini
from search.logic.mercadoLibre_service import obtenerProductos
from api_mercado_libre.ml_categorias import obtenerCategorias, procesadorCategorias, idCategoria
from api_mercado_libre.ml_sub_categorias import obtenerSubCategorias, procesadorSubCategorias
from search.data.paises import paises


router = APIRouter()

@router.post('/searchIA')
def searchIA(credentials: UserCredentials, 
             input_search: str):
    try:
        # Crear una instancia de AuthVerifier con las credenciales proporcionadas
        auth_verifier = AuthVerifier(credentials.client_id, credentials.client_secret)
        authorized = auth_verifier.verify_auth_token()

        if authorized:
            try: 
                ruta_archivo_env = ".env"
                configuracion = Obtener_Variables_entorno(ruta_archivo_env)
                clave_api = configuracion.obtener_variable_entorno("GOOGLE_API_KEY")
                
                model = configurationGemini(clave_api)
                categorias = obtenerCategorias()
                listado_categorias = procesadorCategorias(categorias)

                response_categories = model.generate_content(f""""
                    te voy a pasar una serie de pasos que debes de seguir al pie de la letra: 
                    - El usuario va a poner un input
                    - Se te va a brindar una lista de diccionarios con los siguientes valores: 
                    'pais' y 'codigo' estas son keys.
                    - necesito me brindes el dict al pais que fue identificado. 
                    - A tener en cuenta, el usuario puede pasar, el nombre del pais, provincia o estado, ciudad. En caso de no detectarlo ingresar none
                    - dame el nombre del producto dentro del mismo diccionario
                    - en caso de estar el precio, agregalo o completar none
                    - deberas poder identificar a que categoria pertenece el producto en base a la lista que te brindo
                    - limitate a devolver solo el solo el json

                    categorias: {listado_categorias}
                    paises: {paises}. 
                    input: {input_search}
                 Necesito que las keys sean las siguientes: 
                 - pais
                 - codigo
                 - producto
                 - precio
                 - categoria
                    """)
                response_str_categories = response_categories.text
                texto_limpio = response_str_categories.strip('```json\n').strip('``` \n')
                datos = json.loads(texto_limpio)
                site_id = datos['codigo']
                categoria = datos['categoria']
                id_categoria = categoria.split('-')[0]
                nombre_producto = datos['producto']
                
                sub_categorias = obtenerSubCategorias(id_categoria)
                listado_sub_categorias = procesadorSubCategorias(sub_categorias)

                response_sub_categorias = model.generate_content(f""""
                te voy a pasar un listado de que debes de seguir al pie de la letra: 
                1. Se te va a dar un listado de categorias para que entiendas.
                2. Se te va a pasar un producto.
                3. Indicar a que categoria pertenece el producto brindado. 
                4. Al identificar la categoria, devolverlo con el mismo formate en el que se paso cada una. Solamente eso. Encaso de no encontrar devolver el mensaje, producto no encontrado
                categorias: {listado_sub_categorias}. 
                articulo: {nombre_producto}
                Necestio lo devuelvas en el mismo formato que te lo paso: codigo-nombre
                """)

                sub_categoria = response_sub_categorias.text
                id_sub_categoria = sub_categoria.split('-')[0]

                lista_productos = obtenerProductos(nombre_producto, id_sub_categoria, site_id)

                return lista_productos
            except: 
                print("error")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
          
    except HTTPException as http_exception:
        raise http_exception
        
    except Exception as e:
        print("Ocurrió un error durante la autenticación:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")