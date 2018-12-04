from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config.from_object('config.Config')

mongo = PyMongo(app)

from modules.web.routes import web
from modules.api.routes import api

app.register_blueprint(web)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run()
