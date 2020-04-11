from flask import Flask, render_template, request,redirect,flash,url_for
from flask_mysqldb import MySQL
import requests
from sklearn import linear_model
import pickle
import numpy as np
import os

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
        processinput = request.form['process']
        wastageinput = request.form['wastage']
        # process input
        processes = processinput.split()
        process = [int(x) for x in processes]
        process = np.array(process)
        process = process.reshape((int(len(process) / 2), 2))  # converting 2d
        process = process.tolist()
        inputprocess = process
        processlen = len(process)

        #wastage input
        wastages = wastageinput.split()
        wastage = [int(x) for x in wastages]
        wastage = np.array(wastage)
        wastage = wastage.tolist()
        inputwastage = wastage
        total_wastage = sum(wastage)
        wastagesum = total_wastage

        #adding percentage
        for p in range(len(process)):
            process[p].insert(0, process[p][0] * 100.0 / process[p][1])
        #adding process id
        for p in range(len(process)):
            process[p].insert(0, p + 1)

        os.remove("output.txt")

        while (len(process) != 0 or total_wastage < 0):
            process.sort(key=lambda process: process[1])
            #print("after 10 min add 10% of its battery capacity to the process with highest proirity")
            process[0][2] = process[0][2] + 10 / 100 * process[0][3]
            total_wastage = total_wastage - 10 / 100 * process[0][3]
            #print(process)
            #print("update battery status")
            process[0][1] = process[0][2] * 100.0 / process[0][3]
            #print(process)
            #print("total wastage: {}".format(total_wastage))
            f = open("output.txt","a")
            f.write("$")
            f.write("<---- After 10 minutes and 10% charge ---->")
            f.write("#")
            f.write("Current Process under execution: {}.#".format(str(process[0][0])))
            f.write("Battery Percentage: {}%#".format(str(process[0][1])))
            f.write("Current charge: {}W#".format(str(process[0][2])))
            f.write("Capacity: {}W#".format(str(process[0][3])))
            f.write("|| Processes ||#")
            for i in range(1,len(process)):
                f.write("Process: {}, ".format(str(process[i][0])))
                f.write("Battery: {}%, ".format(str(process[i][1])))
                f.write("Charge: {}W, ".format(str(process[i][2])))
                f.write("Capacity: {}W,#".format(str(process[i][3])))
            f.write("Total Wastage: {}W.#".format(str(total_wastage)))
            if (process[0][1] == 100.0 or process[0][2] > process[0][3]):
                #print("completed process:{}".format(process.pop(0)))
                f.write("Completed process: {}".format(str(process.pop(0))))
            else:
                f.write("Completed process: None")
            f.write("#")
            f.write("-----------------------------------------------")
            f.write("-----------------------------------------------")

            f.write("#")
        f.close()
        f = open("output.txt","r")
        output = f.read()
        f.close()

        output = str(output.split('$'))
        output = output.split('#')
        outputlen= len(output)

        return render_template("result.html",inputprocess = inputprocess,inputwastage=inputwastage,wastagesum=wastagesum,process = process,processlen=processlen, wastage= wastage, total_wastage=total_wastage,output=output, outputlen=outputlen)


@app.route('/about')
def about():
    return render_template("about.html")



if __name__ == '__main__':
    app.run(debug = True)