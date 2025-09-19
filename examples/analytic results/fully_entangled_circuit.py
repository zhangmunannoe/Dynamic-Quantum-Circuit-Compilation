"""
Qubit-reuse-optimal compilation of fully entangled circuit.
"""

import numpy
from quantum.circuit import Circuit

import numpy
from quantum.circuit import Circuit

# Since dynamic circuit compilation is independent of the type of two-qubit gates,
# all two-qubit gates are implemented as controlled-NOT gates.

# Set the number of qubits and entanglement layers
qubit_num = 6
layer_num = 1

# Create a quantum circuit
cir = Circuit("Fully entangled circuit")

# Construct fully entangled circuit
for i in range(layer_num):
    # Single qubit rotation layer, rotation gates can be arbitrarily selected
    for j in range(qubit_num):
        cir.h(j)
    # Entanglement layer
    for j in range(qubit_num - 1):
        for k in range(j + 1, qubit_num):
            cir.cx([j, k])
# Measure all qubits
cir.measure()
# Print quantum circuit
cir.print_circuit()


# Get the biadjacency matrix of the simplified graph of the quantum circuit through boolean matrix multiplication
b_circuit, _ = cir.get_biadjacency_and_candidate_matrices(method="boolean_matrix")

# Verify if the biadjacency matrix of the fully entangled circuit is an all-one matrix
print("\nThe biadjacency matrix of the fully entangled circuit is an all-one matrix:", numpy.all(b_circuit == 1))
