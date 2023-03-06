'''Quantum circuit generation and execution.'''
import numpy as np
from qiskit import Aer, QuantumCircuit, execute
from qiskit.circuit import Parameter
from qiskit_aer.noise import depolarizing_error, NoiseModel
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


def run_quantum_circuit(quantum_circuit, quantum_computer, activate_noise=False):
    ''' Run the quantum circuit on the IonQ quantum computer. '''
    backend = Aer.get_backend('aer_simulator')

    # Get coupling map from backend
    coupling_map = backend.configuration().coupling_map

    # Create an empty noise model
    noise_model = NoiseModel()

    # Add depolarizing error to all single qubit u1, u2, u3 gates
    if activate_noise:
        error = depolarizing_error(0.001, 1)
    else:
        error = depolarizing_error(0, 1)
    noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

    # Get basis gates from noise model
    basis_gates = noise_model.basis_gates

    # Run quantum circuit
    result = execute(quantum_circuit, backend,
                 coupling_map=coupling_map,
                 basis_gates=basis_gates,
                 noise_model=noise_model).result()
    
    return result.get_counts()
