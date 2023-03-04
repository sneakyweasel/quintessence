''' Flask web application. '''
from flask_cors import CORS
from flask import Flask, jsonify, request
from quantum import generate_quantum_circuit, run_quantum_circuit
from result_processing import (filter_errors, add_missing_results, get_error_percentage,
                               order_results, convert_to_places, compute_entropy,
                               convert_entropy_to_words, create_gpt3_prompt)
from ai import retrieve_gpt3_response, convert_storyline_to_image_prompts

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
        steps = post_data.get('steps')
        places = post_data.get('places')
        activate_ai = post_data.get('activate_ai')
        qbit_count = len(places)

        # Create quantum circuit
        quantum_circuit = generate_quantum_circuit(places, steps)

        # Draw circuit and save to frontend public file
        # Error: breaks when running on server
        # quantum_circuit.draw(
        #   output='mpl',
        #   filename='../haze-frontend/public/circuit.png',
        #   vertical_compression=True
        # )

        # Run quantum computation
        simulator_results = run_quantum_circuit(quantum_circuit, quantum_computer)
        print(simulator_results)

        # Process results
        total_shots = sum(simulator_results.values())
        filtered_results = filter_errors(simulator_results)
        completed_results = add_missing_results(filtered_results, qbit_count)
        ordered_results = order_results(completed_results)
        readable_results = convert_to_places(
            ordered_results, places, total_shots
        )

        error_percentage = get_error_percentage(simulator_results)
        entropy_measure = compute_entropy(readable_results)

        # Create GPT3 prompt
        gpt3_prompt = create_gpt3_prompt(readable_results, entropy_measure)

        # Get GPT3 response and create image prompts
        if activate_ai:
            gpt3_response = retrieve_gpt3_response(gpt3_prompt)
            image_prompts = convert_storyline_to_image_prompts(gpt3_response)
        else:
            gpt3_response = ""
            image_prompts = []

        # Send response
        response_object = {'status': 'success'}
        response_object['message'] = {
            'raw_results': simulator_results,
            'results': readable_results,
            'error_percentage': error_percentage,
            'entropy': entropy_measure,
            'entropy_word': convert_entropy_to_words(entropy_measure),
            'gpt3_prompt': gpt3_prompt,
            'gpt3_response': gpt3_response,
            'image_prompts': image_prompts
        }

    else:
        response_object['status'] = 'fail'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
