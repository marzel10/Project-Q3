'''
This Python script is used to support calculations done in deliverable 3.4.
It builds upon the results found in deliverables 4.1 and 4.2.

Created by: Luuk Valkering
Worked on by: Luuk Valkering and Evan de Vries
Created on 19-11-2024 (v1.0)
    Version 1.1: ...
    Version 2.0: ...
'''
from operator import index

# IMPORTANT: use safety factors and reason why! Also reason, mention and label your assumptions.
# Import packages
import numpy as np


def Ktuf(x):
    coef=[-1.10757616,  3.61431483, - 3.51609595,  0.21966005,  1.28383368]
    Ktu=coef[0]*x**5+coef[1]*x**4+coef[2]*x**3+coef[3]*x**2+coef[4]*x
    return Ktu

# Design parameters
D = np.linspace(0.001, 0.4, 100)
w = np.linspace(0.001, 0.5, 100)
t = np.linspace(0.001, 0.1, 100)
L = w #assumption: L = w


yieldlist = [240E6, 503E6, 324E6, 290E6, 1030E6, 1725E6]#Pa
densitylist = [2.7E3, 281E3, 2.78E3, 8E3, 8.19E3, 8E3]    #kg/m^3
print("The material numbers are: AL6061-T6 (1), AL Alloy 7075-T6 (2), AL Alloy 2024-T3 (3)")
print("Stainless steel 316 (4), Inconel 718 (5) Maraging Steel 18Ni(250) (6)")
matnumber = int(input("Please choose your material number:"))
mprops = (yieldlist[matnumber], densitylist[matnumber])

# Forces and moments acting on the lug
# Assume Fx or Fz = 0.1P if Fx or Fz  = 0
load_cases = [
    {
        "Fx": 442.2 * np.array([1, 0, 0]),
        "Fy": 442.2 * np.array([0, 1, 0]),
        "Fz": 1400.25 * np.array([0, 0, 1]),
        "Mx": 0 * np.array([1, 0, 0]),
        "My": 280 * np.array([0, -1, 0]),
        "Mz": 0 * np.array([0, 0, 1]),
        "F1": np.array([0, 0, 1]),
    },
    {
        "Fx": 589.6 * np.array([1, 0, 0]),
        "Fy": 589.6 * np.array([0, 1, 0]),
        "Fz": 442.2 * np.array([0, 0, 1]),
        "Mx": 0 * np.array([1, 0, 0]),
        "My": 88.44 * np.array([0, -1, 0]),
        "Mz": 0 * np.array([0, 0, 1]),
        "F1": np.array([0, 1, 0]),
    },
]

Dlist = []
tlist = []
wlist = []
mlist = []

# Other parameters
n_lugs = 2

for Ds in D:
    for ts in t:
        for ws in w:
            if ws <= Ds + 0.001:  # Skip invalid configurations
                continue

                Afr = L*w + 1/2 * (np.pi * (w/2)**2) - np.pi * (D/2)**2
                l1 = w/2- D*np.sqrt(2)/4
                l2 = (w-D)*t/2
                Abr = D * t
                A1 = l1 * t
                A2 = l2 * t
                Aav = 6/(4/A1+2/A2)
                ratio = Aav/Abr
                Ktu = Ktu(ratio)
                sf = 2
                MS = sf - 1
                h = 0.142


                for i in range(2):
                    # Determine P
                    if n_lugs == 1:
                        P = load_cases[i]["Fx"] + load_cases[i]["Fy"]
                        P_abs = np.sqrt(load_cases[i]["Fx"]**2 + load_cases[i]["Fy"]**2)
                        P_angle = np.atan2(P[0], P[1])

                    elif n_lugs == 2:
                        P = (load_cases[i]["Fx"] + load_cases[i]["Fy"])/2 #removed f1 for clarity
                        P_abs = (np.sqrt(load_cases[i]["Fx"]**2 + load_cases[i]["Fy"]**2**2))/2
                        P_angle = np.atan2(P[0], P[1])


                    Fa = load_cases[i]["Fz"]
                    Ftr = P_abs

                    F_tr_allow = Ktu * Abr * mprops[0]
                    Rtr = Ftr/F_tr_allow
                    Ra = ((1 / (MS + 1))**1.6 - Rtr**1.6)**(1 / 1.6)

                    # calculate mass
                    mass = mprops[1] * t * Afr
                    if Rtr < 1 and Ra < 1:
                        Dlist.append(Ds)
                        tlist.append(ts)
                        wlist.append(ws)
                        mlist.append(mass)
print(min(mlist))

# Check for failure due to Fz/Fx