from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
# ? this is used for password hashing...
from passlib.context import CryptContext
from typing import Optional

# openssl rand -hex 32
SECRET_KEY = "eaf4ddb09296435f82fbe98d4e737d34de87954afedf50bf52b7691d976ef368"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

db = {
    'amith': {
        'username': 'amith',
        'full_name': 'amith kulkarni',
        'email': 'amith@example.com',
        'hashed_password': "$2b$12$5CcicKvdCCTHQKifcE0WuenFUuCeZzQLADiHnduRya3QSlxV3ZDLy",
        'disabled': False # this is if user is logged-in and access token is expired..
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserDB(User):
    hashed_password: str


# Creating 2 variables for storing the token and the hashing algo..

# using [bcrypt] used to convert plain_text to hashed_password
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
# strong the token in url..
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI()

"""# 'hello'--> "sdjhfcsfcsvusdvsdjcvfcd" [hello in encrypted password..]
# here we pass both plain password and hashed , because we store the encrypted password in database..
# when the user provides the [plain password] using CryptContext we convert it to hashed password
# then we check the both the hashed password are same then only he is authorized.."""


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# we are hashing the password entered by the user..
def get_password_hash(password):
    return pwd_context.hash(password)

# we are getting teh user_data


def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserDB(**user_data)

# authenticate the use..

def authenticate(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


# creating an access token..
def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    # creating duplicate because the original should not change..
    user_data = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    user_data.update({'exp': expire})

    # by passing the user_data, secret_key and algo, we create the secret access_token
    create_accessToken = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
    return create_accessToken


# now we are going to create some functions to get the user_data from the access_token from logged in data 

# to get the current user by access_token
async def get_current_user(token:str = Depends(oauth2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials', headers={'WWW-Authenticate':'Bearer'})
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    
    except JWTError:
        raise credential_exception
    
    user = get_user(db,username=token_data.username)
    if user is None:
        raise credential_exception
    return user

# Checking whether the suer is Active or not using disabled field from User Model..
async def get_current_user_active(current_user:str=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive User')
    return current_user

# now we are going to create some functions to creating access token using username and password while sign-in..
@app.post('/token', response_model=Token)
async def login_for_access_token(form_data :OAuth2PasswordRequestForm=Depends()):
    user = authenticate(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect username and password', headers={'WWW-Authenticate':"Bearer"})
    
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    create_token = create_access_token(data={'sub':user.username} ,expire_delta=access_token_expire)
    return {'access_token': create_token, 'token_type':'bearer'}



@app.get('/users/me', response_model=User)
async def get_user_me(current_user:User=Depends(get_current_user_active)):
    return current_user

@app.get('/users/me/items')
async def get_user_items(current_user:User=Depends(get_current_user_active)):
    return [{'item_id':1,'owner':current_user}]