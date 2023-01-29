# import packages
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit_ionq import IonQProvider
import numpy as np
from flask import Flask, request
import json
import os
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

def wording_entropy(entropy_val):


def gpt_prompt_and_eval(input_places, input_probs, entropy_specifier):

    # Initial prompt text
    prompt_init = "Write a fiction story about Mr. Quanta's journey in 5 paragraphs. "
    prompt_init += "He had a " + entropy_specifier + " time going around QuantaLand."
    prompt_init += " night out. The main character lost all memory of what he did and tries to figure out what he did the previous night. Provide a 5 steps story about his drunken journey. He woke up in the hospital." 

    # Probabilities array as text
    input_places = ["bar", "zoo"]
    input_strings = ["unlikely", "likely"]
    lvals = len(input_strings) - 1
    for i in range(lvals):
        prompt_init += " He " + input_probs[i] + " went to the " + input_places[i] + "."

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
    run = CircuitSpec(start, steps, J_val, K_vals, backend)
    final_vals = run.random_walk()

    #feed final_vals into Rob's cleanup function

    #processed_vals = 

    list_of_likelyhood = find_likelyhood_strings(processed_vals)

    #feed resulting array into Gavin's plotting object
    #this takes into
    #list_places
    #processed_vales
    #saves picture into assets/roseplot.png

    #feed into openai function
    #create json ["story"] of final GPT3 result
    #send that back to the API



    return final_vals


if __name__ == "__main__":
    app.run()
