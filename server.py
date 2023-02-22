''' Flask web application. '''
from flask_cors import CORS
from flask import Flask, jsonify, request
from quantum import generate_quantum_circuit, run_quantum_circuit, clean_quantum_results

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# Lauch quantum comic generation
@app.route('/generate', methods=['POST'])
def generate():
    ''' Generate the quantum comic '''
    if request.method == 'POST':
        # Retrieve data
        post_data = request.get_json()
        quantum_computer = post_data.get('quantum_computer')
        qbit_count = post_data.get('qbit_count')
        places = post_data.get('places')

        # Create quantum circuit
        quantum_circuit = generate_quantum_circuit(json_data=post_data)

        # Draw circuit
        # terminal_draw = str(quantum_circuit.draw(output='text', fold=1000))
        quantum_circuit.draw(
            output='mpl', filename='./circuit.png', vertical_compression=True)

        # Perform quantum computation
        simulator_result = run_quantum_circuit(quantum_circuit)
        cleaned_result = clean_quantum_results(simulator_result)
        print(simulator_result)
        print(cleaned_result)

        # Send response
        response_object = {'status': 'success'}
        response_object['message'] = simulator_result

    else:
        response_object['status'] = 'fail'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
