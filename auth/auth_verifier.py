import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import HTTPException
from .env_loader import EnvLoader
from .token_manager import TokenManager

class AuthVerifier:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def verify_auth_token(self):
        try:
            env_loader = EnvLoader("auth/.env")
            env_loader.load_env_variables()

            token_manager = TokenManager()
            client_id, secret_key = token_manager.get_tokens()

            # Verificar el token de autenticación
            if (self.client_id == client_id) and (self.client_secret == secret_key):
                print("Autorizado")
                return True
            else:
                raise HTTPException(status_code=401, detail="Unauthorized")

        except Exception as e:
            print("Ocurrió un error al verificar el token de autenticación:", e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        

