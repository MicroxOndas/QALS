import tkinter as tk
from tkinter import ttk, messagebox

from qals.utils.visualizer_utils import InteractiveStepVisualizer, VisualizerConfig
from qals.algorithms.grover import run_grover_algorithm
from qals.algorithms.deutsch_jozsa import run_deutsch_jozsa
from qals.algorithms.bell_states import (
    create_bell_state, get_bell_name
)
from qals.algorithms.qft import run_qft
from qals.algorithms.teleportation import run_quantum_teleportation

from qals.utils.playground_visualizer import launch_quantum_playground


# ───────────── Launch Functions ─────────────

def launch_grover(n, target, show_bloch):
    try:
        simulator = run_grover_algorithm(n, target, record_steps=True)
        config = VisualizerConfig(show_bloch=show_bloch)
        visualizer = InteractiveStepVisualizer(simulator, config)
        visualizer.show()
    except ValueError as e:
        messagebox.showerror("Validation Error", f"Invalid parameters:\n{str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error running Grover's algorithm:\n{str(e)}")

def launch_deutsch(n, oracle_type, show_bloch):
    try:
        simulator = run_deutsch_jozsa(n, oracle_type)
        config = VisualizerConfig(show_bloch=show_bloch)
        visualizer = InteractiveStepVisualizer(simulator, config)
        visualizer.show()
    except ValueError as e:
        messagebox.showerror("Validation Error", f"Invalid parameters:\n{str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error running Deutsch-Jozsa:\n{str(e)}")

def launch_bell(bell_type, show_bloch):
    try:
        simulator = create_bell_state(bell_type)
        config = VisualizerConfig(show_bloch=show_bloch)
        visualizer = InteractiveStepVisualizer(simulator, config)
        visualizer.show()
    except ValueError as e:
        messagebox.showerror("Validation Error", f"Invalid parameters:\n{str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating Bell state:\n{str(e)}")


def launch_qft(n, initial_state, show_bloch):
    try:
        simulator = run_qft(n, initial_state)
        config = VisualizerConfig(show_bloch=show_bloch)
        visualizer = InteractiveStepVisualizer(simulator, config)
        visualizer.show()
    except ValueError as e:
        messagebox.showerror("Validation Error", f"Invalid parameters:\n{str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error running QFT:\n{str(e)}")

def launch_teleport(initial_state, show_bloch):
    try:
        simulator = run_quantum_teleportation(initial_state)
        config = VisualizerConfig(show_bloch=show_bloch)
        visualizer = InteractiveStepVisualizer(simulator, config)
        visualizer.show()
    except ValueError as e:
        messagebox.showerror("Validation Error", f"Invalid parameters:\n{str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error running quantum teleportation:\n{str(e)}")

def launch_playground():
    """Launches the Quantum Playground."""
    try:
        launch_quantum_playground()
    except Exception as e:
        messagebox.showerror("Error", f"Error launching Quantum Playground:\n{str(e)}")


# ───────────── Configuration Windows ─────────────

def create_config_window(root, title, width=350, height=250):
    """Creates a configuration window with consistent styling."""
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry(f"{width}x{height}")
    win.configure(bg="#f0f0f0")
    win.resizable(False, False)
    
    # Center window
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")
    
    return win

def styled_label(parent, text, font=("Arial", 10), **kwargs):
    return tk.Label(
        parent,
        text=text,
        bg="#f0f0f0",
        font=font,
        **kwargs
    )

def styled_button(parent, text, command, color="#4A90E2"):
    """Creates a styled button."""
    return tk.Button(
        parent, text=text, command=command,
        bg=color, fg="white", font=("Arial", 10, "bold"),
        relief=tk.FLAT, padx=20, pady=8,
        cursor="hand2", activebackground="#357ABD"
    )

def config_grover(root):
    win = create_config_window(root, "Configure Grover's Algorithm")
    
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(expand=True, pady=20)
    
    styled_label(frame, "Number of qubits:").pack(pady=5)
    n_entry = tk.Entry(frame, font=("Arial", 10), width=25, justify="center")
    n_entry.insert(0, "3")
    n_entry.pack(pady=5)
    
    styled_label(frame, "Target state (binary):").pack(pady=5)
    target_entry = tk.Entry(frame, font=("Arial", 10), width=25, justify="center")
    target_entry.insert(0, "101")
    target_entry.pack(pady=5)
    
    show_bloch_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        frame, text="Show Bloch Spheres", variable=show_bloch_var,
        bg="#f0f0f0", font=("Arial", 9), activebackground="#f0f0f0"
    ).pack(pady=10)
    
    styled_button(
        frame, "Run",
        lambda: launch_grover(int(n_entry.get()), target_entry.get(), show_bloch_var.get()),
        color="#27AE60"
    ).pack(pady=5)

def config_deutsch(root):
    win = create_config_window(root, "Configure Deutsch-Jozsa Algorithm")
    
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(expand=True, pady=20)
    
    styled_label(frame, "Number of qubits:").pack(pady=5)
    n_entry = tk.Entry(frame, font=("Arial", 10), width=25, justify="center")
    n_entry.insert(0, "2")
    n_entry.pack(pady=5)
    
    styled_label(frame, "Oracle type:").pack(pady=5)
    oracle_combo = ttk.Combobox(frame, values=["constant", "balanced"], 
                                font=("Arial", 10), width=23, state="readonly")
    oracle_combo.current(1)
    oracle_combo.pack(pady=5)
    
    show_bloch_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        frame, text="Show Bloch Spheres", variable=show_bloch_var,
        bg="#f0f0f0", font=("Arial", 9), activebackground="#f0f0f0"
    ).pack(pady=10)
    
    styled_button(
        frame, "Run",
        lambda: launch_deutsch(int(n_entry.get()), oracle_combo.get(), show_bloch_var.get()),
        color="#27AE60"
    ).pack(pady=5)

def config_bell(root):
    win = create_config_window(root, "Configure Bell State", height=230)
    
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(expand=True, pady=20)
    
    styled_label(frame, "Select Bell state:").pack(pady=5)
    names = [f"{i}: {get_bell_name(i)}" for i in range(4)]
    bell_combo = ttk.Combobox(frame, values=names, font=("Arial", 10), 
                                width=23, state="readonly")
    bell_combo.current(0)
    bell_combo.pack(pady=5)
    
    show_bloch_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        frame, text="Show Bloch Spheres", variable=show_bloch_var,
        bg="#f0f0f0", font=("Arial", 9), activebackground="#f0f0f0"
    ).pack(pady=10)
    
    styled_button(
        frame, "Run",
        lambda: launch_bell(int(bell_combo.get().split(":")[0]), show_bloch_var.get()),
        color="#27AE60"
    ).pack(pady=5)

def config_qft(root):
    win = create_config_window(root, "Configure QFT (Quantum Fourier Transform)")
    
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(expand=True, pady=20)
    
    styled_label(frame, "Number of qubits:").pack(pady=5)
    n_entry = tk.Entry(frame, font=("Arial", 10), width=25, justify="center")
    n_entry.insert(0, "3")
    n_entry.pack(pady=5)
    
    styled_label(frame, "Initial state (binary):").pack(pady=5)
    state_entry = tk.Entry(frame, font=("Arial", 10), width=25, justify="center")
    state_entry.insert(0, "101")
    state_entry.pack(pady=5)
    
    show_bloch_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        frame, text="Show Bloch Spheres", variable=show_bloch_var,
        bg="#f0f0f0", font=("Arial", 9), activebackground="#f0f0f0"
    ).pack(pady=10)
    
    styled_button(
        frame, "Run",
        lambda: launch_qft(int(n_entry.get()), state_entry.get(), show_bloch_var.get()),
        color="#27AE60"
    ).pack(pady=5)

def config_teleport(root):
    win = create_config_window(root, "Configure Quantum Teleportation", height=230)
    
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(expand=True, pady=20)
    
    styled_label(frame, "Initial state to teleport:").pack(pady=5)
    state_combo = ttk.Combobox(frame, values=["plus", "minus", "zero", "one"], 
                               font=("Arial", 10), width=23, state="readonly")
    state_combo.current(0)
    state_combo.pack(pady=5)
    
    show_bloch_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        frame, text="Show Bloch Spheres", variable=show_bloch_var,
        bg="#f0f0f0", font=("Arial", 9), activebackground="#f0f0f0"
    ).pack(pady=10)
    
    styled_button(
        frame, "Run",
        lambda: launch_teleport(state_combo.get(), show_bloch_var.get()),
        color="#27AE60"
    ).pack(pady=5)

# ───────────── Main Menu ─────────────

def launch_gui():
    dimension_x = 600
    dimension_y = 750  # Increased to fit playground button
    root = tk.Tk()
    root.title("QALS - Quantum Algorithms Learning Suite")
    root.iconphoto(True, tk.PhotoImage(file="assets/QALS-removebg.png"))
    root.geometry(f"{dimension_x}x{dimension_y}")
    root.configure(bg="#2C3E50")
    root.resizable(False, False)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (dimension_x // 2)
    y = (root.winfo_screenheight() // 2) - (dimension_y // 2)
    root.geometry(f"{dimension_x}x{dimension_y}+{x}+{y}")

    # Header
    header_frame = tk.Frame(root, bg="#34495E", height=125)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    tk.Label(
        header_frame, 
        text="⚛️ Quantum Algorithms Learning Suite", 
        font=("Arial", 22, "bold"),
        bg="#34495E", fg="white"
    ).pack(pady=22)
    
    tk.Label(
        header_frame, 
        text="QALS by MicroxOndas", 
        font=("Arial", 12, "italic"),
        bg="#34495E", fg="#BDC3C7",
    ).pack()

    # Content frame
    content_frame = tk.Frame(root, bg="#2C3E50")
    content_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)

    tk.Label(
        content_frame, 
        text="Select an Algorithm", 
        font=("Arial", 14, "italic"),
        bg="#2C3E50", fg="#ECF0F1"
    ).pack(pady=(0, 20))

    # Algorithm buttons
    algorithms = [
        ("🔍 Grover's Algorithm", config_grover, "#3498DB"),
        ("🎲 Deutsch-Jozsa", config_deutsch, "#9B59B6"),
        ("🔗 Bell State", config_bell, "#E67E22"),
        ("🌊 QFT", config_qft, "#1ABC9C"),
        ("📡 Teleportation", config_teleport, "#D7D268")
    ]
    extras = [
        ("🎮 Quantum Playground", launch_playground, "#EF4343")
    ]
    for btn_list in[algorithms, extras]:
        for text, command, color in btn_list:
            btn = tk.Button(
                content_frame, 
                text=text, 
                command=lambda c=command: c(root) if callable(c) and c.__code__.co_argcount > 0 else c(),
                bg=color, fg="white",
                font=("Arial", 13, "bold"),
                relief=tk.FLAT,
                width=45, height=2,
                cursor="hand2",
                activebackground=color,
                bd=0
            )
            btn.pack(pady=6)
            
            # Hover effect
            def on_enter(e, b=btn, c=color):
                b.configure(bg=adjust_color(c, 1.2))
            def on_leave(e, b=btn, c=color):
                b.configure(bg=c)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        tk.Label(
            content_frame, 
            text="or", 
            font=("Arial", 14, "italic"),
            bg="#2C3E50", fg="#ECF0F1"
        ).pack(pady=(10, 10))

    # Exit button
    tk.Button(
        content_frame, 
        text="✖ Exit", 
        command=root.destroy,
        bg="#C0392B", fg="white",
        font=("Arial", 12, "bold"),
        relief=tk.FLAT,
        width=45, height=2,
        cursor="hand2",
        activebackground="#A93226"
    ).pack(pady=10)

    root.mainloop()

def adjust_color(hex_color, factor):
    """Adjusts the brightness of a hexadecimal color."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    return f'#{r:02x}{g:02x}{b:02x}'

if __name__ == "__main__":
    launch_gui()