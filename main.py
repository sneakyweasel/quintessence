# import packages
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit_ionq import IonQProvider
import numpy as np
from flask import Flask
app = Flask(__name__)

#this will be the url
class CircuitSpec:

    def __init__(self, start, steps, speed, likelyhood, backend):
        self.start = start #starting site
        self.steps = steps  #number of trotter steps
        self.speed = speed
        self.likelyhood = likelyhood
        self.backend = backend
        # Depends on the configuration of the application.


    def random_walk(self):        
        L = len(self.likelyhood)
        #Define Parameters
        J = Parameter('J')
        K_i = []
        for ind in range(L):
            K_i.append(Parameter('K_'+str(ind)))
        #Define Unitary
        qc_U = QuantumCircuit(L)
        for i in range(L):
            qc_U.rz(K_i[i]/2, i)
        for i in range(L):
            if i % 2 == 0:
                qc_U.rxx(-J/2, i%L, (i+1)%L)
                qc_U.ryy(-J/2, i%L, (i+1)%L)
        for i in range(L):
            if i % 2 != 0:
                qc_U.rxx(-J, i%L, (i+1)%L)
                qc_U.ryy(-J, i%L, (i+1)%L)
        for i in range(L):
            if i % 2 == 0:
                qc_U.rxx(-J/2, i%L, (i+1)%L)
                qc_U.ryy(-J/2, i%L, (i+1)%L)
        for i in range(L):
            qc_U.rz(K_i[i]/2, i)
        #Compose Main Circuit with set number of Unitary steps:
        qc_main = QuantumCircuit(L)
        qc_main.x(self.start)
        for step in range(self.steps):
            qc_main = qc_main.compose(qc_U, qubits=range(L))
        #Add Measurement Circuit
        qc_meas = QuantumCircuit(L,L)
        qc_meas.measure_all(add_bits=False)
        qc_end = qc_main.compose(qc_meas, range(L))
        #Bind Parameters
        qc_end = qc_end.bind_parameters({J:self.speed})
        for ind in range(L):
            qc_end = qc_end.bind_parameters({K_i[ind]:self.likelyhood[ind]})
        #Transpile and Run
        trans_circ = transpile(qc_end, self.backend)
        job = self.backend.run(trans_circ)
        #Return the counts for the jobs
        return job.result().get_counts()

@app.route('/')
def full_circ_instance():
    #provider
    provider = IonQProvider("tQgNZln2nI3JSOg7hZhRXjSJHYfgrS2S")
    provider.backends()
    backend = provider.get_backend("ionq_simulator")

    start = 0
    K_vals = np.zeros(12)
    steps = 30
    K_vals[0] = +np.pi/2
    J_val = np.pi/10
    run = CircuitSpec(start, steps, J_val, K_vals, backend)
    final_vals = run.random_walk()

    return final_vals

    
if __name__ == "__main__":
    app.run()
