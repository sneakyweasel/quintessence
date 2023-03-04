'''Quantum circuit generation and execution.'''
import numpy as np
from qiskit import Aer, QuantumCircuit, transpile
from qiskit.circuit import Parameter
# from qiskit_ionq import IonQProvider  # pylint: disable=import-error

# Ignore divide by zero errors in console
np.seterr(divide='ignore')

# Load API keys from environment variables
QUANTUM_API_KEY = "123456"


def generate_quantum_circuit(places, steps):
    '''Generate the quantum circuit from the JSON data.'''

    # Retrieve probabilities
    probabilities = []
    for place in places:
        probabilities.append(place[1])

    # Quantum circuit variables
    start = 0
    probabilities[start] = 0
    j_val = np.pi / 10

    # Define Qiskit parameters
    qbit_count = len(probabilities)
    j = Parameter('J')
    k_i = []
    for i in range(qbit_count):
        k_i.append(Parameter('K_'+str(i)))

    # Define unitary
    qc_unitary = QuantumCircuit(qbit_count)
    qc_unitary.barrier()
    for i in range(qbit_count):
        qc_unitary.rz(k_i[i]/2, i)
    for i in range(qbit_count):
        if i % 2 == 0:
            qc_unitary.rxx(-j / 2, i % qbit_count, (i+1) % qbit_count)
            qc_unitary.ryy(-j / 2, i % qbit_count, (i+1) % qbit_count)
    for i in range(qbit_count):
        if i % 2 != 0:
            qc_unitary.rxx(-j, i % qbit_count, (i+1) % qbit_count)
            qc_unitary.ryy(-j, i % qbit_count, (i+1) % qbit_count)
    for i in range(qbit_count):
        if i % 2 == 0:
            qc_unitary.rxx(-j / 2, i % qbit_count, (i+1) % qbit_count)
            qc_unitary.ryy(-j / 2, i % qbit_count, (i+1) % qbit_count)
    for i in range(qbit_count):
        qc_unitary.rz(k_i[i]/2, i)

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
    qc_final = qc_final.bind_parameters({j: j_val})
    for ind in range(qbit_count):
        qc_final = qc_final.bind_parameters({k_i[ind]: probabilities[ind]})

    # Return the quantum circuit
    return qc_final


def run_quantum_circuit(quantum_circuit, quantum_computer):
    ''' Run the quantum circuit on the IonQ quantum computer. '''
    quantum_backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(quantum_circuit, quantum_backend)
    job = quantum_backend.run(transpiled_circuit)
    return job.result().get_counts()
