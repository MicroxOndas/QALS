"""
Modular and configurable visualization utilities for quantum algorithms.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from typing import List, Tuple, Optional
from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.visualization.bloch import Bloch

import platform

def get_emoji_font() -> str:
    """Detects the operating system and returns an appropriate emoji font."""
    # Detectar el sistema operativo
    if platform.system() == 'Darwin':
        emoji_font = 'Apple Color Emoji'
    elif platform.system() == 'Windows':
        emoji_font = 'Segoe UI Emoji'
    else:  # Linux
        emoji_font = 'Noto Color Emoji'
    return emoji_font


# ═══════════════════════════════════════════════════════════════════════════
# BLOCH UTILITIES
# ═══════════════════════════════════════════════════════════════════════════

def bloch_vector_from_state(statevector: Statevector, qubit: int) -> Tuple[List[float], float]:
    """Calculates the Bloch vector for a specific qubit.
    
    Returns:
        Tuple of (vector, purity) where purity indicates if the qubit is entangled.
    """
    rho = statevector.to_operator().data
    rho_red = partial_trace(
        rho,
        [i for i in range(statevector.num_qubits) if i != qubit]
    ).data

    x = 2 * np.real(rho_red[0, 1])
    y = 2 * np.imag(rho_red[1, 0])
    z = np.real(rho_red[0, 0] - rho_red[1, 1])
    
    # Calculate purity: Tr(ρ²)
    purity = np.real(np.trace(rho_red @ rho_red))
    
    return [x, y, z], purity


def bloch_vectors_all_qubits(statevector: Statevector) -> List[Tuple[List[float], float]]:
    """Calculates Bloch vectors and purity for all qubits."""
    return [
        bloch_vector_from_state(statevector, q)
        for q in range(statevector.num_qubits)
    ]


def plot_bloch_sphere(vec: List[float], ax, purity: float = 1.0) -> None:
    """Draws a vector on a Bloch sphere with purity indicator."""
    b = Bloch(axes=ax)
    
    # Configure sharper and more visible arrows
    b.vector_width = 4
    b.vector_mutation = 25
    
    # Sphere styling
    b.sphere_alpha = 0.15
    b.sphere_color = '#E8F4F8'
    
    # Calculate vector magnitude
    magnitude = np.linalg.norm(vec)
    
    if magnitude < 0.01:  # Nearly null vector (maximally entangled)
        # Show a point at the center
        b.point_color = ['#9B59B6']
        b.point_marker = ['o']
        b.point_size = [120]
        b.add_points([[0], [0], [0]])
    elif purity < 0.99:  # Mixed state (partially entangled)
        b.vector_color = ['#E74C3C']
        b.vector_width = 3
        b.vector_mutation = 20
        b.add_vectors(vec)
    else:  # Pure state
        b.vector_color = ['#3498DB']
        b.add_vectors(vec)
    
    b.render()


# ═══════════════════════════════════════════════════════════════════════════
# CIRCUIT UTILITIES
# ═══════════════════════════════════════════════════════════════════════════

def calculate_circuit_scale(circuit: QuantumCircuit) -> float:
    """Calculates appropriate scale for circuit visualization."""
    depth = max(circuit.depth(), 1)
    if depth <= 2:
        return 1.2
    elif depth <= 5:
        return 0.4
    else:
        return min(0.7, 3.0 / max(circuit.num_qubits, depth * 0.3))


# ═══════════════════════════════════════════════════════════════════════════
# VISUALIZER CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class VisualizerConfig:
    """Configuration for the visualizer."""
    show_bloch: bool = True
    show_probabilities: bool = True
    show_circuit: bool = True
    adaptive_size: bool = True
    max_width: float = 16
    max_height: float = 10
    base_width_per_qubit: float = 3
    base_height: float = 8
    
    def calculate_figure_size(self, n_qubits: int) -> Tuple[float, float]:
        """Calculates figure size based on number of qubits."""
        if not self.adaptive_size:
            return (self.max_width, self.max_height)
        
        if self.show_bloch:
            width = min(4 + self.base_width_per_qubit * n_qubits, self.max_width)
        else:
            width = min(12, self.max_width)
        
        height = min(self.base_height, self.max_height)
        return (width, height)


# ═══════════════════════════════════════════════════════════════════════════
# STEP SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════

class QuantumStepSimulator:
    """Simulator that records each step of a quantum algorithm."""
    
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits)
        self.statevector = Statevector.from_label("0" * num_qubits)
        self.steps: List[Tuple[str, QuantumCircuit, Statevector]] = []
        self.add_step("Initial state")
    
    def apply_step(self, step_circuit: QuantumCircuit, title: str) -> None:
        """Applies a step to the circuit and records the result."""
        self.statevector = self.statevector.evolve(step_circuit)
        self.circuit.compose(step_circuit, inplace=True)
        self.add_step(title)
    
    def add_step(self, title: str) -> None:
        """Records the current state as a step."""
        self.steps.append((title, self.circuit.copy(), self.statevector))
    
    def get_steps(self) -> List[Tuple[str, QuantumCircuit, Statevector]]:
        """Returns all recorded steps."""
        return self.steps


# ═══════════════════════════════════════════════════════════════════════════
# INTERACTIVE VISUALIZER
# ═══════════════════════════════════════════════════════════════════════════

class InteractiveStepVisualizer:
    """Interactive visualizer with step navigation."""
    
    def __init__(
        self,
        simulator: QuantumStepSimulator,
        config: Optional[VisualizerConfig] = None
    ):
        self.simulator = simulator
        self.config = config or VisualizerConfig()
        self.steps = simulator.get_steps()
        self.n_steps = len(self.steps)
        self.n_qubits = simulator.num_qubits
        self.current_step = 0
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        self._create_figure()
        self._create_widgets()
        self._update_display(0)
    
    def _create_figure(self):
        """Creates the main figure with all subplots."""
        fig_width, fig_height = self.config.calculate_figure_size(self.n_qubits)
        
        # Create figure with custom background
        self.fig = plt.figure(figsize=(fig_width, fig_height), facecolor='#F8F9FA')
        
        if self.config.show_bloch:
            gs = self.fig.add_gridspec(
                3, self.n_qubits + 1,
                height_ratios=[1.2, 1.2, 0.5],
                hspace=0.5, wspace=0.4,
                top=0.80, bottom=0.12, left=0.08, right=0.95
            )
            
            # Probabilities subplot
            if self.config.show_probabilities:
                self.ax_prob = self.fig.add_subplot(gs[0, 0])
                self.ax_prob.set_facecolor('#FFFFFF')
                for spine in self.ax_prob.spines.values():
                    spine.set_edgecolor('#BDC3C7')
                    spine.set_linewidth(1.5)
            else:
                self.ax_prob = None
            
            # Bloch spheres
            self.ax_bloch = []
            for i in range(self.n_qubits):
                ax = self.fig.add_subplot(gs[0, i + 1], projection='3d')
                ax.set_facecolor('#F8F9FA')
                self.ax_bloch.append(ax)
            
            # Circuit subplot
            if self.config.show_circuit:
                self.ax_circuit = self.fig.add_subplot(gs[1, :])
                self.ax_circuit.set_facecolor('#FFFFFF')
            else:
                self.ax_circuit = None
        else:
            gs = self.fig.add_gridspec(
                2, 1,
                height_ratios=[1, 1],
                hspace=0.5,
                top=0.85, bottom=0.12, left=0.08, right=0.95
            )
            
            if self.config.show_probabilities:
                self.ax_prob = self.fig.add_subplot(gs[0, 0])
                self.ax_prob.set_facecolor('#FFFFFF')
            else:
                self.ax_prob = None
                
            if self.config.show_circuit:
                self.ax_circuit = self.fig.add_subplot(gs[1, 0])
                self.ax_circuit.set_facecolor('#FFFFFF')
            else:
                self.ax_circuit = None
                
            self.ax_bloch = []
    
    def _create_widgets(self):
        """Creates control widgets."""
        # Slider
        ax_slider = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor='#ECF0F1')
        self.slider = Slider(
            ax_slider, 'Step',
            0, self.n_steps - 1,
            valinit=0,
            valstep=1,
            valfmt='%d',
            color='#3498DB'
        )
        self.slider.on_changed(self._update_display)
        
        # Buttons
        ax_prev = plt.axes([0.15, 0.01, 0.1, 0.03])
        ax_next = plt.axes([0.70, 0.01, 0.1, 0.03])
        
        self.btn_prev = Button(ax_prev, 'Previous', color='#ECF0F1', hovercolor='#BDC3C7')
        self.btn_next = Button(ax_next, 'Next', color='#ECF0F1', hovercolor='#BDC3C7')
        
        self.btn_prev.on_clicked(self._prev_step)
        self.btn_next.on_clicked(self._next_step)
    
    def _update_display(self, val):
        """Updates the visualization with the current step."""
        step_idx = int(self.slider.val)
        self.current_step = step_idx
        
        title, circuit, state = self.steps[step_idx]
        
        # Limpiar título y textos anteriores
        self.fig.suptitle('')
        for txt in list(self.fig.texts):
            txt.remove()
        
        # Crear barra header
        from matplotlib.patches import FancyBboxPatch
        
        # Configuración del header
        header_height = 0.06
        header_y = 0.92  # Ajustar posición Y
        
        # Fondo principal
        header_bg = FancyBboxPatch(
            (0, header_y), 1, header_height,
            boxstyle="square,pad=0",
            transform=self.fig.transFigure,
            facecolor='#2C3E50',
            edgecolor='none',
            zorder=1000,
            clip_on=False
        )
        self.fig.add_artist(header_bg)
        
        # Línea decorativa inferior
        border_line = FancyBboxPatch(
            (0, header_y), 1, 0.003,
            boxstyle="square,pad=0",
            transform=self.fig.transFigure,
            facecolor='#3498DB',
            edgecolor='none',
            zorder=1001,
            clip_on=False
        )
        self.fig.add_artist(border_line)
        
        # Texto izquierdo - Paso actual
        self.fig.text(
            0.02, header_y + header_height/2,
            f"Step {step_idx}/{self.n_steps - 1}",
            ha='left', va='center',
            fontsize=12, fontweight='bold',
            color='#3498DB',
            transform=self.fig.transFigure,
            zorder=1002
        )
        
        # Texto central - Título del paso
        self.fig.text(
            0.5, header_y + header_height/2,
            title,
            ha='center', va='center',
            fontsize=13, fontweight='bold',
            color='white',
            transform=self.fig.transFigure,
            zorder=1002
        )
        
        # Texto derecho - Número de qubits
        self.fig.text(
            0.98, header_y + header_height/2,
            f"{self.n_qubits} Qubits",
            ha='right', va='center',
            fontsize=11,
            color='#95A5A6',
            transform=self.fig.transFigure,
            zorder=1002
        )
        
        
        # Update probabilities
        if self.config.show_probabilities and self.ax_prob:
            self.ax_prob.clear()
            probs = state.probabilities_dict()
            
            # Create bar chart with custom colors
            bars = self.ax_prob.bar(
                range(len(probs)), 
                list(probs.values()),
                color='#3498DB',
                edgecolor='#2C3E50',
                linewidth=1.5,
                alpha=0.8
            )
            
            # Gradient effect on bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                bar.set_color(plt.cm.Blues(0.4 + 0.6 * height))
            
            self.ax_prob.set_xticks(range(len(probs)))
            self.ax_prob.set_xticklabels(list(probs.keys()), fontsize=9)
            self.ax_prob.set_title("Probabilities", fontsize=12, fontweight='bold', 
                                color='#2C3E50', pad=10)
            self.ax_prob.set_ylabel("Probability", fontsize=10, color='#34495E')
            self.ax_prob.set_ylim(0, max(probs.values()) * 1.15)
            self.ax_prob.grid(True, alpha=0.3, linestyle='--')
            
            # Style spines
            for spine in self.ax_prob.spines.values():
                spine.set_edgecolor('#BDC3C7')
                spine.set_linewidth(1.5)
        
        # Update Bloch spheres
        if self.config.show_bloch:
            bloch_data = bloch_vectors_all_qubits(state)
            
            # Check for entanglement
            max_entangled_count = sum(1 for _, purity in bloch_data if purity < 0.02)
            
            for i in range(len(self.ax_bloch)):
                ax = self.ax_bloch[i]
                vec, purity = bloch_data[-(i+1)]
                
                ax.clear()
                plot_bloch_sphere(vec, ax, purity)
                
                # Determine qubit state
                magnitude = np.linalg.norm(vec)
                if magnitude < 0.01:
                    status = " 🔗"
                    color = '#9B59B6'
                elif purity < 0.99:
                    status = " ⚡"
                    color = '#E74C3C'
                else:
                    status = ""
                    color = '#27AE60'
                
                ax.set_title(
                    f"Qubit {len(bloch_data) - 1 - i}{status}", 
                    fontsize=14, fontweight='bold', color=color, pad=12,
                    fontfamily=get_emoji_font(),
                    y=1.2
                )
            
            # Add entanglement indicator if applicable
            if max_entangled_count >= 2:
                self.fig.text(
                    0.5, 0.95, 
                    "🔗 Maximally Entangled Qubits", 
                    ha='center', fontsize=11, 
                    weight='bold', style='italic',
                    color='#8E44AD',
                    bbox=dict(boxstyle='round,pad=0.6', facecolor='#E8DAEF', 
                                edgecolor='#9B59B6', linewidth=2, alpha=0.9)
                )
        
        # Update circuit
        if self.config.show_circuit and self.ax_circuit:
            self.ax_circuit.clear()
            scale = calculate_circuit_scale(circuit)

            custom_style = {
                'backgroundcolor': "#F8F9FA00",
                'textcolor': "#000000"
            }

            circuit_drawer(
                circuit, output="mpl", ax=self.ax_circuit, 
                fold=-1, scale=scale, style=custom_style
            )
            self.ax_circuit.set_facecolor("#FFFFFF00")

            self.ax_circuit.set_title(
                "Accumulated Circuit", fontsize=12, 
                fontweight='bold', color='#2C3E50', pad=10
            )
            self.ax_circuit.axis('off')
        
        self.fig.canvas.draw_idle()
    
    def _prev_step(self, event):
        """Navigates to the previous step."""
        if self.current_step > 0:
            self.slider.set_val(self.current_step - 1)
    
    def _next_step(self, event):
        """Navigates to the next step."""
        if self.current_step < self.n_steps - 1:
            self.slider.set_val(self.current_step + 1)
    
    def show(self):
        """Shows the visualization maximized with toolbar."""
        manager = plt.get_current_fig_manager()
        
        try:
            # Backend Qt5Agg / TkAgg: maximize window
            manager.window.showMaximized()
        except AttributeError:
            try:
                manager.window.state('zoomed')  # For TkAgg on Windows
            except Exception:
                pass

        # Ensure toolbar is not visible
        try:
            self.fig.canvas.toolbar_visible = False
            self.fig.canvas.header_visible = False
        except Exception:
            pass

        plt.show()