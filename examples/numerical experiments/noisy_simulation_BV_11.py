"""
Noisy simulation of the 11-qubit Bernstein–Vazirani algorithm.
Calibration data are taken from [Benchmarking an 11-qubit quantum computer, Nature Communications 10, 5464 (2019)].
"""

import copy
from quantum.circuit import Circuit
from quantum.backends import Backend

# Single qubit gate fidelity
single_qubit_fidelity = {0: 0.9957, 1: 0.9962, 2: 0.9918, 3: 0.9925, 4: 0.9940, 5: 0.9946,
                         6: 0.9948, 7: 0.9955, 8: 0.9959, 9: 0.9964, 10: 0.9932}
# State preparation and measurement error
spam_fidelity = {0: 0.9931, 1: 0.9910, 2: 0.9930, 3: 0.9960, 4: 0.9930, 5: 0.9932,
                 6: 0.9927, 7: 0.9940, 8: 0.9894, 9: 0.9935, 10: 0.9930}
# Two-qubit gate fidelity
two_qubit_fidelity = [[1, 0.985, 0.977, 0.985, 0.972, 0.985, 0.969, 0.972, 0.987, 0.955, 0.971],
                      [0.985, 1, 0.977, 0.989, 0.982, 0.974, 0.978, 0.981, 0.984, 0.977, 0.979],
                      [0.977, 0.977, 1, 0.980, 0.975, 0.965, 0.984, 0.980, 0.972, 0.973, 0.960],
                      [0.985, 0.989, 0.980, 1, 0.964, 0.974, 0.971, 0.989, 0.960, 0.980, 0.977],
                      [0.972, 0.982, 0.975, 0.964, 1, 0.986, 0.973, 0.973, 0.983, 0.978, 0.965],
                      [0.985, 0.974, 0.965, 0.974, 0.986, 1, 0.965, 0.971, 0.984, 0.951, 0.967],
                      [0.969, 0.978, 0.984, 0.971, 0.973, 0.965, 1, 0.962, 0.972, 0.981, 0.982],
                      [0.972, 0.981, 0.980, 0.989, 0.973, 0.971, 0.962, 1, 0.973, 0.985, 0.973],
                      [0.987, 0.984, 0.972, 0.960, 0.983, 0.984, 0.972, 0.973, 1, 0.967, 0.970],
                      [0.955, 0.977, 0.973, 0.980, 0.978, 0.951, 0.981, 0.985, 0.967, 1, 0.975],
                      [0.971, 0.979, 0.960, 0.977, 0.965, 0.967, 0.982, 0.973, 0.970, 0.975, 1]]

# Logical qubits to physical qubits mapping for different qubit number
logical_physical_mappings = {'BV_11': {0: 3, 1: 0, 2: 2, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 1},
                             'BV_10': {0: 3, 1: 0, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 1},
                             'BV_9': {0: 3, 1: 0, 2: 4, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 1},
                             'BV_8': {0: 3, 1: 0, 2: 4, 3: 6, 4: 7, 5: 8, 6: 9, 7: 1},
                             'BV_7': {0: 3, 1: 0, 2: 4, 3: 7, 4: 8, 5: 9, 6: 1},
                             'BV_6': {0: 3, 1: 0, 2: 4, 3: 7, 4: 9, 5: 1},
                             'BV_5': {0: 3, 1: 0, 2: 7, 3: 9, 4: 1},
                             'BV_4': {0: 3, 1: 0, 2: 7, 3: 1},
                             'BV_3': {0: 3, 1: 0, 2: 1},
                             'BV_2': {0: 3, 1: 1}}


def add_noise(circuit, mapping) -> "Circuit":
    r"""Add depolarizing noise to each quantum operation in the circuit
    based on the mapping from logical qubits to physical qubits.

    Args:
        circuit(Circuit): noiseless quantum circuit
        mapping(dict): logical qubits to physical qubits mapping

    Returns:
        Circuit: noisy quantum circuit
    """
    noisy_gate_history = []  # noisy circuit instruction list
    for gate in circuit.gate_history:
        if len(gate['which_qubit']) == 1:  # single-qubit operation
            logical_qubit = gate['which_qubit'][0]  # get the logical qubit of the gate
            physical_qubit = mapping[logical_qubit]  # get the corresponding physical qubit
            if gate['name'] == 'r':  # reset operation
                # Calculate the state preparation error rate of the physical qubit
                error_rate = 1 - spam_fidelity[physical_qubit]
                # Add a noise to the reset operation
                noisy_gate_history.append(gate)
                noisy_gate_history.append({'name': 'depolarizing', 'which_qubit': [logical_qubit],
                                           'signature': None, 'prob': error_rate})
            elif gate['name'] == 'm':  # measurement operation
                # Calculate the measurement error rate of the physical qubit
                error_rate = 1 - spam_fidelity[physical_qubit]
                # Add a noise to the measurement
                noisy_gate_history.append({'name': 'depolarizing', 'which_qubit': [logical_qubit],
                                           'signature': None, 'prob': error_rate})
                noisy_gate_history.append(gate)
            else:  # other single-qubit gate
                # Calculate the single-qubit gate error rate of the physical qubit
                error_rate = 1 - single_qubit_fidelity[physical_qubit]
                # Add a noise to the single-qubit gate
                noisy_gate_history.append(gate)
                noisy_gate_history.append({'name': 'depolarizing', 'which_qubit': [logical_qubit],
                                           'signature': None, 'prob': error_rate})
        else:  # two-qubit gate
            logical_qubits = gate['which_qubit']
            # Get the corresponding physical qubits
            physical_qubit_0 = mapping[logical_qubits[0]]
            physical_qubit_1 = mapping[logical_qubits[1]]
            # Calculate the corresponding two-qubit gate error rate
            error_rate = 1 - two_qubit_fidelity[physical_qubit_0][physical_qubit_1]
            # Add depolarizing noise to the two-qubit gate
            noisy_gate_history.append(gate)
            noisy_gate_history.append({'name': 'depolarizing', 'which_qubit': [logical_qubits[0]],
                                       'signature': None, 'prob': error_rate})
            noisy_gate_history.append({'name': 'depolarizing', 'which_qubit': [logical_qubits[1]],
                                       'signature': None, 'prob': error_rate})

    circuit._history = noisy_gate_history

    return circuit


def reduce_to_given_size(circuit, target_size) -> "Circuit":
    r"""Compile the 11-qubit Bernstein-Vazirani circuit into
    an equivalent dynamic circuit with the specified number of qubits.

    Args:
        circuit(Circuit): the 11-qubit Bernstein-Vazirani circuit
        target_size(int): the specified number of qubits

    Returns:
        Circuit: Bernstein-Vazirani circuit with specified number of qubits
    """
    # Make a copy of the input circuit
    compiled_circuit = copy.deepcopy(circuit)
    # Convert the static quantum circuit to its DAG representation
    graph, roots, terminals = compiled_circuit.to_dag(reset=False)
    # All edges corresponding to the optimal compilation
    optimal_edges = [(terminals[k], roots[k + 1]) for k in range(circuit.width - 2)]
    # Get all the added edges in order to compile the circuit to the target size
    added_edges = optimal_edges[:circuit.width - target_size]
    graph.add_edges_from(added_edges)
    # Convert the modified DAG to a dynamic quantum circuit
    compiled_circuit._reorder_by_dag(graph, added_edges)
    compiled_circuit.remap_indices(print_index=False)

    return compiled_circuit


# Set the secret string encoded in the function to 10-bit all-one string
secret_string = "1111111111"
# The number of qubits
qubit_num = len(secret_string) + 1
# The simulation shots
shots = 10000

# Create a quantum circuit
cir = Circuit("Bernstein-Vazirani algorithm")

# State initialization
for i in range(qubit_num):
    cir.reset(i)
# Apply Hadamard gates before the oracle
for i in range(qubit_num - 1):
    cir.h(i)
# Put the auxiliary qubit in the minus state
cir.x(qubit_num - 1)
cir.h(qubit_num - 1)
# Implement the quantum oracle for the hidden string
for i in range(len(secret_string)):
    if secret_string[i] == "1":
        cir.cx([i, qubit_num - 1])
# Apply another layer of Hadamard gates
for i in range(qubit_num - 1):
    cir.h(i)
# Measure all qubits
for i in range(qubit_num):
    cir.measure(i, mid=str(i))
# Set 'output_ids' for the final sampling results
cir.output_ids = [str(i) for i in range(qubit_num - 1)]
# Run simulation of the noiseless circuit
noiseless_count = cir.run(shots=shots, backend=Backend.StateVector)['counts'][secret_string]


# Gradually reduce the number of qubits from 11 to 2
for size in range(11, 1, -1):
    # Compile the circuit to the given size
    compiled_cir = reduce_to_given_size(cir, size)
    if size == 4:  # reorder the qubit index in the BV_4 circuit
        compiled_cir.remap_indices(remap={0: 0, 1: 1, 2: 3, 3: 2})
    # Plot the circuit
    compiled_cir.print_circuit()
    # Add noise to the circuit
    noisy_cir = add_noise(compiled_cir, logical_physical_mappings['BV_' + str(size)])
    # Run simulation of the noisy circuit
    noisy_count = noisy_cir.run(shots=shots, backend=Backend.DensityMatrix)['counts']
    # Print the simulation result
    print('BV_' + str(size), 'probability of obtaining the correct outcome',
          noisy_count[secret_string] / noiseless_count)
