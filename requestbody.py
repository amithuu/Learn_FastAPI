
# ? here we learnt how to  Include/Exclude fields from the models while accessing..[using models and using fields as well]


from typing import List, Optional
from typing_extensions import Literal
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
app = FastAPI()


# ! here i am showing the password as well which i should not show.
# class UserIn(BaseModel):
#     username:str
#     password:str
#     email:EmailStr
#     full_name = str


# @app.post('/users', response_model=UserIn)
# async def create_user(user:UserIn):
#     return user


# * Without showing password in response body..
# class UserBase(BaseModel):
#     username:str
#     email:EmailStr
#     full_name : str

# class UserIn(UserBase):
#     password:str


# @app.post('/users', response_model=UserBase)
# async def create_user(user:UserIn):
#     return user


# ? Include/Exclude fields from the models while accessing..


# class Item(BaseModel):
#     name: str
#     description: Optional[str]
#     price: float
#     tax: float = 10.5  # default value for tax..
#     tags: List[str] = []


# items = {
#     'foo': {'name': 'Foo', 'price': 56.4},
#     'bar': {'name': 'Bar', 'description': 'this is bar', 'price': 56, 'tax': 56.3},
#     'baz': {'name': 'Baz', 'description': None, 'price': 50.3, 'tax': 10.5, 'tags': []},
# }


# @app.get('/items/{item_id}', response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: Literal['foo', 'bar', 'baz']):
#     return items[item_id]


# @app.get('/items/{item_id}/name', response_model=Item, response_model_include={'name', 'description'},)
# async def get_name(item_id:  Literal['foo', 'bar', 'baz']):
#     return items[item_id]


# @app.get('/items/{item_id}/public', response_model=Item, response_model_exclude={'tax'},)
# async def get_name(item_id:  Literal['foo', 'bar', 'baz']):
#     return items[item_id]
