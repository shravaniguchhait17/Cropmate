# imports
import pyowm
import dateutil.parser
import requests
# map to icons for display in widget
ICONMAP = {
  '01d':'wi-day-sunny',
  '02d':'wi-day-cloudy',
  '03d':'wi-cloudy',
  '04d':'wi-rain',
  '09d':'wi-showers',
  '10d':'wi-rain',
  '11d':'wi-thunderstorm',
  '13d':'wi-snow',
  '50d':'wi-fog',
  '01n':'wi-night-clear',
  '02n':'wi-night-cloudy',
  '03n':'wi-night-cloudy',
  '04n':'wi-night-rain',
  '09n':'wi-night-showers',
  '10n':'wi-night-rain',
  '11n':'wi-night-thunderstorm',
  '13n':'wi-night-snow',
  '50n':'wi-fog',
}

'''
This is a weather object that acts
as the mini widget on the web application
to retrieve quick stats about the queried
zipcode 

init by setting the PWOWM api key
'''
class Weather(object):
  
  def __init__(self):
    API_key = 'bbc00bebcdfaaf6c4b97bc4161dc189e'
    self.owm = pyowm.OWM(API_key)
    print(self.owm)
  '''
  get the data from the server with
  the queried zipcode and parses
  the forecast and json into
  a dictionary
  @param zipcode, the query zipcode
  '''
  def get_weather(self,city_name):
    API_key = 'bbc00bebcdfaaf6c4b97bc4161dc189e'
    endpoint = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric'
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        location = data['name']
        print(location)
        weather_description = data['weather'][0]['description']
        weather = data['weather']
        print(weather_description)
        temperature = data['main']['temp']
        print(temperature)
        return data
    else:
        return 'noData'
    
  def update(self, zipcode):
    '''Get data from the server'''
    zipcode = str(zipcode)
    print(zipcode)
    try:
      loc = self.owm.weather_at_place(zipcode)
      print(loc)
      current = loc.get_weather()
      print(current)
      fc = self.owm.three_hours_forecast(zipcode)
      # fc = owm.daily_forecast(zipcode,limit=6)
      forecast = fc.get_forecast().get_weathers()
    except :
      return 'noData'
    
    
    # parse the forecast
    self.data = self.parse(current)
    self.data["forecast"] = [(weather.get_reference_time('iso').split(" ")[0],weather.get_status()) 
    	for weather in forecast]
  
  '''
  return the current data
  @return data
  '''
  def display(self):
    return self.data
  
  '''
  parse the owm weather object for each
  key that we have queried and then set it into
  an organized dict with its values
  @param w, pyowm weather object
  @return data as a dict
  '''
  def parse(self, w):
    temp = w.get_temperature('fahrenheit')
    if 'temp_min' in temp:
      temp = dict(day=temp['temp'],
                  min=temp['temp_min'],
                  max=temp['temp_max'])
    icon = w.get_weather_icon_name()
    
    data = dict(
      date        = dateutil.parser.parse(w.get_reference_time('iso')),
      temp        = temp.get('day', 0),
      min         = temp.get('min', 0),
      max         = temp.get('max', 0),
      wind        = w.get_wind(),
      humidity 	  = w.get_humidity(),
      status      = w.get_status(),
      pressure    = w.get_pressure(),
      description = w.get_detailed_status(),
      code        = w.get_weather_code(),
      icon        = ICONMAP.get(icon,icon),
      sunrise     = dateutil.parser.parse(w.get_sunrise_time('iso')),
      sunset      = dateutil.parser.parse(w.get_sunset_time('iso')),
    )
    return data

# tests
if __name__ == '__main__':
  weatherApp = Weather()
  weatherApp.update('Davanagere')
  data = weatherApp.display()
  for key in data:
 		print (key, data[key])