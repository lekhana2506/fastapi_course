from fastapi.testclient import TestClient
from app.main import myapp
from app.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app import models
import os
import psycopg2
from app.database import base
import pytest
from app.oauth2 import create_access_token
from app.config import Settings

settings=Settings()

#client=TestClient(app)

database_url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/testing'
engine=create_engine(database_url)

TestingsessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

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
    myapp.dependency_overrides[get_db]=override_get_db
    yield TestClient(myapp)                 # runs the test

@pytest.fixture
def test_user2(client):
    user_data={"email":"helloworld1@gmail.com","password":"1234"}
    res=client.post("/users",json=user_data)
    assert res.status_code==200
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data={"email":"helloworld@gmail.com","password":"123"}
    res=client.post("/users",json=user_data)
    assert res.status_code==200
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post_creation(test_user,session,test_user2):
    post_data=[
        {
            "title":"title1",
            "content":"content1",
            "owner_id":test_user['id']
        },
        {
            "title":"title2",
            "content":"content2",
            "owner_id":test_user['id']
        },
        {
            "title":"title3",
            "content":"content3",
            "owner_id":test_user2['id']
        },
        {
            "title":"title4",
            "content":"content4",
            "owner_id":test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map=map(create_post_model,post_data)
    posts=list(post_map)

    session.add_all(posts)
    session.commit()
    posts_list=session.query(models.Post).all()
    return posts_list