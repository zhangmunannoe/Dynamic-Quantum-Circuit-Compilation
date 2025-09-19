"""
Numerical experiments of the random quantum circuits.
"""

# Since dynamic circuit compilation is independent of the type of two-qubit gates,
# all two-qubit gates are implemented as controlled-NOT gates.

import math
import random
from quantum.circuit import Circuit


def random_circuits(num_qubit, num_gate) -> "Circuit":
    r"""Generate a random quantum circuit with the specified number of qubits and two-qubit gates.

    Args:
        num_qubit(int): the number of qubits in the random circuit
        num_gate(int): the number of two-qubit gates in the random circuit

    Returns:
        Circuit: a random circuit
    """
    # Create a quantum circuit
    circuit = Circuit()
    # Occupy all qubits with single qubit gate
    for i in range(num_qubit):
        circuit.h(i)
    # Randomly generate the specified number of two-qubit gate
    for j in range(num_gate):
        qubit = random.sample(range(num_qubit), 2)
        circuit.cx(qubit)
    # Measure all qubits
    circuit.measure()

    return circuit


# Set the number of random circuits
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
    cir = random_circuits(qubit_num, gate_num)
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
