calculating = __import__('Calculating Stuff')
import geometry_design
import numpy as np
from itertools import product


Material_names = [
    "AL6061-T6", 
    "AL Alloy 7075-T6", 
    "AL Alloy 2024-T3", 
    "Stainless Steel 316", 
    "Inconel 718", 
    "Maraging Steel 18Ni(250)"
]


normal_yield = np.array([240E6, 503E6, 324E6, 290E6, 1030E6, 1725E6])#Pa
shear_yield = normal_yield/np.sqrt(3)  # Shear yield strengths in MPa
E_moduli = np.array([69, 71.7, 73.1, 193, 205, 210])*10**6  # Young's Moduli in GPa
thermal_expanbsion = np.array([23.6, 23.5, 22.2, 16.0, 13.0, 10.8])*10**-6  # Thermal expansion coefficients in 1/K

material_properties = np.vstack((Material_names, E_moduli, normal_yield, shear_yield)).T


t2 = np.linspace(0.0001, 0.1, 100)
t3 = np.linspace(0.0001, 0.1, 100)



Force1 = np.array([442.2, 1400.25, 442.2])  # Force vector in 3D [Fx, Fy, Fz]
Moment1 = np.array([0.02, 0, 280])  # Moment vector in 3D [Mx, My, Mz]

Force2 = np.array([589.6, 442.2, 589.6])  # Force vector in 3D [Fx, Fy, Fz]
Moment2 = np.array([0.02, 0, 88.44])  # Moment vector in 3D [Mx, My, Mz]



# load_cases = [
#     {
#         "Fx": 442.2 * np.array([1, 0, 0]),
#         "Fy": 442.2 * np.array([0, 1, 0]),
#         "Fz": 1400.25 * np.array([0, 0, 1]),
#         "Mx": 0 * np.array([1, 0, 0]),
#         "My": 280 * np.array([0, -1, 0]),
#         "Mz": 0 * np.array([0, 0, 1]),
#         "F1": np.array([0, 0, 1]),
#     },
#     {
#         "Fx": 589.6 * np.array([1, 0, 0]),
#         "Fy": 589.6 * np.array([0, 1, 0]),
#         "Fz": 442.2 * np.array([0, 0, 1]),
#         "Mx": 0 * np.array([1, 0, 0]),
#         "My": 88.44 * np.array([0, -1, 0]),
#         "Mz": 0 * np.array([0, 0, 1]),
#         "F1": np.array([0, 1, 0]),
#     },
# ]
