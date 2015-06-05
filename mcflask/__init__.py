from flask import Flask
from flask.ext.mongoengine import MongoEngine
from pymongo import read_preferences

from flask_mail import Mail, Message








#create application
app = Flask(__name__)


app.secret_key = 'W\x86l,l\xb7Q\x19go\x9d`3{\x8etw\xea;>\x0bf\x1c\xf4'
app.config.from_pyfile('config.ini')
app.config["MONGODB_SETTINGS"] = {'db' : app.config["DATABASENAME"], 'read_preference': read_preferences.ReadPreference.PRIMARY}

debug = True

mail = Mail(app)

#create database
db = MongoEngine(app)

from mcflask.functions import initmembers



import mcflask.views
import mcflask.admin



#todo remove implement in usersystem

initmembers()



if __name__ == "__main__":

    #todo remove
    app.run()
