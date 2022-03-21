from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
 
app.config['SERVER_NAME'] = '127.0.0.1:5000'
oauth = OAuth(app)
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/google/')
def google():
   
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    try:
        token = oauth.google.authorize_access_token()
        # user = oauth.google.parse_id_token(token)
        # print(" Google User ", user)
        print(token['userinfo'])
        print(token['userinfo'].keys())
    except:
        print("Error")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)