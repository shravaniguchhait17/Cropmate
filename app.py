from flask import Flask, render_template, request, flash,jsonify,redirect,url_for
from flask_bootstrap import Bootstrap

# Weather Prediction
from weather import Weather

# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from test import Predict
from firebase_admin import auth

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firebase end Here

# Login
from login import Login

# Admin Login
from admin_login import Login_Admin

# Kisan Center Login
from kisan_center_login import Login_Kisan

# Weather Forcast 15 Days
import requests
import bs4

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'e53b7406a43e2fd9ec89553019420927'


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/weather',methods=['POST','GET'])
def weather():
    weatherModel = Weather()
    if request.method == 'POST':
        city_name = request.form['city']
        if len(city_name) == 0:
            return render_template('weather_pred.html',error=1)
        try:
            daily = request.form['daily']
            print(daily)
            valid = weatherModel.get_weather(city_name)
            if valid == 'noData':
                return render_template('weather_pred.html',error=1)

            # weather_data = weatherModel.display()
            # print()
            invalidZip = False
            results = {"zipcode":city_name,"invalidZip":invalidZip, "weather":valid}
            print(results)
            return render_template('weather.html', results = results)
        except:
            day_15 = request.form['15days']
            print(day_15)
            city_name = city_name.lower()
            print(city_name)
            res = requests.get('https://www.timeanddate.com/weather/india/'+city_name+'/ext')
            data = bs4.BeautifulSoup(res.text,'lxml')
            # print(data)
            weather_table = data.find('table', {"id": "wt-ext"})
            # print(weather_table)
            tbody = weather_table.find('tbody')
            rows = tbody.find_all('tr')
            # print(rows)
            extracted_data = []

            # Loop through the rows and extract required attributes
            for row in rows:
                columns = row.find_all('td')
                # print(columns)
                # day = columns[1].text.strip()  # Extract day
                # print(day)
                temp = columns[3].text.strip()  # Extract temperature
                print(temp)
                weather = columns[2].text.strip()  # Extract weather description
                print(weather)
                wind_speed = columns[4].text.strip()  # Extract maximum temperature
                print(wind_speed)
                max_humidity = columns[6].text.strip()  # Extract maximum temperature
                print(max_humidity)
                sunrise = columns[10].text.strip()  # Extract maximum temperature
                print(sunrise)
                sunset = columns[11].text.strip()  # Extract maximum temperature
                print(sunset)
                print("\n")
                # Append the extracted data as a dictionary to the list
                extracted_data.append({'temp': temp, 'weather': weather, 'wind_speed': wind_speed, 'max_humidity': max_humidity, 'sunrise': sunrise, 'sunset': sunset})

            # Print the extracted data for verification
            print(extracted_data)
                  

            return render_template('weather_15_days.html',result=extracted_data,result_len = len(extracted_data))    
    
    return render_template('weather_pred.html',error=0)



@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':

        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone']
        kisan_id = request.form['kisan_id']
        adhar_id = request.form['adhar_id']
        state = request.form['state']
        city = request.form['city']
        fullAddress = request.form['fullAddress']
        locality = request.form['locality']
        zipcode = request.form['zipcode']
        password = request.form['password']
        conform_password = request.form['conform_password']
        print(first_name,middle_name,last_name, phone_number,kisan_id,state,city,fullAddress,locality,password,conform_password)


        docs = db.collection(u'kisan_id').get()
        print(docs)
            # print(u'{} => {}'.format(doc.id,data))

        if password == conform_password:
             for doc in docs:
                data = doc.to_dict()
                print(data)
                for item in data['id']:
                 print(item)
                 if item == kisan_id:
                    try:
                        email_id = 'kisan'+kisan_id+'@gmail.com'
                        print(email_id)
                        user = auth.create_user(email = email_id,password= password)
                        print('Sucessfully created new user: {0}'.format(user.uid))
                    except Exception as e:
                        print('Error creating user:', e)
                        return render_template('register.html',alert=2,first_name=first_name)
                    

                    

                    if user.uid:
                        doc_ref = db.collection(u'users').document(u''+user.uid)
                        doc_ref.set({
                            u'first_name': first_name,
                            u'middle_name': middle_name,
                            u'last_name' :last_name,
                            u'phone_number': phone_number,
                            u'kisan_id': kisan_id,
                            u'adhar_id': adhar_id,
                            u'state': state,
                            u'city': city,
                            u'fullAddress': fullAddress,
                            u'locality': locality,
                            u'zipcode': zipcode
                            })

                        
                        return render_template('register.html',alert=1,first_name=first_name)

    return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():

    if request.method == 'POST':
        login_kisan = Login()
        data,email = login_kisan.kisan_login()
        print(data)
        print(type(data))
        
        if data == 'successful':
            user = auth.get_user_by_email(email)
            print('Successfully fetched user data: {0}'.format(user.uid))

            doc_ref = db.collection(u'users').document(u''+user.uid)
            
            docs = doc_ref.get().to_dict()
            print(docs)
            print(user.uid)
            return render_template('kisan_profile.html',data=docs,display=False,user_id=user.uid)
        else:
            flash(f'Login Failed Please check Your Kisan ID Number and Password','danger')
            return redirect('/login')



    return render_template('login.html')


if __name__ == "__main__":
    
    app.run(debug=True)
    
