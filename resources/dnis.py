from flask_restful import Resource
from flask import request
from Req_Parser import Req_Parser
import requests


class DNI(Resource):
    parser = Req_Parser()
    parser.add_argument('dni', str, required=True)

    def post(self):

        url = 'https://api.peruapis.com/v1/dni'

        print(request.json)
        dni = request.json['dni']
        data = {'document': str(dni)}
        headers = {'Authorization': 'Bearer pRqpAIW6ZhqET16qE7mgMXv4ptqGi5xvdrWIzqLDYvwJDUHeKLmNgaF8R1Rp',
                   'Accept': 'application/json'}

        response = requests.post(
            url, data=data, headers=headers)
        print(response.json())

        return response.json()