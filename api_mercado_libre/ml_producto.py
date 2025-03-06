import requests
def obtenerProductos(titulo, id_sub_categoria, site_id = "MLA"):

    # Configurar la URL de la API
    url = f"https://api.mercadolibre.com/sites/{site_id}/search?category_id={id_sub_categoria}&q={titulo}"
    # Enviar la solicitud a la API
    response = requests.get(url)
    # Verificar el código de respuesta
    if response.status_code == 200:
        # Decodificar la respuesta JSON
        data = response.json()
        return data
    else:
        # Imprimir el error
        print(f"Error: {response.status_code}")
    
def procesarDatos(data, datoNecesario='precio'):
    listado_productos = []
    # Imprimir los resultados
    for producto in data["results"]:
        producto_ = f"{producto['title']}-{producto['price']}"
        listado_productos.append(f"${producto['price']}") #{producto['title']}-
    return listado_productos

if __name__ == '__main__':
    data = obtenerProductos('iphone 11 pro 64gb', 'MLA1055')
    lista_productos = procesarDatos(data)
    print(lista_productos)
    
    
    
 # # Imprimir los resultados
    # if datoNecesario.lower() == 'precio':
    #     listado_productos = []
    #     for producto in data["results"]:
    #         print(producto['price'])
    #         listado_productos.append(f"{producto['price']}")
    #         return listado_productos
        
    # elif  datoNecesario.lower() == 'nombre-precio':
    #     listado_productos = []
    #     for producto in data["results"]:
    #         listado_productos.append(f"{producto['title']}-{producto['price']}")
    #     return listado_productos
    
    # elif  datoNecesario.lower() == 'nombre':
    #     listado_productos = []
    #     for producto in data["results"]:
    #         listado_productos.append(f"{producto['title']}")
    #     return listado_productos
    # else: 
    #     return None