"""
Quantum Playground - Interactive quantum gate experimentation.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class QubitState:
    """Represents the state of a single qubit."""
    theta: float = 0.0  # Polar angle (0 to π)
    phi: float = 0.0    # Azimuthal angle (0 to 2π)
    
    def to_statevector(self) -> Statevector:
        """Converts qubit parameters to a Qiskit statevector."""
        alpha = np.cos(self.theta / 2)
        beta = np.exp(1j * self.phi) * np.sin(self.theta / 2)
        return Statevector([alpha, beta])
    
    @classmethod
    def from_statevector(cls, sv: Statevector) -> 'QubitState':
        alpha, beta = sv.data

        # --- Normalización defensiva ---
        norm = np.sqrt(np.abs(alpha)**2 + np.abs(beta)**2)
        if norm == 0 or not np.isfinite(norm):
            return cls(theta=0.0, phi=0.0)

        alpha /= norm
        beta /= norm

        # --- Protección numérica para arccos ---
        a = np.clip(np.abs(alpha), 0.0, 1.0)
        theta = 2 * np.arccos(a)

        # Fase relativa
        phi = np.angle(beta) - np.angle(alpha)

        return cls(theta=float(theta), phi=float(phi))



class QuantumPlayground:
    """Manages the quantum playground state and operations."""
    
    # Available single-qubit gates
    AVAILABLE_GATES = {
        'I': 'Identity',
        'X': 'Pauli-X (NOT)',
        'Y': 'Pauli-Y',
        'Z': 'Pauli-Z',
        'H': 'Hadamard',
        'S': 'S Gate (Phase)',
        'T': 'T Gate',
        'Sdg': 'S† (S-dagger)',
        'Tdg': 'T† (T-dagger)',
        'RX': 'Rotation-X (θ)',
        'RY': 'Rotation-Y (θ)',
        'RZ': 'Rotation-Z (θ)',
    }
    
    def __init__(self):
        self.qubit_state = QubitState()
        self.current_statevector = self.qubit_state.to_statevector()
        self.history: List[Tuple[str, Statevector]] = [("Initial", self.current_statevector)]
        self.circuit = QuantumCircuit(1)
    
    def reset(self):
        """Resets the playground to initial state."""
        self.qubit_state = QubitState()
        self.current_statevector = self.qubit_state.to_statevector()
        self.history = [("Initial", self.current_statevector)]
        self.circuit = QuantumCircuit(1)
    
    def set_qubit_state(self, theta: float, phi: float):
        """Sets the qubit to a specific state."""
        self.qubit_state = QubitState(theta=theta, phi=phi)
        self.current_statevector = self.qubit_state.to_statevector()
        self.circuit = QuantumCircuit(1)
        self.history = [("Custom State", self.current_statevector)]
    
    def apply_gate(self, gate_name: str, parameter: Optional[float] = None) -> bool:
        """
        Applies a quantum gate to the current state.
        
        Args:
            gate_name: Name of the gate to apply
            parameter: Parameter for parameterized gates (in radians)
            
        Returns:
            True if gate was applied successfully, False otherwise
        """
        qc = QuantumCircuit(1)
        
        try:
            if gate_name == 'I':
                qc.id(0)
            elif gate_name == 'X':
                qc.x(0)
            elif gate_name == 'Y':
                qc.y(0)
            elif gate_name == 'Z':
                qc.z(0)
            elif gate_name == 'H':
                qc.h(0)
            elif gate_name == 'S':
                qc.s(0)
            elif gate_name == 'T':
                qc.t(0)
            elif gate_name == 'Sdg':
                qc.sdg(0)
            elif gate_name == 'Tdg':
                qc.tdg(0)
            elif gate_name in ('RX', 'RY', 'RZ'):
                if parameter is None or not np.isfinite(parameter):
                    return False
                if gate_name == 'RX':
                    qc.rx(parameter, 0)
                elif gate_name == 'RY':
                    qc.ry(parameter, 0)
                else:
                    qc.rz(parameter, 0)
            else:
                return False
            
            # Apply gate and update state
            self.current_statevector = self.current_statevector.evolve(qc)
            self.circuit.compose(qc, inplace=True)
            self.qubit_state = QubitState.from_statevector(self.current_statevector)
            
            # Add to history
            gate_label = gate_name
            if parameter is not None:
                gate_label += f"({parameter:.2f})"
            self.history.append((gate_label, self.current_statevector))
            
            return True
            
        except Exception as e:
            print(f"Error applying gate {gate_name}: {e}")
            return False
    
    def get_bloch_vector(self) -> List[float]:
        """Returns the Bloch vector representation of the current state."""
        rho = self.current_statevector.to_operator().data
        x = 2 * np.real(rho[0, 1])
        y = 2 * np.imag(rho[1, 0])
        z = np.real(rho[0, 0] - rho[1, 1])
        return [x, y, z]
    
    def get_probabilities(self) -> Dict[str, float]:
        """Returns measurement probabilities."""
        return self.current_statevector.probabilities_dict()
    
    def get_state_amplitudes(self) -> Tuple[complex, complex]:
        """Returns the complex amplitudes of |0⟩ and |1⟩."""
        return tuple(self.current_statevector.data)
    
    def undo(self) -> bool:
        """Undoes the last gate operation."""
        if len(self.history) <= 1:
            return False
        
        self.history.pop()
        last_gate, last_state = self.history[-1]
        self.current_statevector = last_state
        self.qubit_state = QubitState.from_statevector(last_state)
        
        # Rebuild circuit from history (excluding initial state)
        self.circuit = QuantumCircuit(1)
        # Note: We don't rebuild the full circuit history for simplicity
        # The circuit display will show cumulative operations
        
        return True
    
    def get_history_summary(self) -> List[str]:
        """Returns a list of all operations performed."""
        return [label for label, _ in self.history]
    
    def get_state_description(self) -> str:
        """Returns a human-readable description of the current state."""
        alpha, beta = self.get_state_amplitudes()
        
        # Format complex numbers nicely
        def format_complex(c: complex) -> str:
            real = np.real(c)
            imag = np.imag(c)
            
            if abs(imag) < 1e-10:
                return f"{real:.3f}"
            elif abs(real) < 1e-10:
                return f"{imag:.3f}i"
            else:
                sign = "+" if imag >= 0 else "-"
                return f"{real:.3f} {sign} {abs(imag):.3f}i"
        
        return f"|ψ⟩ = ({format_complex(alpha)})|0⟩ + ({format_complex(beta)})|1⟩"


# Preset states for quick selection
PRESET_STATES = {
    "|0⟩ (Ground)": (0.0, 0.0),
    "|1⟩ (Excited)": (np.pi, 0.0),
    "|+⟩ (Plus)": (np.pi/2, 0.0),
    "|-⟩ (Minus)": (np.pi/2, np.pi),
    "|i⟩ (Plus-Y)": (np.pi/2, np.pi/2),
    "|-i⟩ (Minus-Y)": (np.pi/2, -np.pi/2),
}