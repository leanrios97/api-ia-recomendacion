import requests

def obtenerSubCategorias(id_categoria):
    url_subCategories = f'https://api.mercadolibre.com/categories/{id_categoria}'
    response = requests.get(url_subCategories)

    if response.status_code == 200:
        subCategories = response.json()
        return subCategories
    else:
        print(response.status_code)
        
def procesadorSubCategorias(subCategories):
    try:
        listado_sub_Categorias = []
        
        for i in subCategories['children_categories']:
            idSub = i['id']
            SubName = i['name']
            listado_sub = f'{idSub}-{SubName}'
            listado_sub_Categorias.append(listado_sub)
        
        return listado_sub_Categorias
    except Exception as e:
        print(f"Error al procesar Sub Categorias: {e}")
        
if __name__ == '__main__':
    subCategories = obtenerSubCategorias('MLA1574')
    listado_sub_Categorias = procesadorSubCategorias(subCategories)
    print(listado_sub_Categorias)