import logging
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return 'Secure Password Manager API!'

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    email = request.form['email']
    password = request.form['password']
    logger.info(f"Login attempt: {email}, {password}")

    if email == 'test@example.com' and password == 'testpassword':
        return 'Login successful!'
    else:
        return 'Invalid email or password.'
    
if __name__ == '__main__':
    logging.info('Application started')
    app.run(debug=True, port=5000)
