'''
This Python script is used to support calculations done in deliverable 3.4.
It builds upon the results found in deliverables 4.1 and 4.2.

Created by: Luuk Valkering
Worked on by: Luuk Valkering and Evan de Vries
Created on 19-11-2024 (v1.0)
    Version 1.1: Proof that method for Rtr works
    Version 2.0: Calculate Ra and Rtr seperately and minimize safety factor
'''
from operator import index

# IMPORTANT: use safety factors and reason why! Also reason, mention and label your assumptions.
# Import packages
import numpy as np

# Design parameters
D = np.linspace(0.01, 0.2, 100)
w = np.linspace(0.01, 0.2, 100)
t = np.linspace(0.005, 0.05, 100)
#L = w #assumption: L = w


yieldlist = [240E6, 503E6, 324E6, 290E6, 1030E6, 1725E6]#Pa
densitylist = [2.7E3, 2.81E3, 2.78E3, 8E3, 8.19E3, 8E3]    #kg/m^3
print("The material numbers are: AL6061-T6 (1), AL Alloy 7075-T6 (2), AL Alloy 2024-T3 (3)")
print("Stainless steel 316 (4), Inconel 718 (5) Maraging Steel 18Ni(250) (6)")
matnumber = int(input("Please choose your material number:"))
mprops = (yieldlist[matnumber], densitylist[matnumber])

# Forces and moments acting on the lug
# Assume Fx or Fz = 0.1P if Fx or Fz  = 0
load_cases = [
    {
        "Fx": 442.2,
        "Fy": 442.2,
        "Fz": 1400.25,
        "Mx": 0,
        "My": -280,
        "Mz": 0,
        "F1": 0,
    },
    {
        "Fx": 589.6,
        "Fy": 589.6,
        "Fz": 442.2,
        "Mx": 0,
        "My": -88.44,
        "Mz": 0,
        "F1": 0,
    },
]

Dlist = []
tlist = []
wlist = []
mlist = []

# Other parameters
n_lugs = 2
sf = 2
MS = sf - 1

for Ds in D:
    for ts in t:
        for ws in w:
            if ws <= Ds + 0.001:  # Skip invalid configurations
                continue
            Afr = ws**2 + 1/2 * (np.pi * (ws/2)**2) - np.pi * (Ds/2)**2  #L*ws becomes ws^2
            l1 = ws/2- Ds*np.sqrt(2)/4
            l2 = (ws-Ds)*ts/2
            Abr = Ds * ts
            A1 = l1 * ts
            A2 = l2 * ts
            Aav = 6/(4/A1+2/A2)
            ratio = Aav/Abr
            Kty = -0.323*ratio**2+1.365*ratio
            h = 0.142

            for i in range(2):
                # Determine P
                if n_lugs == 1:
                    Fa = load_cases[i]["Fx"] + load_cases[i]["F1"]
                    Ftr = load_cases[i]["Fy"]
                    P_abs = np.sqrt(load_cases[i]["Fx"]**2 + load_cases[i]["Fy"]**2)
                    #P_angle = np.atan2(P[0], P[1])

                elif n_lugs == 2:
                    Fa = load_cases[i]["Fx"] + load_cases[i]["F1"]
                    Ftr = load_cases[i]["Fy"]
                    P_abs = (np.sqrt(load_cases[i]["Fx"]**2 + load_cases[i]["Fy"]**2))/2
                    #P_angle = np.atan2(P[0], P[1])

                F_tr_allow = Ktu * Abr * mprops[0]
                Rtr = Ftr/F_tr_allow
                #Ra = ((1 / (MS + 1))**1.6 - Rtr**1.6)**(1 / 1.6)
                #Ra = Fa/F_a_allowed

                # calculate mass
                mass = mprops[1] * t * Afr
                maxrtr=0
                conf=[0,0,0]
                if Rtr<1:
                    if Rtr>maxrtr:
                        maxrtr=Rtr
                        conf[0]=Ds
                        conf[1]=ts
                        conf[2]=ws
                    Dlist.append(Ds)
                    tlist.append(ts)
                    wlist.append(ws)
                    mlist.append(mass)
#print(Dlist)
#print(tlist)
#print(wlist)
#print(mlist)
#print(min(mlist))
print(maxrtr,conf)

# Check for failure due to Fz/Fx