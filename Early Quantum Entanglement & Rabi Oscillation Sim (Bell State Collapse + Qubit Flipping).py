from qutip import *
import numpy as np
from numpy.random import choice

# Bell state entanglement
up = basis(2, 0)
down = basis(2, 1)
bell = (tensor(up, up) + tensor(down, down)).unit()
rho = bell * bell.dag()

P_up = tensor(up * up.dag(), qeye(2))
P_down = tensor(down * down.dag(), qeye(2))

prob_up = expect(P_up, rho)
prob_down = expect(P_down, rho)

chosen = choice(['up', 'down'], p=[prob_up, prob_down])
outcome = '0 (up, +1)' if chosen == 'up' else '1 (down, -1)'

if chosen == 'up':
    projector = P_up
else:
    projector = P_down
collapsed = (projector * bell).unit()

print(f"Measurement outcome on first qubit: {outcome}")
print("Collapsed state:")
print(collapsed)

# Rabi oscillation
H = 2 * np.pi * 0.1 * sigmax()
psi0 = up
times = np.linspace(0, 10, 100)
result = mesolve(H, psi0, times, [], [sigmaz()])

print("\nRabi oscillation expectation <sigma_z> at t=0,2,4,6,8:")
print(result.expect[0][[0,20,40,60,80]])