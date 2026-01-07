"""
Quantum Teleportation.
"""

from qiskit import QuantumCircuit
from qals.utils.visualizer_utils import QuantumStepSimulator


def run_quantum_teleportation(
    initial_state: str = "plus",
    record_steps: bool = True
) -> QuantumStepSimulator:
    """
    Simulates the quantum teleportation protocol.
    
    Args:
        initial_state: "plus", "minus", "zero", "one"
        record_steps: If True, records each step
        
    Returns:
        Simulator with recorded steps
    """

    if initial_state not in ["plus", "minus", "zero", "one"]:
            raise ValueError("initial_state must be 'plus', 'minus', 'zero', or 'one'.")

    # 3 qubits: [0] state to teleport, [1] Alice, [2] Bob
    simulator = QuantumStepSimulator(3)
    
    # Prepare state to teleport
    qc_prep = QuantumCircuit(3)
    if initial_state == "plus":
        qc_prep.h(0)
    elif initial_state == "minus":
        qc_prep.x(0)
        qc_prep.h(0)
    elif initial_state == "one":
        qc_prep.x(0)
    simulator.apply_step(qc_prep, f"Prepare state |{initial_state}⟩")
    
    # Create entangled pair between Alice and Bob
    qc_bell = QuantumCircuit(3)
    qc_bell.h(1)
    qc_bell.cx(1, 2)
    simulator.apply_step(qc_bell, "Create EPR pair between Alice and Bob")
    
    # Alice: entangle with her part of the EPR pair
    qc_alice = QuantumCircuit(3)
    qc_alice.cx(0, 1)
    qc_alice.h(0)
    simulator.apply_step(qc_alice, "Alice entangles and measures")
    
    # Bob applies corrections
    qc_bob = QuantumCircuit(3)
    qc_bob.cx(1, 2)
    qc_bob.cz(0, 2)
    simulator.apply_step(qc_bob, "Bob applies corrections")
    
    return simulator