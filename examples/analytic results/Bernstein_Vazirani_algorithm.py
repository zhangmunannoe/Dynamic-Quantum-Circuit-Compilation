"""
Qubit-reuse-optimal compilation of Bernstein-Vazirani algorithm.
"""

import numpy
from functools import reduce
from quantum.circuit import Circuit

# Set the secret string encoded in the function
secret_string = "10110"
# The number of qubits
qubit_num = len(secret_string) + 1

# Create a quantum circuit
cir = Circuit("Bernstein-Vazirani algorithm")

# State initialization
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

# Apply another layer of Hadamard gates after the oracle
for i in range(qubit_num - 1):
    cir.h(i)

# Measure all qubits
cir.measure()
# Print the circuit
cir.print_circuit()


# Get the biadjacency matrix of the simplified graph of the quantum circuit through boolean matrix multiplication
b_circuit, _ = cir.get_biadjacency_and_candidate_matrices(method="boolean_matrix")

# Construct the matrix corresponding to the added edges in the optimal compilation
op_matrix = numpy.zeros([qubit_num, qubit_num], dtype=int)
for i in range(0, qubit_num - 2):
    op_matrix[i][i + 1] += 1

# Construct the adjacency matrix corresponding to the optimal compilation
zero_matrix = numpy.zeros([qubit_num, qubit_num], dtype=int)
adjacency_matrix = numpy.block([[zero_matrix, b_circuit], [op_matrix, zero_matrix]])

# Iteratively calculate the power of the adjacency matrix
nilpotent = reduce(numpy.matmul, [adjacency_matrix for _ in range(2 * qubit_num)])

# Check whether the adjacency matrix corresponding to the optimal compilation is nilpotent
print("\nThe adjacency matrix corresponding to the optimal compilation is nilpotent:", numpy.all(nilpotent == 0))
