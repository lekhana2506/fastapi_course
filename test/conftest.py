from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
import pytest

# Test database URL
TEST_DATABASE_URL = 'postgresql://postgres:2506@localhost:5432/testing'

# Create engine and session factory for the test database
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pytest fixture to manage database session
@pytest.fixture()
def session():
    # Drop and recreate tables for a clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pytest fixture for the test client
@pytest.fixture()
def client(session):
    # Override `get_db` to use the test database session
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

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