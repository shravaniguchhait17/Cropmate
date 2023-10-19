import pyrebase
from flask import request


class Login_Admin(object):

    def __init__(self):
        
        self.config = {
            "apiKey": "AIzaSyDh4zCPQPOma3raq3A6RASCwn2bPBluUzk",
            "authDomain": "crop-detection-app-cb3de.firebaseapp.com",
            "databaseURL": "https://crop-detection-app-cb3de-default-rtdb.firebaseio.com",
            "projectId": "crop-detection-app-cb3de",
            "storageBucket": "crop-detection-app-cb3de.appspot.com",
            "messagingSenderId": "142309765615"
        }


        self.firebase = pyrebase.initialize_app(self.config)

        self.auth = self.firebase.auth()

    def admin_login(self):

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['pass']
            try:
                user = self.auth.sign_in_with_email_and_password(email, password)
                
                return 'successful',email
            except:
                return 'unsuccessful'
