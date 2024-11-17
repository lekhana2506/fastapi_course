from app import schemas
import pytest
from jose import jwt
from app.config import Settings

setting=Settings()


def test_root(client):
    response=client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message')=='changed'
    assert response.status_code==200

def test_user_creation(client):
    res=client.post("/users",json={"email":"helloworld@gmail.com","password":"123"})
    new_user=schemas.UserResponse(**res.json())
    assert new_user.email=='helloworld@gmail.com'
    assert res.status_code==200

def test_login_user(client,test_user):
    res=client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    print(res.json())
    login_res=schemas.Token(**res.json())
    payload=jwt.decode(login_res.access_token,setting.secret_key,algorithms=[setting.algorithm])
    id=payload.get("user_id")
    assert res.status_code==200
    assert login_res.token_type=='bearer'
    assert id==test_user['id']

@pytest.mark.parametrize("email,password,status_code",[
    ('wrongemail@gmail.com','123',500),
    ('wrongemail@gmail.com','wrongpassword',500),
    ('helloworld@gamil.com','wrongpassword',500),
    (None,'123',500),
    ('helloword@gmail.com',None,500)
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res=client.post("/login",data={"username":email,"password":password})
    assert res.status_code==status_code
    #assert res.json().get('detail')=='Internal server error'


