import pyrebase
from flask import request


class Login(object):

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

    def kisan_login(self):

        if request.method == 'POST':
            kisan_id = request.form['kisan_id']
            print(kisan_id)
            password = request.form['password']
            print(password)
            email = 'kisan'+kisan_id+'@gmail.com'
            print(email)
            try:
                user = self.auth.sign_in_with_email_and_password(email, password)
                print(user)
                return 'successful',email
            except Exception as e:
                print('Error creating user:', e)
                return 'unsuccessful'