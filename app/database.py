from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings

settings=Settings()

database_url=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine=create_engine(database_url)

SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    except:
        db.close()
    finally:
        db.close()

