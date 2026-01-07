![](https://github.com/MicroxOndas/QALS/blob/main/assets/QALS.jpg)


# QALS - Quantum Algorithms Learning Suite

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![uv](https://img.shields.io/badge/uv-latest-orange.svg)
![Qiskit](https://img.shields.io/badge/qiskit-latest-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**QALS** (Quantum Algorithms Learning Suite) is an interactive educational platform for learning and visualizing quantum computing algorithms. Built with Python, Qiskit, and Matplotlib, it provides step-by-step visualizations of quantum algorithms with real-time Bloch sphere representations and probability distributions.

**Powered by uv** - Ultra-fast Python package management for reliable and quick dependency installation.

---

## 🌟 Features

### Interactive Algorithm Visualizations
- **Step-by-step navigation** through quantum algorithms
- **Real-time Bloch sphere** visualization for each qubit
- **Probability histograms** showing measurement outcomes
- **Circuit diagrams** displaying accumulated quantum operations
- **Operation history** tracking all applied gates

### Supported Quantum Algorithms

1. **Grover's Algorithm** 🔍
   - Quantum search in unsorted databases
   - Configurable number of qubits and target state
   - Optimal iteration calculation
   - Visual breakdown of oracle and diffusion operators

2. **Deutsch-Jozsa Algorithm** 🎲
   - Determines if a function is constant or balanced
   - Single-query solution to a classical multi-query problem
   - Configurable oracle types

3. **Bell States** 🔗
   - Creation of all four maximally entangled Bell states (Φ+, Φ-, Ψ+, Ψ-)
   - Visual demonstration of quantum entanglement
   - Individual or batch generation

4. **Quantum Fourier Transform (QFT)** 🌊
   - Core component of Shor's algorithm
   - Configurable initial states
   - Step-by-step phase rotations and swaps

5. **Quantum Teleportation** 📡
   - Transfer quantum states using entanglement
   - Demonstrates EPR pairs and quantum measurement
   - Multiple initial state options

6. **Quantum Playground** 🎮 *(NEW)*
   - Interactive gate experimentation environment
   - Real-time state manipulation
   - Matrix representations on hover
   - 12 quantum gates available

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8 or higher
uv (ultra-fast Python package manager)
```

### Installation

1. **Install uv** (if not already installed)
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

2. **Clone the repository**
```bash
git clone https://github.com/MicroxOndas/QALS.git
cd QALS
```

3. **Install dependencies with uv**
```bash
uv pip install -r requirements.txt
```

Or use uv to run directly:
```bash
uv run main-gui.py
```

Required packages:
- `qiskit` - Quantum computing framework
- `numpy` - Numerical computations
- `matplotlib` - Visualization
- `tkinter` - GUI (usually comes with Python)

4. **Run QALS**
```bash
uv run main-gui.py
```

### Why uv?

QALS uses **uv** for dependency management because it's:
- ⚡ **10-100x faster** than pip
- 🔒 **More reliable** with better dependency resolution
- 🎯 **Drop-in replacement** for pip
- 🚀 **Modern** Python tooling

Learn more about uv at [astral.sh/uv](https://astral.sh/uv)

---

## 📖 Usage Guide

### Main Menu

Launch QALS to see the main menu with all available algorithms:

```
⚛️ Quantum Algorithms Learning Suite
QALS by MicroxOndas

Select an Algorithm:
🔍 Grover's Algorithm
🎲 Deutsch-Jozsa
🔗 Bell State
🌊 QFT
📡 Teleportation

or

🎮 Quantum Playground
```

### Algorithm Configuration

Each algorithm has a configuration window where you can:
- Set the number of qubits
- Configure algorithm-specific parameters
- Toggle Bloch sphere visualization
- Choose initial states

### Interactive Visualizer

All algorithms use the same powerful interactive visualizer:

**Navigation Controls:**
- **Slider**: Move between algorithm steps
- **Previous/Next buttons**: Step backward/forward
- **Keyboard shortcuts**: Arrow keys for navigation

**Display Components:**
- **Bloch Spheres**: 3D representation of each qubit's state
  - Pure states: Blue vectors
  - Mixed states (entangled): Red vectors or purple center points
- **Probability Histogram**: Measurement outcome probabilities
- **Circuit Display**: Accumulated quantum gates
- **State Information**: Current step description

---

## 🎮 Quantum Playground

The **Quantum Playground** is an interactive environment for experimenting with single-qubit quantum gates.

### Features

**Parameter Control:**
- **θ (theta) slider**: Polar angle (0 to π)
- **φ (phi) slider**: Azimuthal angle (0 to 2π)
- **Rotation slider**: Parameter for RX, RY, RZ gates

**Available Gates:**
- **Pauli Gates** (Blue): X, Y, Z
- **Hadamard** (Purple): H
- **Phase Gates** (Orange/Green): S, T, S†, T†
- **Rotation Gates** (Red): RX, RY, RZ
- **Identity**: I

**Preset States:**
- |0⟩ (Ground)
- |1⟩ (Excited)
- |+⟩ (Plus)
- |-⟩ (Minus)
- |i⟩ (Plus-Y)
- |-i⟩ (Minus-Y)

**Interactive Features:**
- Hover over gates to see their matrix representation
- Real-time Bloch sphere updates
- Operation history tracking
- Undo functionality

### Example Workflow

```python
1. Start with |0⟩ state
2. Apply H gate → Creates superposition
3. Apply S gate → Adds phase
4. Observe changes in:
   - Bloch sphere position
   - Probability distribution
   - State vector representation
```

---

## 🏗️ Project Structure

```
qals/
├── main-gui.py                    # Main application entry point
├── requirements.txt               # Python dependencies
├── assets/
│   └── QALS-removebg.png         # Application icon
│
├── algorithms/
│   ├── grover.py                 # Grover's algorithm implementation
│   ├── deutsch_jozsa.py          # Deutsch-Jozsa algorithm
│   ├── bell_states.py            # Bell states creation
│   ├── qft.py                    # Quantum Fourier Transform
│   └── teleportation.py          # Quantum teleportation
│
├── logic/
│   └── quantum_playground.py     # Playground state management
│
└── utils/
    ├── visualizer_utils.py       # Core visualization components
    └── playground_visualizer.py  # Playground UI
```

---

## 🔧 Technical Details

### Architecture

**Core Components:**

1. **QuantumStepSimulator**
   - Records each step of quantum algorithms
   - Maintains state vector history
   - Manages quantum circuit composition

2. **InteractiveStepVisualizer**
   - Handles UI rendering and interactions
   - Updates Bloch spheres, histograms, and circuits
   - Manages slider and button widgets

3. **QuantumPlayground**
   - Single-qubit state manipulation
   - Gate application with history
   - State-to-Bloch conversion utilities

### Technology Stack

**Package Management:**
- **uv** - Ultra-fast Python package installer and resolver
  - Replaces pip with 10-100x speed improvement
  - Written in Rust for maximum performance
  - Better dependency resolution and conflict handling
  - Compatible with pip requirements files

**Core Dependencies:**
- **Qiskit** - IBM's quantum computing SDK
- **NumPy** - Numerical computing
- **Matplotlib** - Scientific visualization
- **Tkinter** - Cross-platform GUI framework

### Visualization Features

**Bloch Sphere Rendering:**
- Custom colors for different state types
- Arrow mutation for visibility
- Automatic state detection (pure/mixed/entangled)

**Enhanced UI:**
- Gradient color schemes
- Responsive layouts
- Hover effects and animations
- Professional matplotlib styling

**State Indicators:**
- 🔗 Maximally entangled qubits
- ⚡ Partially entangled states
- Color-coded qubit titles

---

## 📚 Educational Value

QALS is designed for:

### Students
- Visual understanding of abstract quantum concepts
- Interactive experimentation without coding
- Step-by-step algorithm walkthroughs

### Educators
- Classroom demonstrations
- Assignment creation
- Visual aids for lectures

### Researchers
- Quick prototyping of quantum circuits
- Algorithm visualization for presentations
- Educational outreach

---

## 🎓 Learning Resources

### Understanding Quantum Gates

**Pauli Gates:**
- **X Gate**: Bit flip (quantum NOT)
  ```
  X|0⟩ = |1⟩
  X|1⟩ = |0⟩
  ```

- **Y Gate**: Bit flip + phase flip
  ```
  Y = iXZ
  ```

- **Z Gate**: Phase flip
  ```
  Z|0⟩ = |0⟩
  Z|1⟩ = -|1⟩
  ```

**Hadamard Gate:**
- Creates superposition
  ```
  H|0⟩ = (|0⟩ + |1⟩)/√2 = |+⟩
  H|1⟩ = (|0⟩ - |1⟩)/√2 = |-⟩
  ```

**Phase Gates:**
- **S Gate**: π/2 phase rotation
- **T Gate**: π/4 phase rotation

**Rotation Gates:**
- **RX(θ)**: Rotation around X-axis
- **RY(θ)**: Rotation around Y-axis
- **RZ(θ)**: Rotation around Z-axis

### Bloch Sphere Interpretation

The Bloch sphere is a geometric representation of a qubit state:
- **North pole (|0⟩)**: θ = 0
- **South pole (|1⟩)**: θ = π
- **Equator**: Superposition states
- **Azimuthal angle (φ)**: Phase information

### Quantum Algorithms Explained

**Grover's Algorithm:**
- **Problem**: Find marked item in unsorted database
- **Classical**: O(N) queries
- **Quantum**: O(√N) queries
- **Key concept**: Amplitude amplification

**Deutsch-Jozsa:**
- **Problem**: Determine if function is constant or balanced
- **Classical**: Up to 2^(n-1) + 1 queries
- **Quantum**: 1 query
- **Key concept**: Quantum parallelism

**Bell States:**
- **Concept**: Maximally entangled two-qubit states
- **Property**: Measuring one qubit instantly affects the other
- **Application**: Quantum teleportation, superdense coding

---

## 🐛 Troubleshooting

### Common Issues

**Problem**: Bloch spheres don't update
- **Solution**: Check matplotlib backend supports interactive mode
- Try: `matplotlib.use('TkAgg')` or `matplotlib.use('Qt5Agg')`

**Problem**: Gates don't respond
- **Solution**: Ensure qiskit is properly installed
- Verify: `uv pip list | grep qiskit`

**Problem**: GUI doesn't appear
- **Solution**: Check tkinter installation
- Test: `python -m tkinter`

**Problem**: Slow rendering
- **Solution**: Disable Bloch spheres for large circuits
- Reduce number of qubits if possible

**Problem**: History doesn't show
- **Solution**: Maximize window for better visibility
- Check console for error messages

**Problem**: Dependencies not installing
- **Solution**: Make sure uv is properly installed
- Try: `uv --version`
- Reinstall: `uv pip install --reinstall -r requirements.txt`

**Problem**: uv command not found
- **Solution**: Add uv to your PATH or reinstall
- Check: `echo $PATH | grep .cargo/bin`

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Adding New Algorithms

1. Create algorithm file in `algorithms/`
2. Implement using `QuantumStepSimulator`
3. Add configuration window in `main-gui.py`
4. Update this README

### Improving Visualizations

- Enhance Bloch sphere rendering
- Add new visualization modes
- Improve UI responsiveness

### Bug Reports

Please include:
- Operating system
- Python version
- Qiskit version
- Steps to reproduce
- Error messages

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**MicroxOndas**

Created as an educational tool for quantum computing enthusiasts.

---

## 🙏 Acknowledgments

- **Astral (uv team)**: For creating the ultra-fast Python package manager
- **IBM Qiskit Team**: For the excellent quantum computing framework
- **Matplotlib Community**: For powerful visualization tools
- **Quantum Computing Community**: For educational resources and inspiration

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/MicroxOndas/QALS/issues)

---

## 🔮 Future Roadmap

### Planned Features

- [ ] **Multi-qubit Playground**: Extend playground to 2-3 qubits
- [ ] **Custom Circuit Builder**: Drag-and-drop circuit creation
- [ ] **Export Functionality**: Save circuits and visualizations
- [ ] **More Algorithms**: 
  - Shor's algorithm
  - Quantum Approximate Optimization Algorithm (QAOA)
- [ ] **Interactive Tutorials**: Step-by-step guided lessons
- [ ] **Animation Mode**: Automatic step progression

### Community Requests

Want a feature? Open an issue!

---

## 📊 Project Stats

- **Languages**: Python
- **Package Manager**: uv (ultra-fast)
- **Frameworks**: Qiskit, Matplotlib, Tkinter
- **Lines of Code**: ~3000+
- **Quantum Gates**: 12+
- **Algorithms**: 6
- **Visualization Components**: 5

---

## 🎯 Use Cases

### Academic
- University quantum computing courses
- High school physics demonstrations
- Online quantum computing workshops

### Professional
- Research presentations
- Team training sessions

### Personal
- Self-learning quantum computing
- Algorithm exploration
- Visual experimentation

---

## 💡 Tips & Tricks

1. **Start Simple**: Begin with Bell states to understand entanglement
2. **Use Presets**: Quantum Playground presets are great learning tools
3. **Watch History**: Operation history shows the sequence of gates
4. **Experiment**: Try different gate combinations in the playground
5. **Compare**: Run same algorithm with different parameters
6. **Read Matrices**: Hover over gates to see their mathematical form

---

## 📖 References

### Quantum Computing Resources

- [Qiskit Textbook](https://qiskit.org/textbook/)
- [Quantum Computing for the Very Curious](https://quantum.country/)
- [Nielsen & Chuang: Quantum Computation and Quantum Information](https://en.wikipedia.org/wiki/Quantum_Computation_and_Quantum_Information)

### Bloch Sphere
- [Bloch Sphere Visualization](https://en.wikipedia.org/wiki/Bloch_sphere)
- [Understanding the Bloch Sphere](https://www.quantum-inspire.com/kbase/bloch-sphere/)

### Quantum Algorithms
- [Grover's Algorithm Explained](https://qiskit.org/textbook/ch-algorithms/grover.html)
- [Deutsch-Jozsa Algorithm](https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html)

---

<div align="center">

**Made with ❤️ for the quantum computing community**

⚛️ **QALS** - Making Quantum Computing Visual and Accessible

[⬆ Back to Top](#qals---quantum-algorithms-learning-suite)

</div>
