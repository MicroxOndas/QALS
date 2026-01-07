"""
Creation of Bell states.
"""

from qiskit import QuantumCircuit
from qals.utils.visualizer_utils import QuantumStepSimulator


def create_bell_state(
    bell_type: int = 0,
    record_steps: bool = True
) -> QuantumStepSimulator:
    """
    Creates one of the four Bell states.
    
    Args:
        bell_type: 0 (Φ+), 1 (Φ-), 2 (Ψ+), 3 (Ψ-)
        record_steps: If True, records each step
        
    Returns:
        Simulator with recorded steps
    """

    if bell_type not in [0, 1, 2, 3]:
        raise ValueError("bell_type must be 0, 1, 2, or 3.")
    
    simulator = QuantumStepSimulator(2)
    
    # Hadamard on the first qubit
    qc_h = QuantumCircuit(2)
    qc_h.h(0)
    simulator.apply_step(qc_h, "Create superposition")
    
    # CNOT to entangle
    qc_cnot = QuantumCircuit(2)
    qc_cnot.cx(0, 1)
    simulator.apply_step(qc_cnot, "Entangle with CNOT")
    
    # Apply transformations according to Bell type
    if bell_type == 1:  # Φ-
        qc_z = QuantumCircuit(2)
        qc_z.z(0)
        simulator.apply_step(qc_z, "Apply Z to first qubit")
    elif bell_type == 2:  # Ψ+
        qc_x = QuantumCircuit(2)
        qc_x.x(1)
        simulator.apply_step(qc_x, "Apply X to second qubit")
    elif bell_type == 3:  # Ψ-
        qc_z = QuantumCircuit(2)
        qc_z.z(0)
        simulator.apply_step(qc_z, "Apply Z to first qubit")
        qc_x = QuantumCircuit(2)
        qc_x.x(1)
        simulator.apply_step(qc_x, "Apply X to second qubit")
    
    return simulator


def get_bell_name(bell_type: int) -> str:
    """Returns the name of the Bell state."""
    names = ["Φ+", "Φ-", "Ψ+", "Ψ-"]
    return names[bell_type]