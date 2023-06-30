#from .repo_post import post
from .repo_post import PostRepository

# For a new basic set of CRUD or Custom Repository operations you could just do

# from .base import GenericCrudRepository
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = GenericCrudRepository[Item, ItemCreate, ItemUpdate](Item)