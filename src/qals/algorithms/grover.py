"""
Grover's algorithm.
"""

import numpy as np
from typing import List, Tuple

from qiskit import QuantumCircuit
from qals.utils.visualizer_utils import QuantumStepSimulator


def calculate_optimal_grover_iterations(n: int) -> int:
    """Calculates the optimal number of iterations for Grover's algorithm."""
    N = 2 ** n
    return int(np.floor(np.pi / 4 * np.sqrt(N)))


def create_grover_oracle(n: int, target: str) -> List[Tuple[str, QuantumCircuit]]:
    """
    Creates the steps of the Grover oracle for a target state.
    
    Args:
        n: Number of qubits
        target: Binary string of the target state (e.g., "101")
        
    Returns:
        List of tuples (description, circuit) for each oracle step
    """
    steps = []
    
    # Previous X gates (for bits that are 0 in the target)
    qc_x_prev = QuantumCircuit(n)
    for t, bit in enumerate(target):
        if bit == "0":
            qc_x_prev.x(t)
    if qc_x_prev.size() > 0:
        steps.append(("Oracle: Previous X gates", qc_x_prev))
    
    # Multi-controlled Z
    qc_mcz = QuantumCircuit(n)
    if n == 1:
        qc_mcz.z(0)
    elif n == 2:
        qc_mcz.cz(0, 1)
    else:
        qc_mcz.h(n - 1)
        qc_mcz.mcx(list(range(n - 1)), n - 1)
        qc_mcz.h(n - 1)
    steps.append(("Oracle: MCZ", qc_mcz))
    
    # Posterior X gates (undo)
    qc_x_post = QuantumCircuit(n)
    for t, bit in enumerate(target):
        if bit == "0":
            qc_x_post.x(t)
    if qc_x_post.size() > 0:
        steps.append(("Oracle: Posterior X gates", qc_x_post))
    
    return steps


def create_grover_diffuser(n: int) -> List[Tuple[str, QuantumCircuit]]:
    """
    Creates the steps of the Grover diffusion operator.
    
    Args:
        n: Number of qubits
        
    Returns:
        List of tuples (description, circuit) for each diffuser step
    """
    steps = []
    
    # Previous Hadamards
    qc_h_prev = QuantumCircuit(n)
    for q in range(n):
        qc_h_prev.h(q)
    steps.append(("Diffuser: Previous H gates", qc_h_prev))
    
    # Previous X gates
    qc_x_prev = QuantumCircuit(n)
    for q in range(n):
        qc_x_prev.x(q)
    steps.append(("Diffuser: Previous X gates", qc_x_prev))
    
    # Multi-controlled Z
    qc_mcz = QuantumCircuit(n)
    if n == 1:
        qc_mcz.z(0)
    elif n == 2:
        qc_mcz.cz(0, 1)
    else:
        qc_mcz.h(n - 1)
        qc_mcz.mcx(list(range(n - 1)), n - 1)
        qc_mcz.h(n - 1)
    steps.append(("Diffuser: MCZ", qc_mcz))
    
    # Posterior X gates
    qc_x_post = QuantumCircuit(n)
    for q in range(n):
        qc_x_post.x(q)
    steps.append(("Diffuser: Posterior X gates", qc_x_post))
    
    # Posterior Hadamards
    qc_h_post = QuantumCircuit(n)
    for q in range(n):
        qc_h_post.h(q)
    steps.append(("Diffuser: Posterior H gates", qc_h_post))
    
    return steps


def run_grover_algorithm(
    n: int,
    target: str,
    record_steps: bool = True
) -> QuantumStepSimulator:
    """
    Executes Grover's algorithm recording each step.
    
    Args:
        n: Number of qubits
        target: Target state to search for (binary string, e.g., "101")
        record_steps: If True, records each substep; if False, only complete iterations
        
    Returns:
        Simulator with all recorded steps
    """

    if len(target) != n or any(bit not in "01" for bit in target):
        raise ValueError("The target state must be a binary string of length n.")
    
    target = target[::-1]  # Reverse for Qiskit convention
    
    simulator = QuantumStepSimulator(n)
    num_iterations = calculate_optimal_grover_iterations(n)
    
    # Initial Hadamards
    qc_init = QuantumCircuit(n)
    for q in range(n):
        qc_init.h(q)
    simulator.apply_step(qc_init, "Initial Hadamards")
    
    # Grover iterations
    for it in range(num_iterations):
        
        # Oracle
        oracle_steps = create_grover_oracle(n, target)
        for desc, qc in oracle_steps:
            title = f"[Iter {it}] {desc}"
            if record_steps:
                simulator.apply_step(qc, title)
            else:
                simulator.circuit.compose(qc, inplace=True)
                simulator.statevector = simulator.statevector.evolve(qc)
        
        # Diffuser
        diffuser_steps = create_grover_diffuser(n)
        for desc, qc in diffuser_steps:
            title = f"[Iter {it}] {desc}"
            if record_steps:
                simulator.apply_step(qc, title)
            else:
                simulator.circuit.compose(qc, inplace=True)
                simulator.statevector = simulator.statevector.evolve(qc)
        
        if not record_steps:
            simulator.add_step(f"After iteration {it}")
    
    return simulator