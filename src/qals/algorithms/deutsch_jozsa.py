"""
Deutsch-Jozsa algorithm.
"""

from qiskit import QuantumCircuit
from qals.utils.visualizer_utils import QuantumStepSimulator


def run_deutsch_jozsa(
    n: int,
    oracle_type: str = "balanced",
    record_steps: bool = True
) -> QuantumStepSimulator:
    """
    Executes the Deutsch-Jozsa algorithm.
    
    Args:
        n: Number of input qubits (total n+1 qubits with the auxiliary)
        oracle_type: "constant" or "balanced"
        record_steps: If True, records each step
        
    Returns:
        Simulator with recorded steps
    """
    simulator = QuantumStepSimulator(n + 1)
    
    # Prepare auxiliary qubit in |1⟩
    qc_prep = QuantumCircuit(n + 1)
    qc_prep.x(n)
    simulator.apply_step(qc_prep, "Prepare auxiliary qubit in |1⟩")
    
    # Hadamards on all qubits
    qc_h = QuantumCircuit(n + 1)
    for i in range(n + 1):
        qc_h.h(i)
    simulator.apply_step(qc_h, "Initial superposition")
    
    # Oracle
    qc_oracle = QuantumCircuit(n + 1)
    if oracle_type == "constant":
        pass  # Does nothing
    else:  # balanced
        for i in range(n):
            qc_oracle.cx(i, n)
    simulator.apply_step(qc_oracle, f"Oracle ({oracle_type})")
    
    # Final Hadamards on input qubits
    qc_h_final = QuantumCircuit(n + 1)
    for i in range(n):
        qc_h_final.h(i)
    simulator.apply_step(qc_h_final, "Final Hadamards")
    
    return simulator