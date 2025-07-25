from qutip import *
import numpy as np

# Simplified quantum kicked rotor (harmonic oscillator basis, N=50 levels)
N = 50
a = destroy(N)
H0 = a.dag() * a  # Free rotor (momentum p^2/2)
H_kick = 5 * (a + a.dag())**2 / 2  # Kick strength K=5

# Initial state: Coherent state alpha=sqrt(12)
psi0 = coherent(N, np.sqrt(12))

# Times and kick periods (10 kicks)
times = np.linspace(0, 10, 101)
kick_times = np.arange(1, 11)

# Evolve free, then kick at integers
result = mesolve(H0, psi0, times, [])

# Apply kicks manually (approximate)
states = [psi0]
for t in kick_times:
    # Evolve to kick time
    result_to_kick = mesolve(H0, states[-1], [0, 1], [])
    # Instant kick (e^{-i H_kick delta_t} ≈ 1 - i H_kick delta_t for small delta_t, but use unitary expm)
    U_kick = (-1j * H_kick).expm()
    post_kick = U_kick * result_to_kick.states[-1]
    states.append(post_kick)

# Expectation of position (number operator for spread)
expect_n = [expect(a.dag() * a, state) for state in states]
print("Quantum kicked rotor <n> fluctuations (spread):", expect_n)