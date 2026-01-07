"""
Interactive visualizer for the Quantum Playground.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.patches import FancyBboxPatch
from typing import Optional

from qiskit.visualization import plot_bloch_vector
from qiskit.visualization.bloch import Bloch

from qals.logic.quantum_playground import QuantumPlayground, PRESET_STATES


class QuantumPlaygroundVisualizer:
    """Interactive visualizer for quantum gate experimentation."""
    
    def __init__(self):
        self.playground = QuantumPlayground()
        self.active_gate_preview = None
        self.rotation_param = np.pi/2  # For parameterized gates (default to π/2)
        
        self._create_figure()
        self._create_widgets()
        self._update_display()


    def _show_gate_matrix(self, gate_name: str):
        """Displays the State Vector (left) and Gate Matrix (right)."""
        # Guardamos qué puerta estamos viendo para poder actualizarla al hacer click
        self.active_gate_preview = gate_name 
        
        self.ax_matrix.clear()
        self.ax_matrix.axis('off')

        # --- 1. VECTOR DE ESTADO ACTUAL ---
        alpha, beta = self.playground.get_state_amplitudes()
        
        def fmt_c(c):
            if abs(c.imag) < 0.001: return f"{c.real:.2f}"
            if abs(c.real) < 0.001: return f"{c.imag:.2f}j"
            return f"{c.real:.1f}{c.imag:+.1f}j"

        vector_data = [[fmt_c(alpha)], [fmt_c(beta)]]

        # --- 2. DATOS DE LA MATRIZ (RZ CORREGIDA) ---
        GATE_DATA = {
            'I':   ([['1', '0'], ['0', '1']], None),
            'X':   ([['0', '1'], ['1', '0']], None),
            'Y':   ([['0', '-i'], ['i', '0']], None),
            'Z':   ([['1', '0'], ['0', '-1']], None),
            'H':   ([['1', '1'], ['1', '-1']], r"$\frac{1}{\sqrt{2}}$"),
            'S':   ([['1', '0'], ['0', 'i']], None),
            'T':   ([['1', '0'], ['0', r'$e^{i\pi/4}$']], None),
            'Sdg': ([['1', '0'], ['0', '-i']], None),
            'Tdg': ([['1', '0'], ['0', r'$e^{-i\pi/4}$']], None),
            'RX':  ([[r'$\cos$', r'$-i\sin$'], 
                    [r'$-i\sin$', r'$\cos$']], None),
            'RY':  ([[r'$\cos$', r'$-\sin$'], 
                    [r'$\sin$',  r'$\cos$']], None),
            # --- CORRECCIÓN AQUÍ: RZ COMPLETA ---
            'RZ':  ([[r'$e^{-i\theta/2}$', '0'], 
                    ['0', r'$e^{i\theta/2}$']], None)
        }

        if gate_name not in GATE_DATA:
            return

        matrix_rows, prefix = GATE_DATA[gate_name]

        # Expansión condicional para RX/RY si quieres más detalle, 
        # o mantenerlo corto como arriba.
        if gate_name in ['RX', 'RY']:
             # Si prefieres la versión completa, descomenta esto:
             # matrix_rows = [[r'$\cos(\frac{\theta}{2})$', r'$-i\sin$'], ... etc
             pass

        # --- 3. DIBUJAR TABLA DEL VECTOR (IZQUIERDA) ---
        # Ajustamos bbox para dejar espacio al símbolo X
        table_vec = self.ax_matrix.table(
            cellText=vector_data, loc='center', cellLoc='center',
            bbox=[0.05, 0.3, 0.15, 0.4] 
        )
        table_vec.auto_set_font_size(False)
        table_vec.set_fontsize(12)
        
        for key, cell in table_vec.get_celld().items():
            cell.set_linewidth(0)
            cell.set_facecolor('none')

        # Corchetes Vector
        self.ax_matrix.text(0.04, 0.5, '[', fontsize=30, ha='right', va='center', transform=self.ax_matrix.transAxes)
        self.ax_matrix.text(0.21, 0.5, ']', fontsize=30, ha='left', va='center', transform=self.ax_matrix.transAxes)
        self.ax_matrix.text(0.125, 0.2, 'State', fontsize=9, ha='center', color='#7F8C8D', transform=self.ax_matrix.transAxes)

        # --- 4. SÍMBOLO DE MULTIPLICACIÓN ---
        # Dibujamos una 'X' matemática o un punto grande
        self.ax_matrix.text(0.33, 0.5, r'$\times$', fontsize=20, ha='center', va='center', transform=self.ax_matrix.transAxes, color='#34495E')

        # --- 5. DIBUJAR TABLA DE LA MATRIZ (DERECHA) ---
        table_mat = self.ax_matrix.table(
            cellText=matrix_rows, loc='center', cellLoc='center',
            bbox=[0.45, 0.3, 0.45, 0.4] 
        )
        table_mat.auto_set_font_size(False)
        table_mat.set_fontsize(13)

        for key, cell in table_mat.get_celld().items():
            cell.set_linewidth(0)
            cell.set_facecolor('none')

        # Corchetes Matriz
        mat_left = 0.44
        mat_right = 0.91
        self.ax_matrix.text(mat_left, 0.5, '[', fontsize=35, ha='right', va='center', transform=self.ax_matrix.transAxes)
        self.ax_matrix.text(mat_right, 0.5, ']', fontsize=35, ha='left', va='center', transform=self.ax_matrix.transAxes)

        if prefix:
            self.ax_matrix.text(mat_left - 0.02, 0.5, prefix, fontsize=12, ha='right', va='center', transform=self.ax_matrix.transAxes)
            
        self.ax_matrix.text(0.675, 0.2, f'Gate ({gate_name})', fontsize=9, ha='center', color='#7F8C8D', transform=self.ax_matrix.transAxes)

        self.fig.canvas.draw_idle()

    def _hide_gate_matrix(self):
        """Hides the matrix display."""
        self.ax_matrix.clear()
        self.ax_matrix.axis('off')
        self.fig.canvas.draw_idle()
    
    def _create_figure(self):
        """Creates the main figure with all components."""
        self.fig = plt.figure(figsize=(16, 9), facecolor='#F8F9FA')
        
        # Main title
        self.fig.suptitle(
            "⚛️ Quantum Playground - Interactive Gate Explorer",
            fontsize=16, fontweight='bold', color='#2C3E50', y=0.98
        )
        
        # Create grid layout
        gs = self.fig.add_gridspec(
            3, 3,
            width_ratios=[1.2, 1.5, 1.3],
            height_ratios=[1.5, 0.8, 0.5],
            hspace=0.3, wspace=0.3,
            top=0.93, bottom=0.08, left=0.05, right=0.98
        )
        
        # --- MODIFICADO: BLOCH SPHERE TRANSPARENTE ---
        self.ax_bloch = self.fig.add_subplot(gs[0, 0], projection='3d')
        self.ax_bloch.set_title("Qubit State", fontsize=12, fontweight='bold', 
                                color='#2C3E50', pad=15, x=0.1)
        # Hacemos el fondo del eje transparente
        self.ax_bloch.patch.set_alpha(0)
        # Hacemos los paneles (paredes 3D) transparentes
        self.ax_bloch.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        self.ax_bloch.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        self.ax_bloch.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        # ---------------------------------------------
        
        # Middle: Probabilities
        self.ax_probs = self.fig.add_subplot(gs[0, 1])
        self.ax_probs.set_facecolor('#FFFFFF')
        self.ax_probs.set_title("Measurement Probabilities", fontsize=12, 
                                fontweight='bold', color='#2C3E50', pad=10)
        
        # Right: State info
        self.ax_info = self.fig.add_subplot(gs[0, 2])
        self.ax_info.set_facecolor('#F8F9FA')
        self.ax_info.axis('off')
        
        # Bottom left: Parameter sliders
        self.ax_sliders = self.fig.add_subplot(gs[1, 0])
        self.ax_sliders.set_facecolor('#FFFFFF')
        self.ax_sliders.axis('off')
        
        # Bottom middle: Gate buttons
        self.ax_gates = self.fig.add_subplot(gs[1, 1])
        self.ax_gates.set_facecolor('#FFFFFF')
        self.ax_gates.axis('off')

        self.ax_matrix = self.fig.add_subplot(gs[1, 1])
        self.ax_matrix.set_position([0.34, 0.18, 0.40, 0.12]) 
        self.ax_matrix.set_facecolor('none') # Fondo transparente
        self.ax_matrix.axis('off')
        
        # Bottom right: History
        self.ax_history = self.fig.add_subplot(gs[0, 2])
        self.ax_history.set_facecolor('#FFFFFF')
        self.ax_history.axis('off')
        
        # Control buttons area
        self.ax_controls = self.fig.add_subplot(gs[2, :])
        self.ax_controls.set_facecolor('#F8F9FA')
        self.ax_controls.axis('off')
    
    def _create_widgets(self):
        """Creates all interactive widgets."""
        
        # === PARAMETER SLIDERS ===
        slider_bg = '#ECF0F1'
        slider_color = '#3498DB'
        
        # Theta slider (polar angle)
        ax_theta = plt.axes([0.08, 0.42, 0.15, 0.02], facecolor=slider_bg)
        self.slider_theta = Slider(
            ax_theta, 'θ (polar)',
            0, np.pi,
            valinit=0,
            valstep=0.01,
            color=slider_color
        )
        self.slider_theta.on_changed(self._on_param_change)
        
        # Phi slider (azimuthal angle)
        ax_phi = plt.axes([0.08, 0.38, 0.15, 0.02], facecolor=slider_bg)
        self.slider_phi = Slider(
            ax_phi, 'φ (azimuth)',
            0, 2*np.pi,
            valinit=0,
            valstep=0.01,
            color=slider_color
        )
        self.slider_phi.on_changed(self._on_param_change)
        
        # Rotation parameter slider (for RX, RY, RZ)
        ax_rot = plt.axes([0.08, 0.34, 0.15, 0.02], facecolor=slider_bg)
        self.slider_rotation = Slider(
            ax_rot, 'Rotation (rad)',
            0, 2*np.pi,
            valinit=np.pi/2,
            valstep=0.01,
            color='#E74C3C'
        )
        self.slider_rotation.on_changed(self._on_rotation_change)
        
        # === PRESET STATE BUTTONS ===
        preset_y_start = 0.30  # Justo debajo del último slider
        preset_spacing = 0.027
        preset_width = 0.15
        
        self.preset_buttons = {}
        # Guardamos la posición Y del último botón para colocar los controles debajo
        last_y = preset_y_start 
        
        for idx, (name, _) in enumerate(PRESET_STATES.items()):
            last_y = preset_y_start - idx * preset_spacing
            ax_preset = plt.axes([0.08, last_y, preset_width, 0.022])
            btn = Button(ax_preset, name, color='#1ABC9C', hovercolor='#16A085')
            btn.label.set_fontsize(10)
            btn.label.set_color('white')
            btn.label.set_weight('bold')
            btn.on_clicked(lambda event, n=name: self._set_preset(n))
            self.preset_buttons[name] = btn
        
        # === SYSTEM CONTROL BUTTONS ===
        # Calculamos posición debajo de los presets con un margen
        controls_y = last_y - 0.1
        btn_height = 0.025
        # Dividimos el ancho (0.15) en dos botones de 0.07 con hueco de 0.01
        
        # Reset button (Izquierda)
        ax_reset = plt.axes([0.08, controls_y, 0.07, btn_height])
        self.btn_reset = Button(ax_reset, 'Reset', color='#E74C3C', hovercolor='#C0392B')
        self.btn_reset.label.set_color('white')
        self.btn_reset.label.set_fontsize(10)
        self.btn_reset.label.set_weight('bold')
        self.btn_reset.on_clicked(lambda event: self._reset())
        
        # Undo button (Derecha)
        ax_undo = plt.axes([0.16, controls_y, 0.07, btn_height])
        self.btn_undo = Button(ax_undo, 'Previous', color='#F39C12', hovercolor='#E67E22')
        self.btn_undo.label.set_color('white')
        self.btn_undo.label.set_fontsize(9)
        self.btn_undo.label.set_weight('bold')
        self.btn_undo.on_clicked(lambda event: self._undo())
        
        # === GATE BUTTONS (Centro) ===
        gate_buttons_y_start = 0.42
        gate_button_height = 0.03
        gate_button_width = 0.08
        gate_spacing = 0.035
        
        self.gate_buttons = {}
        gates_layout = [
            ['H', 'X', 'Y', 'Z'],
            ['I','RX', 'RY', 'RZ'],
            ['S', 'T', 'Sdg', 'Tdg'],
        ]

        x_offset = 0.34
        
        for row_idx, row in enumerate(gates_layout):
            for col_idx, gate in enumerate(row):
                if gate == '':
                    continue
                    
                x = x_offset + col_idx * (gate_button_width + 0.01)
                y = gate_buttons_y_start - row_idx * gate_spacing
                
                ax_btn = plt.axes([x, y, gate_button_width, gate_button_height])
                
                # Color based on gate type
                if gate in ['RX', 'RY', 'RZ']:
                    color = '#E74C3C'  # Red for rotation gates
                elif gate in ['H']:
                    color = '#9B59B6'  # Purple for Hadamard
                elif gate in ['X', 'Y', 'Z']:
                    color = '#3498DB'  # Blue for Pauli gates
                elif gate in ['S', 'Sdg',]:
                    color = '#F39C12'  # Yellow for 90 degrees Fase gates
                elif gate in ['T', 'Tdg']:
                    color = "#33C867"  # Green for 45 degrees Fase gates
                else:
                    color = '#95A5A6'  # Gray for others
                
                btn = Button(ax_btn, gate, color=color, hovercolor='#2C3E50')
                btn.label.set_color('white')
                btn.label.set_weight('bold')
                btn.on_clicked(lambda event, g=gate: self._apply_gate(g))
                
                def connect_hover(ax, gate):
                    ax.figure.canvas.mpl_connect(
                        'axes_enter_event',
                        lambda event: self._show_gate_matrix(gate) if event.inaxes == ax else None
                    )
                    ax.figure.canvas.mpl_connect(
                        'axes_leave_event',
                        lambda event: self._hide_gate_matrix() if event.inaxes == ax else None
                    )
                connect_hover(ax_btn, gate)

                self.gate_buttons[gate] = btn
        
    
    def _update_display(self):
        """Updates all visual elements."""
        
        # === UPDATE BLOCH SPHERE ===
        self.ax_bloch.clear()
        
        # --- RE-APLICAR TRANSPARENCIA AL LIMPIAR ---
        self.ax_bloch.patch.set_alpha(0)
        self.ax_bloch.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        self.ax_bloch.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        self.ax_bloch.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        # -------------------------------------------

        bloch = Bloch(axes=self.ax_bloch)
        bloch.vector_color = ['#3498DB']
        bloch.vector_width = 5
        bloch.vector_mutation = 30
        bloch.sphere_alpha = 0.15
        bloch.sphere_color = '#E8F4F8'
        
        vec = self.playground.get_bloch_vector()
        bloch.add_vectors(vec)
        bloch.render()
        
        self.ax_bloch.set_title(
            "Qubit State", fontsize=12, fontweight='bold', 
            color='#2C3E50', pad=15, x=0.1
        )
        # === UPDATE PROBABILITIES BAR CHART ===
        self.ax_probs.clear()
        probs = self.playground.get_probabilities()
        
        bars = self.ax_probs.bar(
            ['|0⟩', '|1⟩'],
            [probs.get('0', 0), probs.get('1', 0)],
            color=['#3498DB', '#E74C3C'],
            edgecolor='#2C3E50',
            linewidth=2,
            alpha=0.8
        )
        
        for bar in bars:
            height = bar.get_height()
            self.ax_probs.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{height*100:.1f}%',
                ha='center', va='bottom',
                fontweight='bold', fontsize=11
            )
        
        self.ax_probs.set_ylim(0, 1.1)
        self.ax_probs.set_ylabel('Probability', fontsize=10, fontweight='bold')
        self.ax_probs.set_title(
            "Measurement Probabilities", fontsize=10, 
            fontweight='bold', color='#2C3E50', pad=10
        )
        self.ax_probs.grid(True, alpha=0.3, linestyle='--')
        self.ax_probs.set_facecolor('#FFFFFF')
        
        for spine in self.ax_probs.spines.values():
            spine.set_edgecolor('#BDC3C7')
            spine.set_linewidth(1.5)
        
        # Update State Info
        self.ax_info.clear()
        self.ax_info.axis('off')
        state_desc = self.playground.get_state_description()
        alpha, beta = self.playground.get_state_amplitudes()
        
        info_text = (
            f"State Vector:\n{state_desc}\n\n"
            f"Amplitudes:\nα = {alpha:.4f}\nβ = {beta:.4f}\n\n"
            f"Parameters:\nθ = {self.playground.qubit_state.theta:.4f} rad\n"
            f"φ = {self.playground.qubit_state.phi:.4f} rad\n\n"
            f"Bloch Vector:\n[{vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f}]"
        )
        
        self.ax_info.text(
            0.05, 0.95, info_text,
            transform=self.ax_info.transAxes,
            fontsize=9, verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#ECF0F1', 
                        edgecolor='#BDC3C7', linewidth=2)
        )
        
        # Update History
        self.ax_history.clear()
        self.ax_history.axis('off')
        history = self.playground.get_history_summary()
        
        if len(history) <= 4:
            history_text = "Operation History:              \n" + " → ".join(history)
        else:
            recent = history[-50:]
            history_text = "Operation History (last 50):    \n" + "\n".join(
                [f"{i+1}. {op}" for i, op in enumerate(recent)]
            )
        
        self.ax_history.text(
            0.05, 0.3, history_text,
            transform=self.ax_history.transAxes,
            fontsize=8, verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#E8F4F8', 
                        edgecolor='#3498DB', linewidth=2)
        )
        
        self.fig.canvas.draw_idle()
    
    def _on_param_change(self, val):
        """Handles parameter slider changes."""
        theta = self.slider_theta.val
        phi = self.slider_phi.val
        self.playground.set_qubit_state(theta, phi)
        self._update_display()
    
    def _on_rotation_change(self, val):
        """Handles rotation parameter slider changes."""
        self.rotation_param = val
    
    def _apply_gate(self, gate_name: str):
        """Applies a quantum gate."""
        print(f"Applying gate: {gate_name}")
        
        # Check if gate needs parameter
        if gate_name in ['RX', 'RY', 'RZ']:
            print(f"  with parameter: {self.rotation_param:.4f} rad")
            success = self.playground.apply_gate(gate_name, self.rotation_param)
        else:
            success = self.playground.apply_gate(gate_name)
        
        print(f"  Success: {success}")
        print(f"  History: {self.playground.get_history_summary()}")
        
        if success:
            # Update sliders to match new state WITHOUT triggering callbacks
            # This prevents the slider update from calling set_qubit_state() which resets history
            self.slider_theta.eventson = False  # Disable events temporarily
            self.slider_phi.eventson = False
            
            self.slider_theta.set_val(self.playground.qubit_state.theta)
            self.slider_phi.set_val(self.playground.qubit_state.phi)
            
            self.slider_theta.eventson = True  # Re-enable events
            self.slider_phi.eventson = True
            
            self._update_display()
            if self.active_gate_preview == gate_name:
                self._show_gate_matrix(gate_name)
        else:
            print(f"  ERROR: Gate {gate_name} failed to apply!")
    
    def _set_preset(self, preset_name: str):
        """Sets a preset quantum state."""
        theta, phi = PRESET_STATES[preset_name]
        self.playground.set_qubit_state(theta, phi)
        
        # Update sliders without triggering callbacks
        self.slider_theta.eventson = False
        self.slider_phi.eventson = False
        
        self.slider_theta.set_val(theta)
        self.slider_phi.set_val(phi)
        
        self.slider_theta.eventson = True
        self.slider_phi.eventson = True
        
        self._update_display()
    
    def _reset(self):
        """Resets the playground."""
        self.playground.reset()
        
        # Update sliders without triggering callbacks
        self.slider_theta.eventson = False
        self.slider_phi.eventson = False
        self.slider_rotation.eventson = False
        
        self.slider_theta.set_val(0)
        self.slider_phi.set_val(0)
        self.slider_rotation.set_val(np.pi/2)
        
        self.slider_theta.eventson = True
        self.slider_phi.eventson = True
        self.slider_rotation.eventson = True
        
        self._update_display()
    
    def _undo(self):
        """Undoes the last operation."""
        if self.playground.undo():
            # Update sliders without triggering callbacks
            self.slider_theta.eventson = False
            self.slider_phi.eventson = False
            
            self.slider_theta.set_val(self.playground.qubit_state.theta)
            self.slider_phi.set_val(self.playground.qubit_state.phi)
            
            self.slider_theta.eventson = True
            self.slider_phi.eventson = True
            
            self._update_display()
    
    def show(self):
        """Displays the playground."""
        manager = plt.get_current_fig_manager()
        
        try:
            manager.window.showMaximized()
        except AttributeError:
            try:
                manager.window.state('zoomed')
            except Exception:
                pass
        
        try:
            self.fig.canvas.toolbar_visible = True
            self.fig.canvas.header_visible = True
        except Exception:
            pass
        
        plt.show()


def launch_quantum_playground():
    """Launches the Quantum Playground application."""
    visualizer = QuantumPlaygroundVisualizer()
    visualizer.show()


if __name__ == "__main__":
    launch_quantum_playground()