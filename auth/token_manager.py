import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TokenManager:
    def __init__(self):
        pass

    def get_tokens(self):
        client_id = os.environ.get('client_id')
        secret_key = os.environ.get('client_secret')

        if client_id and secret_key:
            print("Se obtuvieron los tokens correctamente.")
            return client_id, secret_key
        else:
            print("No se pudieron obtener los tokens.")
            return None, None