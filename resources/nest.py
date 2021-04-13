from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from nest import read_input, parse_json


auth = HTTPBasicAuth()

CREDENTIALS = {
    'testUser': 'SuperSecretP@ssw0rd!'
}

#  verify if the user has access to the resource
@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return CREDENTIALS.get(username) == password

@auth.error_handler
def unauthorized():
    response = jsonify({
        'error': 'unauthorized',
        'message': 'Please authenticate to access this API.'})
    response.status_code = 401
    return response

class Nest(Resource):

    @auth.login_required
    def post(self):

        # get json from request body
        json_data = request.get_json(force=True)

        # get nlevels from request params json
        request_params = request.args.get('nlevels')
        if not request_params:
            response = jsonify({
                    'message': "Please provide nlevels as parameters"
                })
            response.status_code = 400
            return response

        # convert the params to list
        nlevels = [i for i in request_params.split(',')]
        res = parse_json(json_data, nlevels)

        if res:
            response = jsonify({
                'data': res
            })
            response.status_code = 201
            return response
        else:
            response = jsonify({
                'message': 'nlevels must be one of the keys in the json array'
            })
            response.status_code = 400
            return response

