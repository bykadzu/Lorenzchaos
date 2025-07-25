from qutip import *
import numpy as np

# Create a three-qubit GHZ state
ghz = (tensor(basis(2,0), basis(2,0), basis(2,0) ) + tensor(basis(2,1), basis(2,1), basis(2,1))).unit()

# Initial density matrix
rho0 = ghz * ghz.dag()

# Time list
times = np.linspace(0, 10, 200)

# Stochastic bath: random telegraph noise + low-frequency sinusoid
# For simplicity, apply a dephasing noise to all qubits with added sinusoid modulation

# Define collapse operators for dephasing on each qubit
c_ops = [np.sqrt(0.1) * tensor(sigmax() if i==0 else qeye(2), sigmax() if i==1 else qeye(2), sigmax() if i==2 else qeye(2)) for i in range(3)]

# Add time-dependent sinusoidal modulation to the rate
def rate(t, args):
    return 0.05 * (1 + np.sin(0.1 * t))  # Low-frequency sinusoid + base rate

c_ops_td = [[c_op, rate] for c_op in c_ops]  # Time-dependent collapse ops

# Hamiltonian: small random field for drift
H = 0.01 * (tensor(sigmax(), qeye(2), qeye(2)) + tensor(qeye(2), sigmay(), qeye(2)) + tensor(qeye(2), qeye(2), sigmaz()))

# Expectation operators: measure coherence, e.g., <X1 X2 X3> for GHZ phase
op = tensor(sigmax(), sigmax(), sigmax())  # Example for off-diagonal coherence proxy

# Solve master equation
result = mesolve(H, rho0, times, c_ops_td, [op])

# Output expectations (full for fun, but abbreviated here)
print("Coherence expectations (first 20):", result.expect[0][:20])
print("Times (first 5):", times[:5])