# Dynamic Quantum Circuit Compilation

This repository provides Python code accompanying the article **Dynamic Quantum Circuit Compilation** ([arXiv:2310.11021](https://arxiv.org/abs/2310.11021)).

## Requirements

To ensure compatibility, we suggest the following setup:

| Package     | Version |
|-------------|---------|
| Python      | 3.8     |
| numpy       | 1.24.4  |
| pandas      | 2.0.3   |
| networkx    | 3.1     |
| matplotlib  | 3.7.5   |

## Description

Dynamic quantum circuit compilation transforms static quantum circuits into equivalent dynamic circuits with fewer qubits through **qubit reuse** after measurement.

This project includes:
- The heuristic methods described in the manuscript
- Analytical and numerical examples to support reproducibility and verification  

## Key Methods

#### 1. `quantum.circuit.is_reducible`
Check whether a static quantum circuit can be reduced via qubit reuse.

**Method options:**  
- `"graph"` — Path searching on the graph representation (Algorithm 1 in [arXiv:2310.11021v2])  
- `"reachability"` — Reachability analysis between qubits (Algorithm 2 in [arXiv:2310.11021v2])  
- `"matrix"` — Boolean matrix multiplication (Algorithm 3 in [arXiv:2310.11021v2])

#### 2. `quantum.circuit.reduce`
Compile a static quantum circuit into an equivalent dynamic circuit with fewer qubits using the specified method.

**Method options:**  
- `"minimum_remaining_values"`: minimum remaining values heuristic (Section 7.1 in [arXiv:2310.11021v2])
- `"greedy"`: greedy heuristic (Section 7.2 in [arXiv:2310.11021v2])
- `"hybrid"`: hybrid method (Section 7.3 in [arXiv:2310.11021v2])

👉 For more details, please refer to the manuscript and the in-code docstrings.

## Analytical Results

Verification of qubit-reuse-optimal compilation strategies  are provided in `examples/analytical_results/`, inclduing:
1. Bernstein-Vazirani algorithm
2. Quantum ripple carry adder
3. Linearly entangled circuit
4. Circularly entangled circuit
5. Pairwise entangled circuit
6. Fully entangled circuit
7. Diamond structured circuit
8. MBQC cluster-state circuit

## Numerical Evaluations

The numerical evaluations for heuristic algorithms are provided in `examples/numerical_evaluations/`, including
1. GRCS circuits
2. Quantum supremacy circuits on Sycamore and Zuchongzhi processor
3. Quantum ripple carry adders
4. QAOA Max-cut circuits
5. Regular random circuits and randon IQP circuits
6. Noisy simulations

## Feedback

For feedback or questions, please contact Munan Zhang at zhangmunannoe@gmail.com 🙂.
