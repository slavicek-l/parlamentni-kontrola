from fastapi import APIRouter
from . import poslanci, hlasovani, tisky, statistiky, admin

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(poslanci.router, prefix="/poslanci", tags=["poslanci"])
api_router.include_router(hlasovani.router, prefix="/hlasovani", tags=["hlasovani"])
api_router.include_router(tisky.router, prefix="/tisky", tags=["tisky"])
api_router.include_router(statistiky.router, prefix="/statistiky", tags=["statistiky"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
