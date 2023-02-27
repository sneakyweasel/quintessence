''' Flask web application. '''
from flask_cors import CORS
from flask import Flask, jsonify, request
from quantum import generate_quantum_circuit, run_quantum_circuit
from result_processing import filter_errors, get_error_percentage, order_results, convert_to_places, convert_probability_to_likelyhood, compute_entropy

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
        # quantum_circuit.draw(
        #     output='mpl', filename='./circuit.png', vertical_compression=True)

        # Perform quantum computation
        simulator_result = run_quantum_circuit(quantum_circuit)
        print(simulator_result)

        # Process results
        total_shots = sum(simulator_result.values())
        filtered_result = filter_errors(simulator_result)
        ordered_result = order_results(filtered_result)
        readable_result = convert_to_places(
            ordered_result, places, total_shots
        )
        # error_percentage = get_error_percentage(simulator_result)
        # entropy = compute_entropy(readable_result)

        # Send response
        response_object = {'status': 'success'}
        response_object['message'] = readable_result

    else:
        response_object['status'] = 'fail'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
