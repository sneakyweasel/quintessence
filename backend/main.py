''' Flask web application. '''
import os
from flask_cors import CORS
from flask import Flask, jsonify, request
# pylint: disable=import-error
from quantum import generate_quantum_circuit, run_quantum_circuit
from result_processing import (filter_errors, add_missing_results, get_error_percentage,
                               order_results, convert_to_places, compute_entropy,
                               convert_entropy_to_words, create_gpt3_prompt)
from ai import retrieve_gpt3_response, convert_storyline_to_image_prompts
# pylint: enable=import-error

# Instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

# Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Sanity check route
@app.route("/")
def hello():
    ''' Sanity check route '''
    return "Python flask server is running! :D"

# Lauch quantum comic generation
@app.route('/generate', methods=['POST'])
def generate():
    ''' Generate the quantum comic '''
    if request.method == 'POST':
        # Retrieve data
        post_data = request.get_json()
        quantum_backend = post_data.get('quantum_backend')
        steps = post_data.get('steps')
        jval = post_data.get('jval')
        raw_places = post_data.get('places')
        activate_ai = post_data.get('activate_ai')
        activate_noise = post_data.get('activate_noise')
        qbit_count = len(raw_places)

        # Slice places to get only the names and percentages
        places = []
        for _i, place in enumerate(raw_places):
            places.append( [place[0], place[2]] )

        # Create quantum circuit
        quantum_circuit = generate_quantum_circuit(places, steps, jval)

        # Run quantum computation
        print(quantum_backend)
        simulator_results = run_quantum_circuit(quantum_circuit, quantum_backend, activate_noise)

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
            'ordered_results': ordered_results,
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
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
