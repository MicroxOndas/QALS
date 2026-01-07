"""
Quantum Fourier Transform (QFT).
"""

import numpy as np
from qiskit import QuantumCircuit
from qals.utils.visualizer_utils import QuantumStepSimulator


def run_qft(
    n: int,
    initial_state: str = None,
    record_steps: bool = True
) -> QuantumStepSimulator:
    """
    Executes the Quantum Fourier Transform.
    
    Args:
        n: Number of qubits
        initial_state: Initial state (e.g., "101"), None for |0...0⟩
        record_steps: If True, records each step
        
    Returns:
        Simulator with recorded steps
    """
    simulator = QuantumStepSimulator(n)
    
    # Prepare initial state if specified
    if initial_state:
        qc_init = QuantumCircuit(n)
        for i, bit in enumerate(initial_state[::-1]):
            if bit == "1":
                qc_init.x(i)
        simulator.apply_step(qc_init, f"Prepare state |{initial_state}⟩")
    
    # QFT
    for j in range(n):
        # Hadamard on qubit j
        qc_h = QuantumCircuit(n)
        qc_h.h(j)
        simulator.apply_step(qc_h, f"H on qubit {j}")
        
        # Controlled rotations
        for k in range(j + 1, n):
            qc_rot = QuantumCircuit(n)
            angle = 2 * np.pi / (2 ** (k - j + 1))
            qc_rot.cp(angle, k, j)
            simulator.apply_step(qc_rot, f"Controlled rotation ({k}→{j})")
    
    # Swap qubits
    for i in range(n // 2):
        qc_swap = QuantumCircuit(n)
        qc_swap.swap(i, n - i - 1)
        simulator.apply_step(qc_swap, f"Swap qubits {i} ↔ {n-i-1}")
    
    return simulator