"""
Numerical experiments of the random instantaneous quantum polynomial (IQP) circuits.
"""

# IQP circuits take the form of H^n D H^n where H denotes the hadamard gate
# and D constitutes a block of gates diagonal in the computational basis.
# e.g. The block circuit D can be constructed by randomly selecting gates from the set {√CZ, T}
# Consequently, the gates within the block circuit D can be applied in any temporal order.

import math
import random
from quantum.circuit import Circuit


def random_iqp_circuits(num_qubit, num_gate) -> "Circuit":
    r"""Generate a random IQP circuit with the specified number of qubits and two-qubit gates.

    Args:
        num_qubit(int): the number of qubits in the random IQP circuit
        num_gate(int): the number of two-qubit gates in the random IQP circuit

    Returns:
        Circuit: a random IQP circuit
    """
    # Create a quantum circuit
    circuit = Circuit()
    # Add a layer of Hadamard gates
    for i in range(num_qubit):
        circuit.h(i)
    # Randomly generate the block circuit D
    # Here we omit all single-qubit gates and only employ CZ gates to construct the block circuit
    for j in range(num_gate):
        qubit = random.sample(range(num_qubit), 2)
        circuit.cz(qubit)
    # Add another layer of Hadamard gates
    for i in range(num_qubit):
        circuit.h(i)
    # Measure all qubits
    circuit.measure()

    # Add group tags for all commutable CZ gates
    for gate in circuit.gate_history:
        if gate['name'] == 'cz':
            gate['group_tag'] = 'z_group'
        else:
            gate['group_tag'] = None

    return circuit


# Set the number of random IQP circuits
run_times = 10
# Set the random shots for the random greedy algorithm
random_shots = 5
# Set the ratio between the number of two-qubit gates and qubits
gate_qubit_ratio = 2


for t in range(run_times):
    # Randomly select a qubit number between 10 and 40
    qubit_num = random.randint(10, 40)

    # Calculate the number of two-qubit gates
    gate_num = math.floor(qubit_num * gate_qubit_ratio)

    # Generate the random circuit
    cir = random_iqp_circuits(qubit_num, gate_num)
    original_width = cir.width

    # Apply random greedy heuristic algorithm to compile the circuit
    cir.reduce(method="random_greedy", shots=random_shots)
    compiled_width = cir.width

    # Calculate the reducibility factor
    reducibility_factor = 1 - compiled_width / original_width

    # Print the result
    print("original circuit width:", original_width, "\n" 
          "number of two-qubit gates:", gate_num, "\n" 
          "reducibility factor:", reducibility_factor, "\n")
