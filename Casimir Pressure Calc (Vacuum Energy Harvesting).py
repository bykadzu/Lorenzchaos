import sympy as sp
import numpy as np

# Symbols
h_bar, c, d, A = sp.symbols('h_bar c d A')  # h_bar=Planck/2pi, c=light, d=gap, A=area

# Casimir pressure (attractive, negative)
P = - (sp.pi**2 * h_bar * c) / (240 * d**4)

# Energy harvest potential: Force F = P * A, work over delta_d
F = P * A
delta_d = sp.symbols('delta_d')
E_harvest = sp.integrate(F, (d, d, d - delta_d))  # Approximate extraction

# Numerical: h_bar=1.0545718e-34, c=3e8, d=50e-9, A=1e-12 (sq micron), delta_d=1e-12 (attosecond tweak)
vals = {h_bar: 1.0545718e-34, c: 3e8, d: 50e-9, A: 1e-12, delta_d: 1e-12}
P_num = float(P.subs(vals))
E_num = float(E_harvest.subs(vals))

print(f"Pressure: {P_num} Pa")
print(f"Harvested Energy: {E_num} J (per tweak)")