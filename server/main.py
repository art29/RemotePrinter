import json
import requests
from flask import Flask, jsonify, make_response
from flask import request as form_request
from flask_assistant import Assistant, ask, tell, request
import pymysql.cursors
from jose import jwt
import conf

app = Flask(__name__)
log = app.logger


# Database credentials

host = conf.host
user = conf.user
password = conf.password
database = conf.db

# Connecting to Database to get url
# Database has a table called oauth with 3 columns (url, oauthid, apikey)
# You need to input the values in the database manually the first time

def database(userid):
    db = pymysql.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM oauth WHERE oauthid = %(col1)s;", {'col1': userid})
            myresult = cursor.fetchone()
    finally:
        db.close()
    return myresult


# Getting User ID from the Dialogflow's request
def get_user_id(request):
    try:
        token = request['originalDetectIntentRequest']['payload']['user'].get('idToken')

        certificate_url = 'https://www.googleapis.com/oauth2/v1/certs'

        response = requests.get(certificate_url)
        certs = json.loads(response.text)

        decoded_info = jwt.decode(token, certs, algorithms=['RS256'],
                                  audience="368764931202-8klro5p8k6700o23ehle251pos44979k.apps.googleusercontent.com")
    except:
        return None
    return decoded_info['sub']


@app.route('/', methods=['POST'])
# Receive new url from a printer
def receive():
    receive_db = pymysql.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    url = form_request.form['url']
    oauth_id = form_request.form['OauthId']
    api_key = form_request.form['ApiKey']
    cursor = receive_db.cursor()
    cursor.execute("UPDATE oauth SET url = %(col1)s WHERE oauthid = %(col2)s AND apikey = %(col3)s;",
                   {'col1': url, 'col2': oauth_id, 'col3': api_key})
    receive_db.commit()
    if cursor.rowcount > 0:
        return 'Received !'  # Update Row
    else:
        cursor.execute("INSERT INTO oauth (url, oauthid, apikey) VALUES (%(col1)s, %(col2)s, %(col3)s);",
                       {'col1': url, 'col2': oauth_id, 'col3': api_key})
        receive_db.commit()
        if cursor.rowcount > 0:
            return 'Received !'  # Create Row if it isn't found
        else:
            return 'Error has been detected... or maybe the same details were already sent.'


# Identifying Dialogflow App
assist = Assistant(app, project_id="test-273da", route='/webhook')


# Setting up webhook
@app.route('/webhook', methods=['POST'])
# Action greeting
@assist.action('greeting')
def greet_and_start():
    speech = "Hi, How are you ? You can ask me multiple things, for example you can ask me to change the temperature " \
             "or, get your user i d so you can do your first setup ! "
    return ask(speech)


# Get ID action for the user to put the User ID in the conf.py file
@assist.action('get-id')
def get_id():
    try:
        userid = get_user_id(request)
        speech = "Ok, the User Id is " + userid
    except:
        speech = "An error has occured, please try later."
    return tell(speech)


# Change temperature action
@assist.action("change-temperature")
def change_temperature(temperature):
    try:
        userid = get_user_id(request)
        url = database(userid)[2] + "/api/printer/tool"
        headers = {'Content-Type': 'application/json', 'X-Api-Key': database(userid)[3]}
        if temperature == "zero":
            temperature = "0"
        temperature = int(temperature)
        payload = {'command': 'target', "targets": {"tool0": temperature}}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if r.status_code != 204:
            speech = "Error, their is a problem, the printer will not heat up, try to find the problem or try later !"
        else:
            temperature = str(temperature)
            if temperature == "0":
                speech = "Ok, cooling down"
            else:
                speech = "Ok, heating up to " + temperature + " degrees"

    except:
        speech = "An error has occured, please try later."
    return tell(speech)


# Extrude filament action
@assist.action("extrude-filament")
def extrude_filament(mm):
    try:
        userid = get_user_id(request)
        url = database(userid)[2] + "/api/printer/tool"
        headers = {'Content-Type': 'application/json', 'X-Api-Key': database(userid)[3]}
        payload = {'command': 'extrude', "amount": int(mm)}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        print(r.status_code)
        if r.status_code != 204:
            speech = "Error, the printer will not extrude, maybe try when the printer isn't printing or try again " \
                     "later ! "
        else:
            speech = "Ok, extruding " + mm + " millimeters"
    except:
        speech = "An error has occured, please try later."
    return tell(speech)


# Home axes action
@assist.action("home-axes")
def home_axes(axes):
    try:
        userid = get_user_id(request)
        url = database(userid)[2] + "/api/printer/printhead"
        headers = {'Content-Type': 'application/json', 'X-Api-Key': database(userid)[3]}
        payload = {'command': 'home', "axes": axes}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        print(r.status_code)
        if r.status_code != 204:
            speech = "Error, the printer will not home, maybe try when the printer isn't printing or try again later !"
        else:
            speech = "Ok, homing"
    except:
        speech = "An error has occured, please try later."
    return tell(speech)


# Get percentage action
@assist.action("get-percentage")
def get_percentage():
    try:
        userid = get_user_id(request)
        url = database(userid)[2] + "/api/job"
        headers = {'Content-Type': 'application/json', 'X-Api-Key': database(userid)[3]}
        r = requests.get(url, headers=headers)
        json_response = r.json()
        percentage = json_response['progress']['completion']
        if r.status_code != 200:
            speech = "Error, their is a problem, I cannot get the percentage, try to find the problem or try later !"
        else:
            if percentage == None:
                speech = "The printer is not printing right now"
            else:
                percentage = str(int(percentage))
                speech = "Ok, the print is now at about " + percentage + " percent"
    except:
        speech = "An error has occured, please try later."
    return tell(speech)


# Get time left action
@assist.action("get-timeleft")
def get_timeleft():
    try:
        userid = get_user_id(request)
        url = database(userid)[2] + "/api/job"
        headers = {'Content-Type': 'application/json', 'X-Api-Key': database(userid)[3]}
        r = requests.get(url, headers=headers)
        json_response = r.json()
        timeleft = json_response['progress']['printTimeLeft']
        if r.status_code != 200:
            speech = "Error, their is a problem, I cannot get the time left, try to find the problem or try later !"
        else:
            if timeleft == None:
                speech = "The printer is not printing right now"
            else:
                timeleft = int(timeleft)
                timeleft = timeleft / 60
                timeleft = int(timeleft)
                timeleft = str(timeleft)
                speech = "Ok, the print has about " + timeleft + " minutes left"
    except:
        speech = "An error has occured, please try later."
    return tell(speech)


# Get temperature action
@assist.action("get-temperature")
def get_temperature():
    try:
        userid = get_user_id(request)
        url = database(userid)[2] + "/api/printer/tool"
        headers = {'Content-Type': 'application/json', 'X-Api-Key': database(userid)[3]}
        r = requests.get(url, headers=headers)
        json_response = r.json()
        get_temp = json_response['tool0']['actual']
        if r.status_code != 200:
            speech = "Error, their is a problem, I cannot get the temperature, try to find the problem or try later !"
        else:
            get_temp = int(get_temp)
            get_temp = str(get_temp)
            speech = "Ok, the printer's temperature is about " + get_temp + " degrees"
    except:
        speech = "An error has occured, please try later."
    return tell(speech)


if __name__ == '__main__':
    app.run(debug=True)
