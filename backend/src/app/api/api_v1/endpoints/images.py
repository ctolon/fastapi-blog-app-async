from typing import Any, List, Dict

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, models, schemas
from app.core.media import upload_file, upload_multiple_files, get_all_medias, get_one_media

router = APIRouter()


@router.post('/', response_model=Dict[str, str])
def upload_an_image(
    image: UploadFile = File(...)
    ):
    """
    Upload an image.
    """
    filename = upload_file(image)
    return {'filename': filename}

@router.post('/upload-multi-image', response_model=Dict[str, List[str]])
def upload_multiple_images(
    images: List[UploadFile] = File(...)
    ):
    """
    Upload multiple images.
    """
    filenames = upload_multiple_files(images)
    return {'filenames': filenames}

@router.get('/get-all-images', response_model=schemas.MultiMedia)
async def get_all_images():
    """
    Get all images.
    """
    all_medias = await get_all_medias()
    return JSONResponse(content=all_medias)

@router.get('/get-image', response_model=schemas.SingleMedia)
async def get_image(
    filename: str
):
    """
    Get An Image With provided name.
    """
    
    get_media = await get_one_media(filename)
    if not get_media:
        raise HTTPException(status_code=404, detail=f"Image not found with this name: {filename}")
    response = {"filename": get_media}
    return JSONResponse(content=response)
