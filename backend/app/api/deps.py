from fastapi import Depends
from ..db import get_db
from ..security import api_key_auth, jwt_auth

def auth_dep():
    # Enforce according to settings
    def _dep(apikey=Depends(api_key_auth), jwt=Depends(jwt_auth)):
        return True
    return _dep

def db_dep():
    return Depends(get_db)
