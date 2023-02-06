'''Main file for the application.'''

# import os
import time

import numpy as np
import openai
import requests
from flask import Flask
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit_ionq import IonQProvider

from polar_plot import entropy, polar_plot_maker

# Load API keys from environment variables
OPENAI_API_KEY = ""
QUANTUM_API_KEY = ""

PLACES = [
    "A rooftop bar",
    "A comedy club",
    "A concert venue",
    "A music festival",
    "A street fair",
    "A bowling alley",
    "A casino",
    "A sports stadium",
    "A karaoke bar",
    "A restaurant with live music",
    "A rooftop terrace",
    "A beach bonfire",
    "A drive-in movie theater",
    "A laser tag arena",
    "A trampoline park",
    "An escape room",
    "A miniature golf course",
    "A rock climbing gym",
    "A go-kart track",
    "A bowling alley",
    "A comedy club",
    "A concert hall",
    "A music festival",
    "A street festival",
    "A rooftop pool",
    "A rooftop garden",
    "A lounge",
    "A dance club",
    "A public square",
    "A rooftop yoga class"
]

# Create the Flask app
app = Flask(__name__)


class CircuitSpec:
    '''Class for the circuit specification.'''

    def __init__(self, start, steps, speed, likelyhood, backend):
        self.start = start  # starting site
        self.steps = steps  # number of trotter steps
        self.speed = speed
        self.likelyhood = likelyhood  # that's the K values
        # Depends on the configuration of the application.
        self.backend = backend

    def random_walk(self):
        '''Method to create the quantum circuit.'''
        L = len(self.likelyhood)

        # Define Parameters
        J = Parameter('J')
        K_i = []
        for ind in range(L):
            K_i.append(Parameter('K_'+str(ind)))

        # Define Unitary
        qc_U = QuantumCircuit(L)
        for i in range(L):
            qc_U.rz(K_i[i]/2, i)
        for i in range(L):
            if i % 2 == 0:
                qc_U.rxx(-J/2, i % L, (i+1) % L)
                qc_U.ryy(-J/2, i % L, (i+1) % L)
        for i in range(L):
            if i % 2 != 0:
                qc_U.rxx(-J, i % L, (i+1) % L)
                qc_U.ryy(-J, i % L, (i+1) % L)
        for i in range(L):
            if i % 2 == 0:
                qc_U.rxx(-J/2, i % L, (i+1) % L)
                qc_U.ryy(-J/2, i % L, (i+1) % L)
        for i in range(L):
            qc_U.rz(K_i[i]/2, i)

        # Compose Main Circuit with set number of Unitary steps:
        qc_main = QuantumCircuit(L)
        qc_main.x(self.start)
        for step in range(self.steps):
            qc_main = qc_main.compose(qc_U, qubits=range(L))

        # Add Measurement Circuit
        qc_meas = QuantumCircuit(L, L)
        qc_meas.measure_all(add_bits=False)
        qc_end = qc_main.compose(qc_meas, range(L))

        # Bind Parameters
        qc_end = qc_end.bind_parameters({J: self.speed})
        for ind in range(L):
            qc_end = qc_end.bind_parameters({K_i[ind]: self.likelyhood[ind]})

        # Transpile and Run
        trans_circ = transpile(qc_end, self.backend)
        job = self.backend.run(trans_circ)

        # Return the counts for the jobs
        return job.result().get_counts()


def full_circuit_instance(sim_type, nb_qubits, start, steps, activate_ai, verbose=False):
    ''' Method to create the full circuit instance. '''

    provider = IonQProvider(QUANTUM_API_KEY)

    if sim_type == 'ideal':
        provider.backends()
        backend = provider.get_backend("ionq_simulator")
    elif sim_type == 'noisy':
        pass
    elif sim_type == 'hardware':
        pass

    # open json file.
    # places - a list of strings
    # probs - a list of strings (a number)
    # start - a number (the index)
    # data = request.json
    # list_places = data.get['places']
    # list_probs = data.get['prob']

    # We should implement a unique choice of places
    list_places = np.random.choice(PLACES, nb_qubits, replace=False)
    list_probs = np.zeros(nb_qubits)
    list_probs[np.random.randint(nb_qubits)] = np.pi / 4

    k_max = np.pi / 4
    k_vals = np.zeros(len(list_probs))

    # parse into numerical values the probs array
    for count, j in enumerate(list_probs):
        k_vals[j] = k_max*int(list_probs[j])/100.0

    j_val = np.pi / 4  # set a default speed value
    circuit = CircuitSpec(start, steps, j_val, k_vals, backend)
    final_vals = circuit.random_walk()

    if verbose:
        print("\n")
        print("Bitstring results and shot number out of 1024 total shots")
        print(final_vals)
        print("\n")

    # feed final_vals into Rob's cleanup function
    processed_vals, active_sites = clean_results(final_vals, n_walkers=1)
    # print(processed_vals)

    list_of_likelyhood = find_likelyhood_strings(processed_vals)
    # print(list_of_likelyhood)

    # get entropy from results
    entropy_specifier = wording_entropy(
        entropy(processed_vals), max_val=np.log(len(list_probs)))

    # feed resulting array into Gavin's plotting object
    # do not take into account the last value for the plot - that's the Errors!
    polar_plot_maker(
        processed_vals,
        labels=list_places,
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
    # this takes into
    # list_places
    # processed_vals
    # saves picture into haze-frontend/public/roseplot.png

    if activate_ai:

        # feed into openai function
        storyline = gpt_prompt_and_eval(
            list_places,
            list_of_likelyhood[:-1],
            active_sites[:-1],
            entropy_specifier,
            list_places[start]
        )
        print(storyline)

        time.sleep(5)

        # clean storyline into 3 separated paragraphs
        # feed into Dall-E API

        # image_from_response(storyline)


def clean_results(counts, n_walkers, verbose=False):
    '''Method to clean the results from the quantum computer.'''
    if verbose:
        print(f'Number of possible end states: {len(counts)}')
    shots = 0
    length_qubits = 0
    for key in counts.keys():
        shots += counts.get(key)
        length_qubits = len(key)
    walkers = {}
    extras = {}
    for key in counts.keys():
        totes = 0
        for l in key:
            if l == '1':
                totes += 1
            else:
                pass
        if totes == n_walkers:
            walkers[key] = counts.get(key)
        else:
            extras[key] = counts.get(key)
    if verbose:
        print(f'Number of walkers: {n_walkers}')
        print(f'Number of {n_walkers} occurences: {len(walkers)}')
        print(f'Number of extra occurences: {len(extras)}')
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
    if verbose:
        print(f'Number of {n_walkers} walkers states: {len(walkers)}')
    totes_walkers_prob = 0
    for key in walkers_prob:
        totes_walkers_prob += walkers_prob.get(key)
    if verbose:
        print(f'Probability of {n_walkers} walkers: {totes_walkers_prob}')
        print(f'Probability of errors: {error_prob}')
        print(
            f'(Sanity check) Total Probability: {totes_walkers_prob + error_prob}')
    final_states = {}
    for key in walkers_prob:
        if walkers_prob.get(key) != 0:
            final_states[key] = walkers_prob.get(key)
    if verbose:
        print(f'Number of {n_walkers} walkers states: {len(walkers)}')
        print(
            f'Number of {n_walkers} walkers non-zero probability states: {len(final_states)}')
    final_states['Error'] = error_prob
    sites_list = []
    sites_prob = []
    active_sites = []
    for key in final_states:
        sites_list.append(key)
    ordered = sorted(sites_list)
    if verbose:
        print(f'Ordered sites list: {ordered}')
        print('='*149)
    for i in ordered:
        sites_prob.append(final_states.get(i))

    site = '1'

    active_sites = []
    for i in enumerate(sites_list):
        active_sites.append(np.abs(sites_list[i].rfind(site)-length_qubits))

    if verbose:
        print(f'Ordered sites probabilities: {sites_prob}')
    return sites_prob, active_sites


def find_likelyhood_strings(array):
    ''' Method to convert probabilities to likelyhoods strings.'''
    possibilities = [0, "may have gone ",  "likely went "]
    # this can be changed
    list_of_likelyhood = []
    for ua in array:
        if 0 <= ua < 0.25:
            ind = 0
        elif 0.25 <= ua < 0.75:
            ind = 1
        elif 0.75 <= ua < 1.0:
            ind = 2
        # append to list
        list_of_likelyhood.append(possibilities[ind])
    return list_of_likelyhood


def wording_entropy(entropy_val, max_val):
    '''Convert the entropy value to a word.'''
    possibilities = ["uneventful", "boring", "regular", "exciting", "chaotic"]
    normed_entropy = entropy_val/max_val
    if 0 <= normed_entropy < 0.1:
        ind = 0
    elif 0.1 <= normed_entropy < 0.4:
        ind = 1
    elif 0.4 <= normed_entropy < 0.6:
        ind = 2
    elif 0.6 <= normed_entropy < 0.9:
        ind = 3
    elif 0.9 <= normed_entropy < 1.0:
        ind = 4

    return possibilities[ind]


def gpt_prompt_and_eval(input_places, input_probs, tags, entropy_specifier, initial_state):
    ''' GPT-3 prompt and evaluation method.'''
    # entropy_specifier = "chaotic"
    # initial_state = "gutter"
    prompt_init = '''Mr. Quanta cannot remember how he got here. Tell the story of him trying to
                     remember how he got here in 3 steps and be descriptive.
                    He only remembers a few things, and considers each possible place one at a time. 
                    Use grandiose language. Embelish everything and paint a picture with words. 
                    Make the descriptions drip with imagery. '''
    prompt_init += f"He had a {entropy_specifier} time before "
    prompt_init += f"awakening at the { initial_state }, and before that"

    # Probabilities array as text
    # input_places = ["bar", "zoo"]
    # input_strings = ["unlikely", "likely"]
    lvals = len(input_probs)
    for i in range(lvals):
        if input_probs[i] != 0:
            prompt_init += ", he " + \
                input_probs[i] + " went to the " + input_places[tags[i]]

    prompt_init += "."

    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt_init, temperature=0, max_tokens=400)

    file = open("./haze-frontend/public/response.txt", "w", encoding="utf-8")
    file.write(response.choices[0].text)
    file.close()

    return response.choices[0].text


def image_from_response(storyline):
    ''' Method to create images from the GPT-3 response. '''
    # split the text
    prepro = storyline.split('\n')
    # print(prepro)
    processed = []
    for i in enumerate(prepro):
        if len(prepro[i]) > 20:
            processed.append(prepro[i])

    pre_prompt = "Digital art in the style of retrowave."

    img_urls = []
    for step in enumerate(processed):

        img = openai.Image.create(
            prompt=pre_prompt + processed[step], n=1, size="1024x1024")
        img_url = img["data"][0]["url"]
        print(img_url)
        img_urls.append(img_url)

        img_data = requests.get(img_url, timeout=10).content
        with open('./haze-frontend/public/pic'+str(step)+'.png', 'wb') as handler:
            handler.write(img_data)
        time.sleep(5)

# @app.route('/api', methods = ['POST'])
# @app.route('/')


if __name__ == "__main__":

    full_circuit_instance(sim_type='ideal',
                          nb_qubits=12, start=3, steps=2, activate_ai=True, verbose=True)
