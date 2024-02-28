from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Set
app=FastAPI()

# ? nested list in a field
# class Item(BaseModel):
#     name:str
#     description:str
#     price: float
#     tax:float
#     location: List[str]=[] # we can pass multiple items in a single variable/field..
    

# @app.put('/items/{item_id}')
# async def nested_model(item_id: int, item:Item):
#     results = {'items_id':item_id, 'item':item}
#     return results


"""{
  "name": "string",
  "description": "string",
  "price": 0,
  "tax": 0,
  "location": [],
}"""





# from pydantic import HttpUrl
# from typing import Optional

# class Image(BaseModel):
#     url:HttpUrl
#     name: str


# class Item(BaseModel):
#     name:str
#     description:str
#     price: float
#     tax:float
#     location: List[str]=[]
#     image:List[Image]=None # we can pass n number of objects..
    

# @app.put('/items/{item_id}')
# async def nested_model(item_id: int, item:Item):
#     results = {'items_id':item_id, 'item':item}
#     return results




"""{
  "name": "string",
  "description": "string",
  "price": 0,
  "tax": 0,
  "location": [],
  "image": {
    "url": "string",
    "name": "string"
  }
}"""

# *we can pass n number of objects..
"""{
  "name": "string",
  "description": "string",
  "price": 0,
  "tax": 0,
  "location": [],
 # ? "image": {
 # ?   "url": "https://www.google.com",
 # ?   "name": "google"
 # ?   },
 # ?   {
 # ?   "url": "https://www.facebook.com",
 # ?   "name": "facebook"
 # ? }
}"""




# * Nested models into one another
from fastapi import Body
from pydantic import HttpUrl
from typing import Optional




class Image(BaseModel):
    url:HttpUrl
    name: str


class Item(BaseModel):
    name:str
    description:str
    price: float
    tax:float
    location: List[str]=[]
    image:List[Image]=None # we can pass n number of objects..
    


class Offer(BaseModel):
    name:str
    description:str
    price:float
    items:List[Item]
    
    
@app.put('/items/{item_id}')
async def nested_model(item_id: int, item:Item):
    results = {'items_id':item_id, 'item':item}
    return results

@app.post('/offers')
async def create_offer(offer:Offer=Body(...,embed=True)):
    return offer

@app.post('/images/multiple')
async def multiple_images(image:List[Image]):
    return image

