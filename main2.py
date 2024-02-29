from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "4879d80cda0f30c587f4cb9039432be1cf9d7de52e3ecc95bec7be6d183662ae"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTE = 30

db = {
    'amith': {
        'username': 'amith',
        'full_name': 'amith kulkarni',
        'email': 'amith@example.com',
        'hashed_password': "$2b$12$5CcicKvdCCTHQKifcE0WuenFUuCeZzQLADiHnduRya3QSlxV3ZDLy",
        'disabled': False
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


 # psw to has
# for hashing the password
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
# to get the token from username and psw
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserDB(**user_data)


def authenticate(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    user_data = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    user_data.update({'expire': expire})

    create_access = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
    return create_access


@app.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        HTTPException(detail='invalid password or username')
    expire_access_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    create_token = create_access_token(
        data={'sub': user.username}, expire_delta=expire_access_token)
    return ({'access_token': create_token, 'token_type': 'bearer'})


# when i login i will get the access_token
# now using that token im trying to get the details of the user..

async def get_current_user(token: str = Depends(oauth2_schema)):
    error = HTTPException(detail='no authorized user')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise error
        token_data = TokenData(username=username)

    except JWTError:
        raise error

    user = get_user(db, username=token_data.username)
    if user is None:
        raise error
    return user


# checking whether the suer is active or not..
# continue tommrow..
