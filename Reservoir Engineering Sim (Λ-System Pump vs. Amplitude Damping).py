import numpy as np
import matplotlib.pyplot as plt
from qutip import *

# System parameters
gamma_loss = 0.05       # amplitude damping rate (|e> to |g> loss)
pump_rate  = 0.2        # increased pump rate (|a> to |e> replenishing)
delta      = 0.0        # detuning for simplicity
times      = np.linspace(0, 50, 500)

# Basis states |g>, |e>, |a>
g = basis(3, 0)
e = basis(3, 1)
a = basis(3, 2)

# Initial state: superposition in computational |g> and |e> subspace
psi0 = (g + e).unit()
rho0 = psi0 * psi0.dag()

# Hamiltonian (pump from auxiliary |a> to excited |e>)
H = delta * e * e.dag()

# Collapse operators
c_ops = [
    np.sqrt(gamma_loss) * g * e.dag(),  # |e> decays to |g>
    np.sqrt(pump_rate)  * e * a.dag()   # pump |a> to |e>
]

# Solve master equation
result = mesolve(H, rho0, times, c_ops, [])

# Fidelity (projected to |g>,|e> subspace)
rho_init_2lvl = psi0 * psi0.dag()
fidelity_reservoir = [fidelity(rho_init_2lvl, (rho.ptrace([0,1])).unit()) for rho in result.states]

# Unprotected (no pump) for comparison
c_ops_unprotected = [np.sqrt(gamma_loss) * g * e.dag()]
result_unprotected = mesolve(H, rho0, times, c_ops_unprotected, [])
fidelity_unprotected = [fidelity(rho_init_2lvl, (rho.ptrace([0,1])).unit()) for rho in result_unprotected.states]

# Plot results
plt.figure(figsize=(8,4))
plt.plot(times, fidelity_unprotected, label='Unprotected qubit', color='gold')
plt.plot(times, fidelity_reservoir, label='Reservoir-pumped qubit', color='crimson')
plt.xlabel('Time')
plt.ylabel('Fidelity')
plt.title('Reservoir Engineering (Λ-system Pump) vs Amplitude Damping')
plt.ylim(0, 1.05)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()