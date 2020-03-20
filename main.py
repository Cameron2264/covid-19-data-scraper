
def CamIsBoss():
    print ("DDogggg")

import os, atexit, socket
from flask import Flask, jsonify #pip install flask
from apscheduler.schedulers.background import BackgroundScheduler
import covidInfoUpdater as covid

localHost = '127.0.0.1'
globalHost = 'xxx.xxx.xxx.xxx'

#init flask
app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/global')
def getGlobalStats():
    return covid.getCoronaGlobalData()

@app.route('/country/<id>')
def getLocalStatsByCountry(id):
    return covid.getCoronaLocalData()[id.lower()]

@app.route('/getCountryList')
def getCountryList():
    return jsonify(covid.getCountryListData())

def correctIP():
    global globalHost
    hostname = socket.gethostname()    
    globalHost = socket.gethostbyname(hostname)

def scheduledTasks():
    covid.updateInfo()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=covid.updateInfo, trigger="interval", seconds=20)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

def main():
    #gets your ipv4 and stores it into 'globalHost'
    correctIP()

    #fetches the info every 20 seconds
    scheduledTasks()

    #starts flask as an online service
    app.run(host=localHost, port='8000', debug=False, use_reloader=False)

if __name__ == "__main__":
    main()