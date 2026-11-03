# IBM Quantum Hardware Explorer Demo

This repository contains a minimal but complete example that:

1. Connects to **IBM Quantum** using your personal API token.
2. Builds a single‑qubit circuit with several gates.
3. Transpiles the circuit for a real quantum processor.
4. Executes the circuit on a real QPU (default: the least‑busy device).
5. Collects measurement statistics and visualises the results with three plots:
   - Qiskit histogram
   - Probability distribution
   - Pie chart of outcome fractions

The demo is provided as a Jupyter notebook (`quantum_demo.ipynb`) that can be run locally or on **Google Colab**.  A small helper script (`run_demo.py`) is also included for people who prefer a pure‑Python execution.

---

## Prerequisites

- Python 3.9+ (the notebook was tested with Python 3.11).
- An **IBM Quantum API token**.  You can obtain one from the [IBM Quantum Platform](https://quantum-computing.ibm.com/).

## Quick start (Colab)

1. Open the notebook in Colab:
   - Upload `quantum_demo.ipynb` to your Google Drive, then use **File → Open notebook → Google Drive**.
   - Alternatively, if the repository is public on GitHub, replace `YOUR_USERNAME/REPO` in the URL:
     ```
     https://colab.research.google.com/github/YOUR_USERNAME/REPO/blob/main/quantum_demo.ipynb
     ```
2. In the first code cell, set your token:
   ```python
   import os
   os.environ['IBM_QUANTUM_TOKEN'] = 'YOUR_IBM_QUANTUM_TOKEN'
   ```
3. Run all cells.  The notebook will install required packages, select a real device, submit the job, wait for the result, and display the three plots.

## Running locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ibm-quantum-hardware-explorer.git
cd ibm-quantum-hardware-explorer

# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate   # on Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Export your IBM token (do NOT commit it!)
set IBM_QUANTUM_TOKEN=YOUR_IBM_QUANTUM_TOKEN   # Windows cmd
# or
export IBM_QUANTUM_TOKEN=YOUR_IBM_QUANTUM_TOKEN   # Bash

# Run the pure‑Python version
python run_demo.py
```

The script prints the same statistical report and saves the three plots as PNG files (`histogram.png`, `distribution.png`, `pie_chart.png`).

## Project structure

```
├─ quantum_demo.ipynb    # Full notebook version (Colab‑ready)
├─ run_demo.py           # Minimal script version
├─ requirements.txt      # Python dependencies
├─ .gitignore            # Ignored files
├─ README.md             # This file
└─ .github/workflows/    # CI (optional)
```

---

## Continuous Integration (optional) ✅

A lightweight GitHub Actions workflow is provided to ensure the notebook can be executed in a clean environment on every push.  It installs the dependencies, runs `run_demo.py` (which is non‑interactive), and uploads the generated plots as artifacts.  This helps catch breaking changes early.

---

## License

This demo is released under the **MIT License** – feel free to fork, modify, and share.
