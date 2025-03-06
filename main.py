from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from models.userCredentials import UserCredentials
from variables_de_entorno.class_obtener_env import Obtener_Variables_entorno
from api_gemini.class_gemini import configurationGemini
from api_mercado_libre.ml_categorias import obtenerCategorias, procesadorCategorias, idCategoria
from api_mercado_libre.ml_sub_categorias import obtenerSubCategorias, procesadorSubCategorias
from api_mercado_libre.ml_producto import obtenerProductos, procesarDatos
from api_dolar.api_dolar import api_dolar, devolucionPrecio

from auth.auth_verifier import AuthVerifier

from recommendation.data.mongoDbHandler import MongoDBHandler
from recommendation.logic.productDistance import ProductDistanceHandler

from router import router as app_routing  


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', tags=['Welcome'])
def hello_api():
  return "api funcionando!!!"

      
@app.post("/auth2")
def authentication(credentials: UserCredentials):
  try:
        # Crear una instancia de AuthVerifier con las credenciales proporcionadas
        auth_verifier = AuthVerifier(credentials.client_id, credentials.client_secret)
        authorized = auth_verifier.verify_auth_token()

        if authorized:
            return {"detail": "Authorized"}
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
          
  except HTTPException as http_exception:
      raise http_exception
    
  except Exception as e:
      print("Ocurrió un error durante la autenticación:", e)
      raise HTTPException(status_code=500, detail="Internal Server Error")



@app.post('/recomendacionPrecio', tags=['Ventas'])
async def recomendacionPrecio(credentials: UserCredentials, productoUser):

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
            
              response_categories = model.generate_content(f"""Tengo las siguientes categorias: {listado_categorias}. 
                                  A que categoria pertenece el siguiente articulo: {productoUser}
                                  Necesito me des la devolucion con la categoria como esta en la lista que te paso.
                                  Ej: MLA1953-Otras categorías
                                  Si no se encontro el producto, devolver mensaje diciendo: Intenta ingresar otro producto o
                                  una mejor descripción.""")
    
              response_str_categories = response_categories.text
              print(response_str_categories)
            
            
              id_categoria = idCategoria(response_str_categories)
              # Sub categorias.
              subCategories = obtenerSubCategorias(id_categoria)
              listado_sub_Categorias = procesadorSubCategorias(subCategories)
              
              response_sub_categories = model.generate_content(f"""Tengo las siguientes categorias: {listado_sub_Categorias}. 
                                            A que categoria pertenece el siguiente articulo: {productoUser}
                                            Necesito me des la devolucion con la categoria como esta en la lista que te paso.
                                            Ej: MLA1953-Otras categorías
                                            Si no se encontro el producto, devolver mensaje diciendo: Intenta ingresar otro producto o
                                            una mejor descripción.""")
              
              response_str_sub_categories = response_sub_categories.text
              id_sub_categoria = idCategoria(response_str_sub_categories)
              
              
              # Obtencion del producto. 
              data = obtenerProductos(productoUser, id_sub_categoria)
              lista_productos = procesarDatos(data)
              
              response_recomendacion_precio = model.generate_content(f"""Te paso un listado de precios: {lista_productos}. 
                                            te pido me des el promedio del los precios
                                            con el siguiente formato: 
                                            - Precio Sugerido de publicacion: """)
              
              response_str_recomendacion_precio = response_recomendacion_precio.text
              
              precio = devolucionPrecio(response_str_recomendacion_precio)
              
              return precio
            
            except Exception as e: 
              print(f"Error en el endpoint: {e}")
            
            
            
          else:
              raise HTTPException(status_code=401, detail="Unauthorized")
            
  except HTTPException as http_exception:
      raise http_exception
    
  except Exception as e:
      print("Ocurrió un error durante la autenticación:", e)
      raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post('/recomentation', tags=['Recomendación'])
async def recomentation(credentials: UserCredentials, 
                  typePublication: int, 
                  namePublication: str,
                  user_lat: float, 
                  user_long: float):
# Validar que typePublication esté dentro de los valores permitidos
  if typePublication not in [0, 1]:
      raise HTTPException(status_code=400, detail="Tipo de publicación inválido. Debe ser 0 (compra) o 1 (venta).")

  # Validar las coordenadas de latitud y longitud
  if not (-90 <= user_lat <= 90):
      raise HTTPException(status_code=400, detail="Latitud inválida. Debe estar entre -90 y 90.")
      
  if not (-180 <= user_long <= 180):
      raise HTTPException(status_code=400, detail="Longitud inválida. Debe estar entre -180 y 180.")
  
  try:
      auth_verifier = AuthVerifier(credentials.client_id, credentials.client_secret)
      authorized = auth_verifier.verify_auth_token()

      if authorized:
        try: 
          mongo_handler = MongoDBHandler()
          publications = mongo_handler.get_publications(typePublication, namePublication)
          
          mongo_handler.close_connection()
          handler = ProductDistanceHandler(publications, user_lat, user_long)
          limit_distance = 500
          result = handler.process_data(limit_distance)
          print(result)
          
          return result
        
        except Exception as e: 
          print(f"Error en el endpoint: {e}")
        
      else:
          raise HTTPException(status_code=401, detail="Unauthorized")
            
  except HTTPException as http_exception:
      raise http_exception
    
  except Exception as e:
      print("Ocurrió un error durante la autenticación:", e)
      raise HTTPException(status_code=500, detail="Internal Server Error")

app.include_router(app_routing)