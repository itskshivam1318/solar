from flask import Flask, render_template, request,redirect,flash,url_for
from flask_mysqldb import MySQL
import requests
from sklearn import linear_model
import pickle

app = Flask(__name__)

app.secret_key = "flash message"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'solar'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/prediction')
def prediction():
    return render_template("prediction.html")

@app.route('/forecast', methods=['POST'])
def forecast():
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=' + city + ',' + state + ','+country+'&appid=666aa9775ae333438329302bf038d988')
    data = r.json()
    with open('Irrad_pickle', 'rb') as f:
        model = pickle.load(f)
    with open('Genn_pickle', 'rb') as f:
        genn = pickle.load(f)
    return render_template("forecast.html", city = city, data = data, model= model, genn = genn)

@app.route('/log')
def log():
    cur = mysql.connection.cursor()
    cur.execute("Select * FROM log")
    data = cur.fetchall()
    cur.close()
    return render_template("log.html", data=data)

@app.route('/addlog')
def addlog():
    return render_template("addlog.html")

@app.route('/logging', methods=['POST'])
def logging():
    if request.method == "POST":
        flash("Log entered Successfully.")
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email_id']
        consumption= request.form['consumption']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO log(fname, lname, email, consumption) VALUES (%s,%s,%s,%s)',(fname,lname,email,consumption))
        mysql.connection.commit()
        return redirect(url_for("addlog"))

@app.route('/about')
def about():
    return render_template("about.html")



if __name__ == '__main__':
    app.run(debug = True)