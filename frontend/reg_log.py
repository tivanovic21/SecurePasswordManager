import requests as req

def register(email, password, firstname, lastname):
    print(email, password, firstname, lastname)

def login(email, password):
    url = 'http://localhost:5000/login'
    req.post(url, data={'email': email, 'password': password})
