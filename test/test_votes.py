import pytest
from app import models

@pytest.fixture()
def test_voted_post(test_post_creation,session,test_user):
    new_vote=models.Votes(post_id=test_post_creation[3].id,user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client,test_post_creation):
    res=authorized_client.post("/votes/",json={'post_id':test_post_creation[3].id,'direction':1})
    assert res.status_code==201

def test_vote_post_twice(authorized_client,test_post_creation,test_voted_post):
    res=authorized_client.post("/votes/",json={"post_id":test_post_creation[3].id,"direction":1})
    assert res.status_code==409

def test_delete_vote(authorized_client,test_post_creation,test_voted_post):
    res=authorized_client.post("/votes/",json={"post_id":test_post_creation[3].id,"direction":0})
    assert res.status_code==201

def test_delete_vote_not_exsist(authorized_client,test_post_creation):
    res=authorized_client.post("/votes/",json={"post_id":test_post_creation[0].id,"direction":0})
    assert res.status_code==404

def test_vote_post_non_exist(authorized_client,test_post_creation):
    res=authorized_client.post("/votes/",json={"post_id":8888,"direction":1})
    assert res.status_code==404

def test_vote_unauthorized_user(client,test_post_creation):
    res=client.post("/votes/",json={"post_id":test_post_creation[0].id,"direction":1})
    assert res.status_code==401

