from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings
import psycopg2
import os

settings=Settings()

database_url = os.getenv('DATABASE_URL', f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')
# if database_url.startswith("postgres://"):
#     database_url = database_url.replace("postgres://", "postgresql://", 1)
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

