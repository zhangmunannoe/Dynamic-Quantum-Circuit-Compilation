"""
Numerical experiments of the GRCS circuits.
For more details, please refer to https://github.com/sboixo/GRCS
"""

import os
from math import pi
from quantum.circuit import Circuit

directory_path = "./data"

# Set the range for the number of cycles
min_cycle = 10
# max_cycle = 67
max_cycle = 15

# Set the range for the number of qubits
# circuit_size = ["4x4", "4x5", "5x5", "5x6", "6x6", "6x7", "7x7", "7x8", "8x8", "8x9",
#                 "9x9", "9x10", "10x10", "10x11", "11x11", "11x12", "12x12"]
circuit_size = ["4x5", "5x5", "5x6", "6x6"]

for qubit_num in circuit_size:
    folder_path = os.path.join(directory_path, qubit_num)
    for cycle_num in range(min_cycle, max_cycle + 1):
        inst_name = "inst_" + qubit_num + "_" + str(cycle_num) + "_0.txt"
        inst_path = os.path.join(folder_path, inst_name)

        input_cir = []
        with open(inst_path, "r") as file:
            for line in file:
                input_cir.append(list(line.strip("\n").split(" ")))

        # Create a quantum circuit
        cir = Circuit()

        # Construct the quantum circuit
        for gate in input_cir[1:]:
            if gate[1] == "h":
                cir.h(int(gate[2]))
            elif gate[1] == "cz":
                cir.cz([int(gate[2]), int(gate[3])])
            elif gate[1] == "t":
                cir.t(int(gate[2]))
            elif gate[1] == "x_1_2":
                cir.rx(int(gate[2]), pi / 2)
            elif gate[1] == "y_1_2":
                cir.ry(int(gate[2]), pi / 2)
            else:
                raise NotImplementedError

        # Measure all qubits
        cir.measure()
        original_width = cir.width

        # Apply random greedy heuristic algorithm to compile the circuit
        cir.reduce(method="random_greedy", shots=10)
        compiled_width = cir.width

        # Calculate the reducibility factor
        reducibility_factor = 1 - compiled_width / original_width

        # Print the result
        print(
            "circuit instance:", inst_name, "\n" 
            "original circuit width:", original_width, "\n" 
            "compiled circuit width:", compiled_width, "\n" 
            "reducibility factor:", reducibility_factor, "\n"
        )
