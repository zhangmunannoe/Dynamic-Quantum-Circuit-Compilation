"""
Reimplementation of DCKF algorithm from [Qubit-Reuse Compilation with Mid-Circuit Measurement and Reset, Phys. Rev. X 13, 041057 (2023)]

Since the source code is not public available, we provide our reimplementation for reproducibility and verification purposes.
"""


import numpy
from typing import List, Tuple
from quantum.circuit import Circuit


def reduce_by_dckf(circuit: Circuit, first_qubit_search=False) -> None:
    r"""Compile a static circuit into an equivalent dynamic circuit by the DCKF algorithm proposed in
    [Qubit-Reuse Compilation with Mid-Circuit Measurement and Reset, Phys. Rev. X 13, 041057 (2023)].

    Args:
        circuit (Circuit): a static circuit
        first_qubit_search (bool, optional): whether to employ brute-force search over the first measured qubit
    """
    def _manage_qubit_reuse(q_register: list, reg_occupation: list, which_qubit: int, edge_addition: list) -> Tuple[list, list]:
        r"""Update the occupation status in the given quantum register, assign an available unit to the
        input qubit and record the occupation order of qubits on each unit in order to manage the qubit reuse.

        Args:
            q_register (list): quantum register to update
            reg_occupation (list): list to record the occupation order of qubits on each register unit.
            which_qubit (int): the qubit to assign available unit
            edge_addition (list): edge addition strategy corresponds to the qubit reuse scheme

        Returns:
            tuple: a tuple containing the updated quantum register and the updated occupation order of qubits on
            all register units.

        Note:
            We use a list to implement quantum register where the value of an element represents a qubit and
            its index indicates the address of the register unit.
            A register unit whose value is None is an available unit.
            We use a list to record the occupation order of qubits on each register unit, where the index of
            an element is the address of the register unit and the value is a list that record the order in which
            this unit is occupied by different qubits.
        """
        if which_qubit not in q_register:
            # Identify all unoccupied registers from existing ones
            available_units = [i for i in range(len(q_register)) if q_register[i] is None]
            if available_units:  # there exist unoccupied register
                dynamic_qubit = available_units[0]  # load which_qubit to the first available register
                # Convert the qubit reuse as an added edge to the DAG of the circuit
                terminal = terminals[reg_occupation[dynamic_qubit][-1]]
                root = roots[which_qubit]
                edge_addition.append((terminal, root))
                # Record the last qubit that occupies this register
                reg_occupation[dynamic_qubit].append(which_qubit)
            else:  # in case where there is no available register, initialize a new register for which qubit
                dynamic_qubit = len(q_register)
                reg_occupation.append([which_qubit])
                q_register.append(which_qubit)
            q_register[dynamic_qubit] = which_qubit

        return q_register, reg_occupation

    def _construct_measurement_order_by_greedy(first_measured_qubit: int) -> List:
        r"""Construct the measurement order from the given first measured qubit by greedy heuristic.

        Args:
            first_measured_qubit: first measured qubit

        Returns:
            list: a list of added edges corresponds to the qubit-reuse scheme.
        """
        measurement_order = []  # initialize a measurement order list
        unmeasured_qubits = set(range(original_circuit_width))
        measured_causal_cone = set()  # causal cone of all measured qubits (Cq)
        qreg, qubit_occupation, edge_addition = [], [], []

        # To measure this qubit, all qubits in its causal cone should be activated
        activated_qubits = all_causal_cones[first_measured_qubit]
        # Manage the activated qubit through a quantum register
        for q in activated_qubits:
            qreg, qubit_occupation = _manage_qubit_reuse(qreg, qubit_occupation, q, edge_addition)

        # Recycle the register occupied by the measured qubit
        measured_address = [i for i in range(len(qreg)) if qreg[i] == first_measured_qubit][0]
        qreg[measured_address] = None

        # Update the measurement order
        measurement_order.append(first_measured_qubit)
        measured_causal_cone = measured_causal_cone.union(all_causal_cones[first_measured_qubit])
        unmeasured_qubits.remove(first_measured_qubit)

        # Apply greedy strategy to get the complete measurement order
        while len(measurement_order) != original_circuit_width:
            next_to_measure = None
            union_size = original_circuit_width
            # Identify the qubit whose causal cone Cq′ adds the fewest new input qubits to Cq as the next to measure
            for qubit in unmeasured_qubits:
                union = measured_causal_cone.union(all_causal_cones[qubit])
                if len(union) <= union_size:
                    next_to_measure = qubit
                    union_size = len(union)

            # Qubits in the causal cone of the next measured qubit but have not been measured should be activated
            activated_qubits = all_causal_cones[next_to_measure].difference(set(measurement_order))
            # Manage the activated qubit through a quantum register
            for q in activated_qubits:
                qreg, qubit_occupation = _manage_qubit_reuse(qreg, qubit_occupation, q, edge_addition)

            # Recycle the register occupied by the measured qubit
            measured_address = [i for i in range(len(qreg)) if qreg[i] == next_to_measure][0]
            qreg[measured_address] = None

            # Update the measurement order
            measurement_order.append(next_to_measure)
            measured_causal_cone = measured_causal_cone.union(all_causal_cones[next_to_measure])
            unmeasured_qubits.remove(next_to_measure)

        return edge_addition

    # Get the biadjacency matrix of the circuit
    biadjacency_matrix, _ = circuit.get_biadjacency_and_candidate_matrices(method="boolean_matrix")
    # Original static circuit width
    original_circuit_width = circuit.width
    # Calculate the causal cone for each measurement
    all_causal_cones = [set(numpy.where(biadjacency_matrix[:, q] == 1)[0]) for q in range(original_circuit_width)]
    # Get the graph representation of the circuit
    graph, roots, terminals = circuit.to_dag()
    new_graph = graph.copy()

    if first_qubit_search:
        # Employ brute-force search over the first measured qubit
        optimal_added_edges = []
        for first_to_measure in range(original_circuit_width):
            added_edges = _construct_measurement_order_by_greedy(first_to_measure)
            if len(added_edges) > len(optimal_added_edges):
                optimal_added_edges = added_edges

        # Compile the input static circuit into dynamic circuit with the modified graph and added edges
        new_graph.add_edges_from(optimal_added_edges)
        circuit._reorder_by_dag(new_graph, optimal_added_edges)
    else:
        # Identify the first measured qubit by greedy heuristic
        first_to_measure = int(numpy.argmin(numpy.sum(biadjacency_matrix, axis=0)))
        added_edges = _construct_measurement_order_by_greedy(first_to_measure)

        # Compile the input static circuit into dynamic circuit with the modified graph and added edges
        new_graph.add_edges_from(added_edges)
        circuit._reorder_by_dag(new_graph, added_edges)

    circuit.remap_indices()
