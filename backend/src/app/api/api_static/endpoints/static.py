from typing import Dict

from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=Dict[str, str])
async def get_static() -> Dict[str, str]:
    """
    Static Files API Base Router.
    """
    return {"message": "Static Files API Base Router."}