def api_dolar():
    import requests
    
    responseDolarBlue = requests.get("https://dolarapi.com/v1/dolares/blue")

    if responseDolarBlue.status_code == 200:
        dolarBlue = responseDolarBlue.json()
        dolarBlueVenta = dolarBlue['venta']
        
        return dolarBlueVenta
    else:
        print(responseDolarBlue.status_code)
        
def devolucionPrecio(precio):
    try: 
        valor = precio.split("$")[1]
        valor_int = int(valor.replace(",", ""))
        dolar = api_dolar()
        precioDolar = round(valor_int / dolar, 2)
        dict_valor = {'precio_arg': valor_int, 'precio_usd': precioDolar} 
        
        return dict_valor
    
    except Exception as e:
        return "No hay recomendación"