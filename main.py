# import packages
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit_ionq import IonQProvider
import numpy as np
from flask import Flask, request
import json
import os
import matplotlib.pylab as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
from scipy.stats import norm
#import openai

# Load your API key from an environment variable or secret management service
app = Flask(__name__)

# this will be the url


class CircuitSpec:
    def __init__(self, start, steps, speed, likelyhood, backend):
        self.start = start  # starting site
        self.steps = steps  # number of trotter steps
        self.speed = speed
        self.likelyhood = likelyhood
        self.backend = backend
        # Depends on the configuration of the application.

    def random_walk(self):
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

def Clean_Results(counts, n_walkers, verbose = False):
    if verbose:
        print(f'Number of possible end states: {len(counts)}')
    shots = 0
    for key in counts.keys():
        shots += counts.get(key)
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
    for key in walkers.keys():
        prob = 0
        if walkers.get(key) == None:
            walkers_prob[key] = 0
        else:
            walkers_prob[key] = walkers.get(key) / shots
    extras_count = 0
    for key in extras.keys():
        if extras.get(key) == None:
            extras_count += 0
        else:
            extras_count += extras.get(key)
    error_prob = extras_count / shots
    if verbose:
        print(f'Number of {n_walkers} walkers states: {len(walkers)}')
    totes_walkers_prob = 0
    for key in walkers_prob.keys():
        totes_walkers_prob += walkers_prob.get(key)
    if verbose:
        print(f'Probability of {n_walkers} walkers: {totes_walkers_prob}')
        print(f'Probability of errors: {error_prob}')
        print(f'(Sanity check) Total Probability: {totes_walkers_prob + error_prob}')
    final_states = {}
    for key in walkers_prob.keys():
        if walkers_prob.get(key) != 0:
            final_states[key] = walkers_prob.get(key)
    if verbose:
        print(f'Number of {n_walkers} walkers states: {len(walkers)}')
        print(f'Number of {n_walkers} walkers non-zero probability states: {len(final_states)}')
    final_states['Error'] = error_prob
    sites_list = []
    sites_prob = []
    for key in final_states.keys():
        sites_list.append(key)
    ordered = sorted(sites_list)
    if verbose:
        print(f'Ordered sites list: {ordered}')
        print('='*149)
    for i in ordered:
        sites_prob.append(final_states.get(i))   
    if verbose:
        print(f'Ordered sites probabilities: {sites_prob}')
    return sites_prob

def find_likelyhood_strings(array):
    possibilities = ["certainly did not go", "unlikely went ", "may have gone ", "likely went ", "certainly went "]
    list_of_likelyhood = []
    for ua in array:
        if 0 <= ua < 0.1:
            ind = 0
        elif 0.1 <= ua < 0.4:
            ind = 1
        elif 0.4 <= ua < 0.6:
            ind = 2
        elif 0.6 <= ua < 0.9:
            ind = 3        
        elif 0.9 <= ua < 1.0:
            ind = 4
        #append to list
        list_of_likelyhood.append(possibilities[ind])
    return list_of_likelyhood

def wording_entropy(entropy_val, max_val):
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


def PolarPlotmaker(probabilities, labels=None, figsize = (5,5), dpi = 120, background = None, debug = False, tick_color = 'limegreen', linelength = 10, pad = 15, save_name = None):
    labels_type = 'string'
    N = len(probabilities)
    angles = np.linspace(0,2*np.pi-2*np.pi/N,N)
    
    angles = np.concatenate((angles,[angles[0]]))
    probabilities = np.concatenate((probabilities,[probabilities[0]]))

    if debug:
        print(f'Angles (length {len(angles)}): {np.round(angles,4)}')
        print(f'Probabilies (length {len(probabilities)}): {np.round(probabilities,4)}')

    
    if labels is not None:
        if len(labels)!=N:
            labels = np.arange(0,N)
            labels_type = 'int'
        

    if labels is None:
        labels = np.arange(0,N)
        labels_type = 'int'


    if labels_type == 'string':
        labels_modified = []
        for label in labels:
            new_label = ""
            lines = 1
            first_step = True
            for i, letter in enumerate(label):
                if lines == 3:
                    new_label = new_label[:-3]
                    new_label += '...'
                    break
                if i % linelength == 0 and not first_step:
                    lines+=1
                    if new_label[-1] != ' ':
                        new_label +='-'
                    new_label += '\n'
                new_label += letter
                first_step = False
            if new_label[:2] == "A " or new_label[:2] == "a ":
                new_label=new_label[2:]
            labels_modified.append(new_label)     

    plt.figure(figsize=figsize, dpi = dpi)
    
    ax = plt.subplot(111, polar=True)

    z = angles
    normalize = colors.Normalize(vmin=z.min(), vmax=z.max())

    cmap = colors.LinearSegmentedColormap.from_list("", ["aqua","mediumslateblue","orchid",'magenta', 'mediumorchid', 'mediumpurple','dodgerblue']*2)

    ax.plot(angles, probabilities, linewidth=1, linestyle='solid')
    
    # Fill area
    #ax.fill(angles, values, 'b', alpha=0.1)

    ax.set_yticklabels([])
    ax.get_yaxis().set_ticks([])

    for i in range(len(probabilities)-1):
        ax.fill_between([angles[i], angles[i+1]], [probabilities[i], probabilities[i+1]], color=cmap(normalize(z[i])))
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels_modified, color = tick_color)
    ax.xaxis.set_tick_params(grid_linewidth = 1, grid_color = tick_color, pad = pad)
    
    ax.spines['polar'].set_color(tick_color)
    
    ax.set_ylim(0,max(probabilities))

    ax.set_facecolor(background)


    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    # Show the graph
    plt.tight_layout()
    
    if type(save_name)==str:
        plt.savefig(save_name, transparent = True)
    #plt.show()
    


def gpt_prompt_and_eval(input_places, input_probs, entropy_specifier, initial_state):
    #entropy_specifier = "chaotic"
    #initial_state = "gutter"
    prompt_init = "Write a fiction story about Mr. Quanta's past journey in 3 steps. "
    prompt_init += "He only remembers a few things. "
    prompt_init += "He had a " + entropy_specifier + " time before awakening in the " + initial_state + ", before that"


    # Probabilities array as text
    #input_places = ["bar", "zoo"]
    #input_strings = ["unlikely", "likely"]
    lvals = len(input_places)
    for i in range(lvals):
        prompt_init += ", he " + input_probs[i] + " went to the " + input_places[i]

    prompt_init += "."

    response = openai.Completion.create(model="text-davinci-003", prompt=prompt_init, temperature=0, max_tokens=400)

    return response.choices[0].text


@app.route('/api', methods = ['POST'])
def full_circ_instance():
    # provider
    provider = IonQProvider("tQgNZln2nI3JSOg7hZhRXjSJHYfgrS2S")
    provider.backends()
    backend = provider.get_backend("ionq_simulator")

    #open json file.
    #places - a list of strings
    #probs - a list of strings (a number)
    #start - a number (the index)
    data = request.json
    list_places = data.get['places']
    list_probs = data.get['prob']
    
    #parse into numerical values the probs array
    for j in range(len(list_probs)):
        K_vals = int(list_probs[j])/100.0

    start = 0
    #start = data.get['start']
    steps = 30
    #steps = data.get['steps']
    J_val = np.pi/4 #set a default speed value
    circuit = CircuitSpec(start, steps, J_val, K_vals, backend)
    final_vals = circuit.random_walk()

    #feed final_vals into Rob's cleanup function

    processed_vals = Clean_Results(final_vals, n_walker = 1)

    list_of_likelyhood = find_likelyhood_strings(processed_vals[:-1])
    entropy_specifier = wording_entropy(entropy_val, max_val = np.log(12))

    #feed resulting array into Gavin's plotting object

    #do not take into account the last value for the plot - that's the Errors!
    PolarPlotmaker(processed_vals[:-1], labels = list_places,debug = False, background='black', tick_color='chartreuse', save_name='./assets/roseplot.png', dpi = 200)
    #this takes into
    #list_places
    #processed_vals
    #saves picture into assets/roseplot.png

    #feed into openai function
    #create json ["story"] of final GPT3 result
    #send that back to the API
    storyline = gpt_prompt_and_eval(list_places, processed_vals[:-1], entropy_specifier)
    print(storyline)


if __name__ == "__main__":
    app.run()
