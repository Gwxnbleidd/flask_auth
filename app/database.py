from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

from config import DB_URL

class Base(DeclarativeBase):
    pass

engine = create_engine(url=DB_URL, echo=False)
session_factory = sessionmaker(engine)

class UsersTable(Base):
    __tablename__ = 'users'

    id: Mapped[int] =  mapped_column(primary_key= True)
    username: Mapped[str] = mapped_column(nullable=False) 
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)


def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_user_in_db(username: str, password: bytes):
    with session_factory() as session:
        session.add(UsersTable(username=username, hashed_password=password))
        session.commit()

def get_user_from_db(username: str):
    with session_factory() as session:
        query = select(UsersTable.id, UsersTable.username, UsersTable.hashed_password).filter_by(username=username).limit(1)
        return session.execute(query).fetchone()

def check_exist_db():
    with session_factory() as session:
        res = session.execute(select(UsersTable.username).limit(1))
        
        return res.fetchone()