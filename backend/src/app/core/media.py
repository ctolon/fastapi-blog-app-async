import shutil
import os
import string
import random
import pathlib
import glob
from typing import List, Union

from fastapi import UploadFile, File

from app.core.config import settings

if not pathlib.Path(settings.MEDIA_DIR).exists():
    pathlib.Path(settings.MEDIA_DIR).mkdir(parents=True, exist_ok=False)
        
def _random_filename_generator(media: UploadFile = File(...)) -> str:
    """Generate random filename for media."""
    
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(media.filename.rsplit('.', 1))
    return filename


def upload_file(media: UploadFile = File(...), new_filename: str = None) -> str:
    """Upload a file to the media directory."""
    
    media_filename = _random_filename_generator(media) if new_filename is None else new_filename
    with open(f'{settings.MEDIA_DIR}/{media_filename}', 'wb+') as buffer:
        shutil.copyfileobj(media.file, buffer)
    return media_filename


def upload_multiple_files(files: List[UploadFile] = File(...)) -> List[str]:
    """Upload multiple files to the media directory."""
    
    filenames = []
    for f in files:
        filename = upload_file(f)
        filenames.append(filename)
    return filenames

async def get_all_medias_with_path():
    """Get all media files with their path."""
    
    return {"filenames": [x for x in glob.glob(f'{settings.MEDIA_DIR}/*')]}

async def get_all_medias():
    """Get all media files without path."""
    
    return {"filenames": [os.path.basename(x) for x in glob.glob(f'{settings.MEDIA_DIR}/*')]}

async def get_one_media_with_path(filename: str) -> Union[str, None]:
    """Get one media file with the given filename and returns filename with path"""
    
    media = [x for x in glob.glob(f'{settings.MEDIA_DIR}/{filename}')]
    if media:
        return media[0]
    else:
        return None

async def get_one_media(filename: str) -> Union[str, None]:
    """Get one media file with the given filename and returns filename without path."""
    
    media = [os.path.basename(x) for x in glob.glob(f'{settings.MEDIA_DIR}/{filename}')]
    if media:
        return media[0]
    else:
        return None
    