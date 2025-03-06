import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pydantic import BaseModel

class UserCredentials(BaseModel):
    client_id: str
    client_secret: str
    
    
    