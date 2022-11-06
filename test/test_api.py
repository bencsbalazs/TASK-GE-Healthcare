import requests
from src.api import geHealthcareRestApi


def test_api():

    api = geHealthcareRestApi()
    apiResponse = requests.get("http://127.0.0.1:5000")

    assert isinstance(api, object)
    assert apiResponse.status_code == 200
