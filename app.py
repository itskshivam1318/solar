from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/temperature', methods = ['POST'])
def temperature():
    zipcode = request.form['zip']
    #return zipcode
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',in&appid=666aa9775ae333438329302bf038d988')
    json_object = r.text
    return json_object
    json_object = r.json()
    temp_k = float(json_object['main']['temp'])
    #return  str(temp_k)
    temp_c = temp_k -273.15
    return render_template('temperature.html',temp = round(temp_c,2))

@app.route('/latlong', methods=['POST'])
def latlong():
    lat = request.form['lat']
    long = request.form['long']
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+long+'&appid=666aa9775ae333438329302bf038d988')
    #json_object = r.text
    #return json_object
    json_object = r.json()
    temp_K = float(json_object['main']['temp'])
    #return str(temp_K)
    temp_c = temp_K - 273.15
    return render_template('latlong.html', temp = round(temp_c,2))

@app.route('/city', methods=['POST'])
def city():
    city = request.form['city']
    state = request.form['state']
    #country = request.form['country']
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+','+state+',in&appid=666aa9775ae333438329302bf038d988')
    #json_object = r.text
    #return json_object
    data = r.json()
    '''
    select_data = dict['list']
    for box in select_data:
        if 'dt_txt' in box:
            box['dt_txt']
    '''
    return render_template('city.html', data = data)






if __name__ == '__main__':
    app.run(debug = True)