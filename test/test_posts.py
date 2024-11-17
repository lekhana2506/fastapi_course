from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_post_creation):
    res=authorized_client.get("/createposts")
    print(res.json())

    def validate(post):
        return schemas.PostOut(**post)
    post_map=map(validate,res.json())
    posts=list(post_map)
    assert res.status_code==200

def test_unauthorized_user_get_all_posts(client,test_post_creation):
    res=client.get("/createposts")
    assert res.status_code==401
    
def test_unauthorized_user_get_one_posts(client,test_post_creation):
    res=client.get(f"/createposts/{test_post_creation[0].id}")
    assert res.status_code==401

def test_get_one_post_not_exist(authorized_client, test_post_creation):
    res = authorized_client.get(f"/createposts/8888")
    print(res.json())  # Print for debugging
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}

def test_get_one_post(authorized_client,test_post_creation):
    res=authorized_client.get(f"/createposts/{test_post_creation[0].id}")
    print(res.json())
    post=schemas.PostOut(**res.json())
    assert post.Post.title==test_post_creation[0].title

@pytest.mark.parametrize("title,content,is_publsihed",[
    ("title1",'content1','True'),
    ("title2",'content2','False'),
    ("title3",'content3','True')
])
def test_create_post(authorized_client,test_user,title,content,is_publsihed):
    res=authorized_client.post("/createposts",json={"title":title,"content":content,"is_published":is_publsihed})
    new_post=schemas.RetrievedPost(**res.json())
    print(new_post)
    assert res.status_code==200
    assert new_post.title==title
    assert new_post.owner_id==test_user['id']

def test_unauthorized_user_create_post(client,test_user):
    res=client.post("/createpots",json={'title':'dvcsz','content':'vadszv'})
    assert res.status_code==404

def test_unauthorized_delete_post(client,test_user,test_post_creation):
    res=client.delete(f'/createposts/{test_post_creation[0].id}')
    assert res.status_code==401

def test_authorized_delete_post(authorized_client,test_user,test_post_creation):
    res=authorized_client.delete(f'/createposts/{test_post_creation[0].id}')
    assert res.status_code==200

def test_authorized_delete_post_nonexist(authorized_client,test_user,test_post_creation):
    res=authorized_client.delete(f'/createposts/896')
    assert res.status_code==404

def test_delete_otheruser_post(authorized_client,test_user,test_post_creation):
    res=authorized_client.delete(f'/createposts/{test_post_creation[3].id}')
    assert res.status_code==404

def test_update_post(authorized_client,test_user,test_post_creation):
    data={
        'title':"updated title",
        'content':'updated content',
        'id': test_post_creation[0].id
    }
    res=authorized_client.put(f'/createposts/{test_post_creation[0].id}',json=data)
    updated_post=schemas.Post(**res.json())
    assert res.status_code==200
    assert updated_post.title==data['title']
    assert updated_post.content==data['content']

def test_update_other_user_post(authorized_client,test_user,test_user2,test_post_creation):
    data={
        'title':"updated title",
        'content':'updated content',
        'id': test_post_creation[3].id
    }
    res=authorized_client.put(f'/createposts/{test_post_creation[3].id}',json=data)
    assert res.status_code==404

def test_unauthorized_update_post(client,test_user,test_post_creation):
    res=client.put(f'/createposts/{test_post_creation[0].id}')
    assert res.status_code==401

def test_authorized_update_post_nonexist(authorized_client,test_user,test_post_creation):
    data={
        'title':"updated title",
        'content':'updated content',
        'id': test_post_creation[3].id
    }
    res=authorized_client.put(f'/createposts/896',json=data)
    assert res.status_code==404
