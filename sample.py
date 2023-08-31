import requests
from flask import Flask, redirect, request, session, url_for
from flask_login import (LoginManager, UserMixin, login_required, login_user)
from flask_oauthlib.client import OAuth

# User class for Flask-Login
class User(UserMixin):
   def __init__(self, user_id):
        self.id = user_id

app = Flask(__name__)

app.secret_key = '1234567890'  # Needed to use sessions

login_manager = LoginManager()
login_manager.init_app(app)

#LinkedIn data
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://REDIRECT_URL/login/authorized'
AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Set up unauthorized handler to render the unauthorized template
@login_manager.unauthorized_handler
def unauthorized():
    return "Unauthorized!" 

@app.route('/login')
def login():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': 'random_string_for_csrf_prevention',  # Should be random for security reasons
        'scope': 'profile email openid'  # Adjust scope based on your needs
    }
    url = requests.Request('GET', AUTHORIZATION_URL, params=params).prepare().url
    return redirect(url)

@app.route('/logout')
def logout():
    session.pop('linkedin_oauth', None)
    return "Logged out!" 

@app.route('/login/authorized')
def authorized():
    error = request.args.get('error', '')
    if error:
        return f"Error received: {error}"
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()
    session['linkedin_token'] = response_data['access_token']
    # Fetch user email address
    headers = {
        'Authorization': f"Bearer {session['linkedin_token']}",
        'cache-control': 'no-cache',
        'X-Restli-Protocol-Version': '2.0.0'  # LinkedIn requires this header for using their v2 API
    }
    response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
    data = response.json()
    # Extracting details
    user_id = data['sub']
    email_verified = data['email_verified']
    full_name = data['name']
    country = data['locale']['country']
    language = data['locale']['language']
    first_name = data['given_name']
    last_name = data['family_name']
    email = data['email']
    profile_picture = data['picture']
    print(f"{user_id}, {full_name}, Logged in with email: {email}")
    # user session
    user =  User(user_id)
    login_user(user)
    return redirect(url_for('chat'))


@app.route('/')
def index():
    return "This is the index!"

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return "this is the chat! Access to logged in users only!"

if __name__ == "__main__":
    app.run(debug=True)
