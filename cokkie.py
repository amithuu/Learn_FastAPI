
#  From this we can learn how to get the data from the api, headers/Network tab # !{request-headers} from the inspect headers..


from fastapi import FastAPI, Cookie, Header
from typing import Optional
app=FastAPI()

@app.get('/items')
async def cookies_headers(
    cookie: Optional[str] = Cookie(None),
    accept_encoding: Optional[str] = Header(None),
    Sec_Ch_Ua_Platform: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    x_token: Optional[str] = Header(None),
    
):
    return{
        'cookie':cookie,
        'accept_encoding': accept_encoding,
        'Sec_Ch_Ua_Platform':Sec_Ch_Ua_Platform,
        'user_agent':user_agent,
        'x_token':x_token,
    }


"""{
  "cookie": null,
  "accept_encoding": "gzip, deflate, br, zstd",
  "Sec_Ch_Ua_Platform": "\"Windows\"",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
  "x_token": null
}"""