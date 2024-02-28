# this is how to make ur request_example filled with data, so that it looks nice in server..

from fastapi import FastAPI, Body
from typing import Optional,List
from pydantic import BaseModel


app=FastAPI()

# ? ---->   Type:1

# class Item(BaseModel):
#     name:str
#     description:Optional[str]=None
#     price:float
#     tax:Optional[float]=None
    
#     class Config:
#         schema_extra={
#             'example':{
#                 'name':'amith',
#                 "description":"this si male",
#                 "price":16.25,
#                 "tax":25.36,
#             }
#         }
    

# @app.put('/items/{item_id}')
# async def update_item(item_id:int, item:Item):
#     return {'item_id':item_id, 'item':item}


# ! the request data will be filled by default..
"""{
  "name": "amith",
  "description": "this si male",
  "price": 16.25,
  "tax": 25.36
}"""



# ? -------> Type: 2
# from pydantic import Field

# class Item(BaseModel):
#     name:str=Field(...,example='amith')
#     description:Optional[str]=Field(None,example='this is male')
#     price:float=Field(...,example=14.67)
#     tax:Optional[float]=Field(None,example=23.55)

# @app.put('/items/{item_id}')
# async def update_item(item_id:int, item:Item):
#     return {'item_id':item_id, 'item':item}


"""{
  "name": "amith",
  "description": "this is male",
  "price": 14.67,
  "tax": 23.55
}"""





# ? ----------> Type:3

# class Item(BaseModel):
#     name:str
#     description:Optional[str]=None
#     price:float
#     tax:Optional[float]=None

# @app.put('/items/{item_id}')
# async def update_item(item_id:int, item:Item=Body(...,
#                                                   example={
#                                                     'name':'amith',
#                                                     "description":"this si male",
#                                                     "price":16.25,
#                                                     "tax":25.36,
#                                                   }
#                                                   )
#                       ):
#     return {'item_id':item_id, 'item':item}



# ? --------> Type:4

# class Item(BaseModel):
#     name:str
#     description:Optional[str]=None
#     price:float
#     tax:Optional[float]=None

# @app.put('/items/{item_id}')
# async def update_item(item_id:int, 
#                       item:Item=Body(
#                         ...,
#                         examples={
                            
#                             "normal":{
#                                 "summary":"this is normal type",
#                                 "description":"this is normal which works correctly",
#                                 "value":{
#                                     'name':'amith',
#                                     "description":"this is male",
#                                     "price":16.25,
#                                     "tax":25.36,
#                                 },
#                             },
                            
#                             "converted":{
#                                 "summary":"fastapi converts str to int",
#                                 "description":'this is converted description',
#                                 "value":{'name':"foo", "price":"16.25"},
#                             },
                            
#                             "invalid":{
#                                 "summary": "this is invalid this wont run",
#                                 "description": "this is error giving case",
#                                 'value':{'name':"amith", "price":'sixteen rupees'},
#                             },
#                         }
#                         )
#                       ):
    
#     return {'item_id':item_id, 'item':item}