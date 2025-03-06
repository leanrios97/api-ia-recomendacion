import requests


def obtenerCategorias():
    url = "https://api.mercadolibre.com/sites/MLA/categories"
    response = requests.get(url)

    if response.status_code == 200:
        categories = response.json()
        return categories
    else:
        print(response.status_code)
        
def procesadorCategorias(categories):
    try: 
        listado_categorias = []
        for x in categories:
            cat_unidas = f"{x['id']}-{x['name']}"
            listado_categorias.append(cat_unidas)
            
        return listado_categorias
    
    except Exception as e:
        print(f"No se puedo procesar categorias: {e}")
    
def idCategoria(response_str_categories):
    try: 
        id_categoria = response_str_categories.split('-')[0]
        return id_categoria
    
    except Exception as e:
        print(f"No se puede devolver el ID Categoria: {e}")



if __name__ == '__main__':
    categories = obtenerCategorias()
    listado_categorias = procesadorCategorias(categories)
    print(listado_categorias)