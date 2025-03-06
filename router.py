from fastapi import APIRouter
from search.api.search_api import router as search_router

router = APIRouter()

router.include_router(search_router, tags = ['search'])
