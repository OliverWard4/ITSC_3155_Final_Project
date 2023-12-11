import os
import tempfile
import pytest
from flask import Flask, url_for
from corkboard import create_app, db
from corkboard.models import User, Board, Comment, Starred
from flask_login import current_user


#install pytest and stuff
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['SECRET_KEY'] = 'test_secret_key'


    with app.app_context():
        db.create_all()


        # Create a test user
        test_user = User(username='test_user', email='test@example.com', password='test_password')
        db.session.add(test_user)
        db.session.commit()


        yield app


        db.session.remove()
        db.drop_all()




@pytest.fixture
def client(app):
    return app.test_client()




def login(client):
    client.post('/login', data=dict(email='test@example.com', password='test_password'), follow_redirects=True)




def test_index(app, client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Landing Page' in response.data




def test_home(app, client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'Home' in response.data




def test_favoriteboards(app, client):
    login(client)
    response = client.get('/home/favoriteboards')
    assert response.status_code == 200
    assert b'Favorite Boards' in response.data




def test_landingPage(app, client):
    response = client.get('/home/landingPage')
    assert response.status_code == 200
    assert b'Landing Page' in response.data




def test_about(app, client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data




def test_register(app, client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


    response = client.post('/register', data=dict(
        username='new_user',
        email='new_user@example.com',
        password='new_password',
        confirm_password='new_password'
    ), follow_redirects=True)


    assert b'Your account has been created! You are now able to log in' in response.data




def test_login(app, client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


    response = client.post('/login', data=dict(
        email='test@example.com',
        password='test_password'
    ), follow_redirects=True)


    assert b'Login successful!' in response.data




def test_logout(app, client):
    login(client)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Landing Page' in response.data




# So above has the functions... ;) Still crankying out the details as we speak




if __name__ == '__main__':
    pytest.main()
