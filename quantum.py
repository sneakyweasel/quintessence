'''Main file for the application.'''
import time
import numpy as np
import openai
import requests
from qiskit import Aer, QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit_ionq import IonQProvider  # pylint: disable=import-error
from polar_plot import entropy, polar_plot_maker

# Ignore divide by zero errors in console
np.seterr(divide='ignore')

# Load API keys from environment variables
OPENAI_API_KEY = "123456"
QUANTUM_API_KEY = "123456"

# Constants
VERBOSE = True


def generate_quantum_circuit(json_data):
    '''Generate the quantum circuit from the JSON data.'''

    # Retrieve probabilities
    probabilities = []
    for place in json_data['places']:
        probabilities.append(place['probability'])

    # Quantum circuit variables
    start = 0
    probabilities[start] = 0
    steps = 1
    J_val = np.pi / 10

    # Define Qiskit parameters
    qbit_count = len(probabilities)
    J = Parameter('J')
    K_i = []
    for i in range(qbit_count):
        K_i.append(Parameter('K_'+str(i)))

    # Define unitary
    qc_unitary = QuantumCircuit(qbit_count)
    qc_unitary.barrier()
    for i in range(qbit_count):
        qc_unitary.rz(K_i[i]/2, i)
    for i in range(qbit_count):
        if i % 2 == 0:
            qc_unitary.rxx(-J / 2, i % qbit_count, (i+1) % qbit_count)
            qc_unitary.ryy(-J / 2, i % qbit_count, (i+1) % qbit_count)
    for i in range(qbit_count):
        if i % 2 != 0:
            qc_unitary.rxx(-J, i % qbit_count, (i+1) % qbit_count)
            qc_unitary.ryy(-J, i % qbit_count, (i+1) % qbit_count)
    for i in range(qbit_count):
        if i % 2 == 0:
            qc_unitary.rxx(-J/2, i % qbit_count, (i+1) % qbit_count)
            qc_unitary.ryy(-J/2, i % qbit_count, (i+1) % qbit_count)
    for i in range(qbit_count):
        qc_unitary.rz(K_i[i]/2, i)

    # Compose main quantum circuit by duplicating the unitary circuit every step
    qc_main = QuantumCircuit(qbit_count)
    qc_main.x(start)
    for i in range(steps):
        qc_main = qc_main.compose(qc_unitary, qubits=range(qbit_count))

    # Add measurement circuit
    qc_measure = QuantumCircuit(qbit_count, qbit_count)
    qc_measure.measure_all(add_bits=False)
    qc_final = qc_main.compose(qc_measure, range(qbit_count))

    # Bind Qiskit parameters
    qc_final = qc_final.bind_parameters({J: J_val})
    for ind in range(qbit_count):
        qc_final = qc_final.bind_parameters({K_i[ind]: probabilities[ind]})

    # Return the quantum circuit
    return qc_final


def run_quantum_circuit(quantum_circuit):
    ''' Run the quantum circuit on the IonQ quantum computer. '''
    quantum_backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(quantum_circuit, quantum_backend)
    job = quantum_backend.run(transpiled_circuit)
    return job.result().get_counts()


def clean_quantum_results(simulator_result, n_walkers=1):
    '''Method to clean the results from the quantum computer.'''
    shots = 0
    length_qubits = 0

    for key in simulator_result.keys():
        shots += simulator_result.get(key)
        length_qubits = len(key)
    walkers = {}
    extras = {}

    for key in simulator_result.keys():
        totes = 0
        for i in key:
            if i == '1':
                totes += 1
            else:
                pass
        if totes == n_walkers:
            walkers[key] = simulator_result.get(key)
        else:
            extras[key] = simulator_result.get(key)

    walkers_prob = {}
    error_prob = 0
    for key in walkers:

        if walkers.get(key) is None:
            walkers_prob[key] = 0
        else:
            walkers_prob[key] = walkers.get(key) / shots
    extras_count = 0
    for key in extras:
        if extras.get(key) is None:
            extras_count += 0
        else:
            extras_count += extras.get(key)
    error_prob = extras_count / shots

    totes_walkers_prob = 0
    for key in walkers_prob:
        totes_walkers_prob += walkers_prob.get(key)

    final_states = {}
    for key in walkers_prob:
        if walkers_prob.get(key) != 0:
            final_states[key] = walkers_prob.get(key)

    final_states['Error'] = error_prob
    sites_list = []
    sites_prob = []
    active_sites = []
    for key in final_states:
        sites_list.append(key)
    ordered = sorted(sites_list)
    for i in ordered:
        sites_prob.append(final_states.get(i))

    site = '1'

    active_sites = []
    for i, obj in enumerate(sites_list):
        active_sites.append(np.abs(obj.rfind(site) - length_qubits))

    if VERBOSE:
        print(f'Active sites list: {active_sites}')
        print(f'Ordered sites list: {ordered}')
        print(f'Ordered sites probabilities: {sites_prob}')
    return sites_prob, active_sites


def convert_probs_to_words(probs):
    ''' Method to convert probabilities to likelyhoods strings.'''
    probability_strings = [
        "wasn't at ",
        "may have gone ",
        "likely went "
    ]
    list_of_likelyhood = []
    # Can be seriously improved...
    for prob in probs:
        if 0 <= prob < 0.25:
            i = 0
        elif 0.25 <= prob < 0.75:
            i = 1
        elif 0.75 <= prob < 1.0:
            i = 2
        list_of_likelyhood.append(probability_strings[i])
    return list_of_likelyhood


def convert_entropy_to_words(entropy_val, entropy_max):
    '''Convert the entropy value to a word.'''
    entropy_strings = [
        "uneventful",
        "boring",
        "regular",
        "exciting",
        "chaotic"
    ]
    normed_entropy = entropy_val / entropy_max
    if 0 <= normed_entropy < 0.1:
        i = 0
    elif 0.1 <= normed_entropy < 0.4:
        i = 1
    elif 0.4 <= normed_entropy < 0.6:
        i = 2
    elif 0.6 <= normed_entropy < 0.9:
        i = 3
    elif 0.9 <= normed_entropy < 1.0:
        i = 4
    return entropy_strings[i]


def create_gpt3_prompt(input_places, input_probs, tags, entropy_specifier, initial_state):
    '''Method to create the GPT-3 prompt.'''
    prompt = '''Mr. Quanta cannot remember how he got here. Tell the story of him trying to
                remember how he got here in 3 steps and be descriptive.
                He only remembers a few things, and considers each possible place one at a time. 
                Use grandiose language. Embelish everything and paint a picture with words. 
                Make the descriptions drip with imagery. '''
    prompt += f"He had a {entropy_specifier} time before "
    prompt += f"awakening at the { initial_state }, and before that"

    # Append probability strings in the prompt
    for i, prob in enumerate(input_probs):
        if prob != "wasn't at ":
            prompt += f', he {prob} went to the {input_places[tags[i]]}'
    prompt += "."

    return prompt


def retrieve_gpt3_result(prompt):
    ''' GPT-3 prompt and evaluation method.'''
    openai.api_key = OPENAI_API_KEY

    # Send the prompt to GPT-3
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=400
    )

    # Write the response to a local file
    file = open("./haze-frontend/public/response.txt", "w", encoding="utf-8")
    file.write(response.choices[0].text)
    file.close()

    if VERBOSE:
        print(response.choices[0].text)

    return response.choices[0].text


def convert_storyline_to_image_prompts(storyline):
    ''' Method to split the GPT-3 response into a list of steps.'''
    # Should use a map
    steps = storyline.split('\n')
    prompt_intro = "Digital art in the style of retrowave."
    image_prompts = []
    for step in steps:
        if len(step) > 20:
            image_prompts.append(prompt_intro + step)
    return image_prompts


def retrieve_image_from_dalle(image_prompt):
    ''' Method to create images from the GPT-3 response.'''

    # Retrieve DALLE image
    response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response["data"][0]["url"]
    return image_url


def save_image(img_url, index):
    '''Save image to local file.'''
    img_data = requests.get(img_url, timeout=10).content
    with open(f'./haze-frontend/public/pic{str(index)}.png', 'wb') as handler:
        handler.write(img_data)


def full_circuit_instance(start, steps, activate_ai):
    ''' Method to create the full circuit instance. '''

    # Example JSON data from the frontend
    json_data = {
        "computer": "ionq",  # quantum computer to use
        "qbit_count": 5,    # number of qubits to use
        "places": [         # list of places to visit and their probabilities
            {"place": "Gym", "probability": 0.2},
            {"place": "Opera", "probability": 0.2},
            {"place": "Rooftop bar", "probability": 0.2},
            {"place": "Street fair", "probability": 0.2},
            {"place": "Pool", "probability": 0.2},
        ]
    }

    # Load the correct quantum backend
    if json_data['computer'] == 'ionq':
        provider = IonQProvider(QUANTUM_API_KEY)
        provider.backends()
        backend = provider.get_backend("ionq_simulator")
    elif json_data['computer'] == 'qiskit':
        backend = provider.get_backend('ibmq_qasm_simulator')
        provider.backends()
    else:
        raise NameError("Unknown quantum backend.")

    # Create places and probabilities arrays
    places = []
    probabilities = []
    for place in json_data['places']:
        places.append(place['place'])
        probabilities.append(place['probability'])

    # Set a default speed value
    j_val = np.pi / 4

    # Scale the probabilities into k values
    k_max = np.pi / 4
    k_vals = np.zeros(len(probabilities))
    for i, prob in enumerate(probabilities):
        k_vals[i] = k_max * int(prob) / 100.0

    # Create quantum circuit instance
    circuit = generate_quantum_circuit(json_data)
    final_vals = circuit.random_walk()

    # feed final_vals into Rob's cleanup function
    processed_vals, active_sites = clean_results(final_vals, n_walkers=1)

    # convert probabilities into words
    list_of_likelyhood = convert_probs_to_words(processed_vals)

    # get entropy from results
    entropy_specifier = convert_entropy_to_words(
        entropy_val=entropy(processed_vals),
        entropy_max=np.log(len(probabilities))
    )

    if VERBOSE:
        print(list_of_likelyhood)
        print(processed_vals)
        print(
            f'Bitstring results and shot number out of 1024 total shots: {print(final_vals)}\n'
        )

    # feed resulting array into Gavin's plotting object
    # do not take into account the last value for the plot - that's the Errors!
    polar_plot_maker(
        processed_vals,
        labels=places,
        figsize=(5, 5),
        dpi=120,
        debug=False,
        tick_color='chartreuse',
        linelength=10,
        pad=8,
        save_name='./haze-frontend/public/roseplot',
        show=False,
        has_error=True,
        offwhite_cutoff=170,
    )

    # If AI is activated, we create the storyline and the images
    if activate_ai:

        # Create the prompt for GPT-3
        prompt = create_gpt3_prompt(
            places,
            list_of_likelyhood[:-1],
            active_sites[:-1],
            entropy_specifier,
            places[start]
        )

        # Get the storyline from GPT-3
        storyline = retrieve_gpt3_result(prompt)
        print(storyline)

        # Split the storyline into steps
        image_prompts = convert_storyline_to_image_prompts(storyline)

        # Get the images from DALL-E
        image_urls = []
        for i, prompt in enumerate(image_prompts):
            image_url = retrieve_image_from_dalle(prompt)
            image_urls.append(image_url)
            save_image(image_url, i)
            time.sleep(3)
        print(image_urls)
