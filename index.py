from flask import Flask
from flask_restful import Api
from src.api import geHealthcareRestApi


app = Flask(__name__)
api = Api(app)
api.add_resource(geHealthcareRestApi, '/')

if __name__ == '__main__':
    app.run(debug=True)
