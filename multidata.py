from fastapi import FastAPI, Query
from typing import List
app=FastAPI()


# ? To pass in the multiple data in the query set..
# @app.get('/items')
# async def multi_data(q: List[str] = Query(..., min_length=1, max_length=10)):
#     result = {'items': [{'item_id':'foo'},{'item_id': 'bar'}]}
#     if q:
#         result.update({'q':q})
#     return result


# ? add the more parameters 
# @app.get('/items')
# async def add_more(q:str=Query(None, 
#                                min_length=3, 
#                                max_length=10,
#                                title='this is title',
#                                description='this is q parameter',
#                                alias='item-query')):
#     result = {'items': [{'items':'foo'}, {'items':'bar'}]}
#     if q:
#         result.update({'q':q})
#     return result

# ! http://127.0.0.1:8000/items?q=hello - Error: because teh alias name is different we have given..
# * http://127.0.0.1:8000/items?item-query=hello - Correct



"""# Multiple data in Request Body"""

# from fastapi import Path, Body
# from pydantic import BaseModel
# from typing import Optional

# class Item(BaseModel):
#     name:str
#     description:Optional[str]=None
#     tax:str
#     price:str
    
# class User(BaseModel):
#     username:str
#     first_name : Optional[str]=None
    

# @app.put('/items/{item_id}')
# async def multi_request(
#                         *,
#                         item_id: int = Path(..., gt=0, lt=10),
#                         item:Optional[Item]=None,
#                         user:User = Body(..., embed=True), # this is body embed is used , if u need the output in the # *dict() kind of input{key:value} 
#                         importance: str # ? instead of adding one class for one variable we can use like this..
#                     ):
#     results = {'item_id': item_id}
    
#     if item:
#         results.update({'item':item})
    
#     if user:
#         results.update({'user':user})
        
#     if importance:
#         results.update({'importance':importance})
        
#     return results


