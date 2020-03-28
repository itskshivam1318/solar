from flask import Flask, render_template, request,redirect,flash,url_for
from flask_mysqldb import MySQL
import requests
from sklearn import linear_model
import pickle
import numpy as np

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

@app.route('/sjf')
def sjf():
    return render_template("redistribution.html")

@app.route('/arrayentry', methods=['POST'])
def arrayentry():
    if request.method == 'POST':
        array = request.form['array']
        inputss = array.split()
        inputs = [int(x) for x in inputss]
        inputs = np.array(inputs)
        process = inputs.reshape((int(len(inputs) / 2), 2))  # converting 2d
        process = process.tolist()
        for p in range(len(process)):
            process[p].insert(0, p + 1)
        sjf = sorted(process, key=lambda x: (x[2], x[1]))
        ct = []
        for i in range(int(len(sjf))):
            if i == 0:
                ct.append(sjf[i][1] + sjf[i][2])
            else:
                ct.append(sjf[i][2] + ct[i - 1])
        ctlen = len(ct)
        tat = []
        for i in range(int(len(sjf))):
            tat.append(ct[i] - sjf[i][1])
        tatlen = len(tat)
        wt = []
        for i in range(int(len(sjf))):
            wt.append(tat[i] - sjf[i][2])
        wtlen = len(wt)
        avarage_WT = round(np.mean(wt), 2)

        return render_template("result.html", inputs = inputs, process= process,sjf =sjf, ct= ct, ctlen= ctlen, tat= tat, tatlen = tatlen,wt=wt, wtlen = wtlen, avarage_WT= avarage_WT)


@app.route('/about')
def about():
    return render_template("about.html")



if __name__ == '__main__':
    app.run(debug = True)