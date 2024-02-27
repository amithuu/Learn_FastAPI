from fastapi import FastAPI
app = FastAPI()


# @app.get("/")
# async def root():
#     return {'message': 'hi i am learning fastapi'}


# @app.post("/")
# async def post():
#     return {'message': 'this is post request'}


# @app.put("/")
# async def put():
#     return {'message': 'this is put request'}

# # Using Parameters


# @app.get('/users')
# async def list_users():
#     return {'message': 'this is users list'}


# # so this should be here..
# @app.get('/users/me')
# async def get_me():
#     return {'user': 'this is current user'}


# @app.get('/users/{user_id}')
# async def get_user(user_id: str):
#     return {'item': user_id}

# # type casting it to the output we need
# # @app.get('/items/item_id')
# # async def item(item_id:int):
# #     return {'item': item_id}

# # @app.get('/users/me')
# # async def get_me():
# #     return {'user': 'this is current user'}
# # # ? o/p: because the route is not able to find the correct route as we have one dynamic route above it, soo we need to write the static route first then write dynamic route..
# # # {
# # #   "item": "me"
# # # }


# # ! Creating own type variables

# from enum import Enum
# class FoodEnum(str, Enum):
#     fruits = 'fruits'
#     vegetables = 'vegetables'
#     dairy = 'dairy'


# @app.get('/foods/{food_name}')
# async def get_food(food_name: FoodEnum):
#     # type 1 of checking the input using FoodEnum class based..
#     if food_name == FoodEnum.vegetables:
#         return {
#             'food_name': food_name,
#             'message': 'you are healthy'
#         }

#     # type 3 using the value written by user..
#     elif food_name.value == 'fruits':
#         return {
#             'food_name': food_name,
#             'message': 'ypu are healthy, but sweet'
#         }

#     return {
#         'food_name': food_name,
#         'message': 'i like dairy products'
#     }


# # Query parameters...[which is passed as query in the parameters.. dynamically]

# fake_db = [{'item_name': 'foo'}, {'item_name': 'bar'}, {'item_name': 'baz'}]

# @app.get('/items')
# async def get_items(skip: int=0, limit:int=10):
#     return fake_db[skip:skip+limit]


# # Optional Query Parameters
# from typing import Optional
# @app.get('/items/{item_id}')
# async def list_item(item_id: str, q: Optional[str] = None):
#     if q:
#         return {'item_id': item_id, 'q':q}

#     return {'item_id': item_id}


# # ? Querying with the 3rd parameter

# @app.get('/items/{item_id}')
# async def get_item(item_id: str, q: Optional[str] = None, short: bool=False):
#     item = {'item_id': item_id}
#     if q:
#         item.update({'q': q})

#     if short:
#         item.update(
#             {'description': 'there is an short in the item so getting this'}
#                     )
#     return item

# # ?ex: programme to get the  user_id and his item

# @app.get('/users/{user_id}/.items/{item_id}')
# async def get_user_item(user_id: str, item_id:str, q: Optional[str]=None, short:bool=False):
#     item = {'user':user_id, 'item':item_id}
#     if q:
#         item.update({'q':q})

#     if short:
#         item.update({'description':'there is one item short for this user'})

#     return item


# # ?in the parameter we have given only one param  item_id , but to get the data we need other fields as well required how to do it,,
# # ? without passing in parameter

# @app.get('/items/{item_id}')
# async def get_item(item_id: str,sample_query_param:str, q: Optional[str] = None, short: bool=False):
#     item = {'item_id': item_id, 'sample_query_param': sample_query_param}
#     if q:
#         item.update({'q': q})

#     if short:
#         item.update(
#             {'description': 'there is an short in the item so getting this'}
#                     )
#     return item


# ! learn about Request Body
# ? passing the data into the database using post request..

# ? as like models in django we create a class here 
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    # description: str # to make any field option..
    description: Optional[str] = None # to make any field option..
    price: float
    # tax: float
    tax: Optional[float] = None

# ?create api
@app.post('/cerate/items')
async def create_item(item:Item):
    return item.dict()


# ?create api with add in data and calculation   
@app.post('/cerate/items/add-ons')
async def create_item_with_add_in_data(item:Item):
    item_dict = item.dict() # converting to dictionary
    
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
        
    return item_dict


        
# ?updating the data or creating the data with {put} request,.,
@app.put('/items/{item_id}')
async def create_item_with_put(item:Item, item_id:int):
    return {'item':item_id, **item.dict()}


# ?we can add extra {query param} as well here
# @app.put('/items/{item_id}')
# async def create_item_with_put(item:Item, item_id:int, q:Optional[str]=None):
#     result = {'item':item_id, **item.dict()}
#     if q:
#         result.update({'q':q})
#     return result