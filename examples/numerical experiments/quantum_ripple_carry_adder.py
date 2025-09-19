"""
Numerical experiments comparing our greedy heuristic with the DCKF algorithm from
[Qubit-Reuse Compilation with Mid-Circuit Measurement and Reset, Phys. Rev. X 13, 041057 (2023)] on quantum ripple carry adders.
"""

import copy

from DCKF_reimplementation import reduce_by_dckf
from quantum.circuit import Circuit

for bit_num in range(2, 20):
    # A k-bit quantum adder needs 3*k+1 qubits
    qubit_num = 3 * bit_num + 1

    # Create a quantum circuit
    cir = Circuit("Quantum ripple carry adder")

    # Construct the n-bit quantum ripple carry adder
    for i in range(bit_num):
        cir.ccx([3 * i + 1, 3 * i + 2, 3 * i + 3])
        cir.cx([3 * i + 1, 3 * i + 2])
    for i in range(bit_num):
        cir.ccx([3 * i, 3 * i + 2, 3 * i + 3])
    for i in range(bit_num):
        cir.cx([3 * i, 3 * i + 2])

    # Measure all qubits
    cir.measure()
    cir1 = copy.deepcopy(cir)
    cir2 = copy.deepcopy(cir)

    # Compile the circuit using different algorithms
    cir.reduce("deterministic_greedy")
    reduce_by_dckf(cir1)
    reduce_by_dckf(cir2, first_qubit_search=True)

    # Print the compiled circuit width
    print("Original circuit width:", qubit_num, "\n"
          "Our greedy:", cir.width, "\n"
          "DCKF:", cir1.width, "\n"
          "DCKF + first qubit search:", cir2.width, "\n")
