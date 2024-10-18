import jwt
import datetime
import bcrypt

from config import JWT_SECRET_KEY, ALGORITHM, DEFAULT_EXPIRED_TIME
from database import create_tables, add_user_in_db, check_exist_db

def create_token(username: str, expired_time: None | datetime.timedelta = None) -> str:
    sub = {'username' : username}
    if expired_time:
        exp = datetime.datetime.now(datetime.timezone.utc) +  expired_time
    else:
        exp = datetime.datetime.now(datetime.timezone.utc) + DEFAULT_EXPIRED_TIME
    user_data = sub.copy()
    user_data.update({'exp': exp})
    token = jwt.encode(payload=user_data, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> str:
    sub = jwt.decode(jwt=token, key=JWT_SECRET_KEY, algorithms= ALGORITHM)
    return sub.get('username')

def check_password(password_from_form, password_from_db):
    return bcrypt.checkpw(password_from_form, password_from_db)

def hash_password(password: bytes):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password, salt=salt)

def initial_data(*args):
    try:
        check_exist_db()
    except:
        create_tables()
        for user in args:
            password = user.get('password')
            password = hash_password(password.encode())
            add_user_in_db(user.get('username'), password)
    return
