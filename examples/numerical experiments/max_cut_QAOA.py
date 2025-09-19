"""
Numerical experiments of Max-Cut QAOA circuits on random unweighted 3-regular graphs.
"""

from math import pi
import networkx as nx
from quantum.circuit import Circuit

# Set the number of random graphs for each qubit number
seed_num = 5
# Set the random shots of the random greedy algorithm
random_shots = 5
# Set the range for the number of qubits
min_qubit_num = 10
max_qubit_num = 50
# Set the number of QAOA unitary layers
layer_num = 1

for q in range(min_qubit_num, max_qubit_num + 1, 4):
    for s in range(seed_num):
        # Generate the random U3R graph
        u3r_graph = nx.random_regular_graph(3, q, s)

        # Create a quantum circuit
        cir = Circuit()

        # Construct the Max-Cut QAOA circuit on the random graph
        # Prepare uniform superposition over all qubits
        for i in range(q):
            cir.h(i)
        # Alternatively apply the problem unitary and the mixing unitary multiple times
        for p in range(layer_num):
            # The problem unitary for Max-Cut cen be implemented using Z-Z rotation gates,
            # which are commutable with each other.
            # Here CZ gates are employed as substitutes for demonstration.
            for edge in u3r_graph.edges():
                cir.cz([edge[0], edge[1]])
            # The mixing unitary, all rotation angles are set to pi for demonstration.
            for node in u3r_graph.nodes:
                cir.rx(node, pi)

        # Measure all qubits
        cir.measure()
        original_width = cir.width

        # Add group tags for all commutable CZ gates
        for gate in cir.gate_history:
            if gate['name'] == 'cz':
                gate['group_tag'] = 'z_group'
            else:
                gate['group_tag'] = None

        # Apply random greedy heuristic algorithm to compile the QAOA circuit
        cir.reduce(method="random_greedy", shots=random_shots)

        # Print the result
        print("Original circuit width:", original_width, "\n"
              "Compiled circuit width:", cir.width, "\n")
