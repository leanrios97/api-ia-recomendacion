import requests
import json

def obtenerProductos(titulo, id_sub_categoria, site_id):
    # Configurar la URL de la API
    url = f"https://api.mercadolibre.com/sites/{site_id}/search?category_id={id_sub_categoria}&q={titulo}"
    
    # Enviar la solicitud a la API
    response = requests.get(url)
    
    # Verificar el código de respuesta
    if response.status_code == 200:
        # Decodificar la respuesta JSON
        data = response.json()

        # Guardar los datos en un archivo JSON
        with open('datos.json', 'w') as outfile:
            json.dump(data, outfile)

        # Crear lista de productos y mostrarlos
        productos_json = []
        for producto in data["results"]:
            productos_json.append(producto)
            print(producto)
        
        # Retornar los productos
        return productos_json
    else:
        # Imprimir el error
        print(f"Error: {response.status_code}")
