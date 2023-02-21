''' Flask web application. '''
from flask_cors import CORS
from flask import Flask, jsonify, request

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/generate', methods=['POST'])
def generate():
    ''' Generate the quantum comic '''
    if request.method == 'POST':
        post_data = request.get_json()
        quantum_computer = post_data.get('quantum_computer')
        qbit_count = post_data.get('qbit_count')
        places = post_data.get('places')

        response_object = {'status': 'success'}
        response_object['message'] = f'{qbit_count} qbits are working...'
    else:
        response_object['status'] = 'fail'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
