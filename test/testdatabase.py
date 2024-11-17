from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db
import os
import psycopg2
from app.database import base
import pytest

#client=TestClient(app)



@pytest.fixture()
def session():
    base.metadata.drop_all(bind=engine)   # drops the prev tables
    base.metadata.create_all(bind=engine) # creates database
    db=TestingsessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)                 # runs the test


database_url=f'postgresql://postgres:2506@localhost:5432/testing'
engine=create_engine(database_url)

TestingsessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)