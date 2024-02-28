""" 
* if we need to add validation after the declaration of variable, we use {Query, Path from fastapi}
* if we need to add validation at the field declaration inside class itself , we use {Field from pydantic}
"""

from fastapi import FastAPI, Query
from typing import Optional

app=FastAPI()

# ? Without validation on q field..
# @app.get("/items")
# async def validate_item(q:Optional[str]=None):
#     result = {'items': [{'item_id':'foo'},{'item_id': 'bar'}]}
#     if q:
#         result.update({'q':q})
#     return result





# ? With validation on field..
# @app.get('/items')
# async def validate_item(q:Optional[str]=Query(None, min_length=3,max_length=10)): # ?adding validation to field {Q}
#     result = {'items': [{'item_id':'foo'},{'item_id': 'bar'}]}
#     if q:
#         result.update({'q':q})
#     return result


"""
* Below are the types of validators we can use for a field validation...

def Query(  # noqa: N802
    default: Any = Undefined,
     alias: Optional[str] = None,
     title: Optional[str] = None,
     description: Optional[str] = None,
     gt: Optional[float] = None,
     ge: Optional[float] = None,
     lt: Optional[float] = None,
     le: Optional[float] = None,
     min_length: Optional[int] = None,
     max_length: Optional[int] = None,
     regex: Optional[str] = None,
     example: Any = Undefined,
     examples: Optional[Dict[str, Any]] = None,
     deprecated: Optional[bool] = None,
     include_in_schema: bool = True,
     **extra: Any,
"""




# ? With Default value if nothing is given..[even if you dont give any value for q param it will take fixed_value as input..]
# @app.get('/items')
# async def validate_item(q:Optional[str]=Query('fixed_value', min_length=3,max_length=10)): # ?adding validation to field {Q}
#     result = {'items': [{'item_id':'foo'},{'item_id': 'bar'}]}
#     if q:
#         result.update({'q':q})
#     return result




# Want to make a field Required with the validations , then use # *{...}, 
# means without any fixed_value, it will be a #!{required field}
# @app.get('/items')
# # async def validate_item(q:str=None): # this is also required field without validations..
# async def validate_item(q:Optional[str]=Query(..., min_length=3,max_length=10)):
#     result = {'items': [{'item_id':'foo'},{'item_id': 'bar'}]}
#     if q:
#         result.update({'q':q})
#     return result





# ? hidden_query how to hide any query [the q param will not be there in parameters, but in link we need to pass them if needed.. ]
# @app.get('/items')
# async def hidden_query_route(q:str = Query(None, include_in_schema=False)):
#     if q:
#         return {'hidden_query':q}
#     return {'hidden_query':'Not Found'}



# * PATH PARAMETERS AND NUMERIC VALIDATION ON FIELDS..
# from fastapi import Path
# @app.get('/item_validate/{item_id}')
# async def item_validate(*, item_id: int= Path(...,gt=3, lt=100), size:float=Query(...,gt=5.56,lt=10 )):
#     result = ({'item_id': item_id}, {'size': size})
#     return result


""" 
async def item_validate(item_id: int= Query(...,gt=3, lt=100)): # ? {Query} checks only for {length} of the variable not the {value} only in {IF VALUE IS ROUTE PARAMETER CASE}..
async def item_validate(item_id: int= Path(...,gt=3, lt=100), q: str):# ? we are getting error here because after default parameter we cannot use dynamic data
async def item_validate(*, item_id: int= Path(...,gt=3, lt=100)):# ? So we are adding it as kwargs {*,}so it does't make any rules.. 
"""


"""  Field Validations @ Model itself.....  """

from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Body

class Item(BaseModel):
    name:str
    description:Optional[str]=Field(None, title='this is teh description of the item', max_length=300)
    price:float=Field(..., gt=0, description='The Price must be greater than Zero')# here(...) is no default value..
    tax:Optional[float]=None

@app.put('/items/{item_id}')
async def update_item(item_id:int, item:Item=Body(..., embed=True)):
    results = {'item_id':item_id, "item":item}
    return results

