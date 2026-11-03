import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram, plot_distribution
import sys
import datetime

def main():
    from run_demo_env import get_token
    token, src = get_token()
    if not token:
        sys.exit('Error: IBM Quantum token not found (neither env var nor Credential Manager).')
    print(f'✅ IBM Quantum token obtained from {src}.')

    # Set up service and select a real backend (least busy)
    service = QiskitRuntimeService(token=token)
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=1)
    print(f'🚀 Running on QPU: {backend.name} ({backend.num_qubits} qubits)')

    # Build circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.t(0)
    qc.x(0)
    qc.y(0)
    qc.z(0)
    qc.measure(0, 0)

    # Transpile
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)

    # Execute (1024 shots)
    sampler = Sampler(backend)
    job = sampler.run([isa_circuit], shots=1024)
    print(f'⏳ Job submitted, ID: {job.job_id()}')
    result = job.result()
    counts = result[0].data.c.get_counts()
    print('✅ Job completed. Counts:', counts)

    # Analytics
    total = sum(counts.values())
    print('\nStatistical report')
    print('---------------------')
    print(f'Total shots: {total}')
    for bits, cnt in sorted(counts.items()):
        pct = cnt / total * 100
        print(f' |{bits}⟩ : {cnt} ({pct:.2f}%)')

    # Plotting & saving
    # Ensure output directory exists
    os.makedirs('outputs', exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    plt.figure(figsize=(8,5))
    plot_histogram(counts, title=f'Results on {backend.name}')
    hist_path = os.path.join('outputs', f'histogram_{ts}.png')
    plt.savefig(hist_path)
    plt.close()

    plt.figure(figsize=(8,5))
    plot_distribution(counts, title='Probability distribution')
    dist_path = os.path.join('outputs', f'distribution_{ts}.png')
    plt.savefig(dist_path)
    plt.close()

    states = list(counts.keys())
    values = list(counts.values())
    plt.figure(figsize=(6,6))
    plt.pie(values, labels=[f'|{s}⟩' for s in states], autopct='%1.1f%%', startangle=140)
    pie_path = os.path.join('outputs', f'pie_chart_{ts}.png')
    plt.title(f'Outcome fractions on {backend.name}')
    plt.savefig(pie_path)
    plt.close()

    print(f'Plots saved: {hist_path}, {dist_path}, {pie_path}')

if __name__ == '__main__':
    main()
