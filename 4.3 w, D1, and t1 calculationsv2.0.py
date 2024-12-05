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

def Ktuf(x):
    coef=[-1.10757616,  3.61431483, - 3.51609595,  0.21966005,  1.28383368]
    Ktu=coef[0]*x**5+coef[1]*x**4+coef[2]*x**3+coef[3]*x**2+coef[4]*x
    return Ktu

def Kbrf(x):
    coef = [-0.07657563,  0.73556647, - 2.56227493,  3.71020721, - 0.85730079]
    Kbr = coef[0] * x ** 5 + coef[1] * x ** 4 + coef[2] * x ** 3 + coef[3] * x ** 2 + coef[4] * x
    return Kbr

def Kuf(x):
    coef = [ 0.00520646, -0.08747833,  0.54885174, -1.59859635,  2.10344953]
    Ku = coef[0] * x ** 5 + coef[1] * x ** 4 + coef[2] * x ** 3 + coef[3] * x ** 2 + coef[4] * x
    return Ku
# Design parameters
D = np.linspace(0.01, 0.09, 100)
w = np.linspace(0.01, 0.1, 100)
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
sm=[] #an array that stores ratios between aplied and allowable forces
# Other parameters
n_lugs = 2
sf = 2
MS = sf - 1
conf=[0,0,0,10E9]
for Ds in D:
    for ts in t:
        for ws in w:
            if ws <= Ds + 0.001:  # Skip invalid configurations
                continue
            Afr = ws**2 + 1/2 * (np.pi * (ws/2)**2) - np.pi * (Ds/2)**2  #L*ws becomes ws^2
            l1 = ws/2- Ds*np.sqrt(2)/4
            l2 = (ws-Ds)/2
            #l2 = (ws-Ds)*ts/2
            Abr = Ds * ts
            A1 = l1 * ts
            A2 = l2 * ts
            Aav = 6/(4/A1+2/A2)
            ratio = Aav/Abr

            if ratio>1.1:
                continue
            Ktu = Ktuf(ratio)
            h = 0.142

            for i in range(1):
                # Determine P
                if n_lugs == 1:
                    Fa = load_cases[0]["Fx"] + load_cases[0]["F1"]
                    Fa1 = load_cases[1]["Fx"] + load_cases[1]["F1"]
                    Ftr = load_cases[0]["Fy"]
                    Ftr1 = load_cases[1]["Fy"]
                    P_abs = np.sqrt(load_cases[0]["Fx"]**2 + load_cases[0]["Fy"]**2)
                    P_abs1 = np.sqrt(load_cases[1]["Fx"] ** 2 + load_cases[1]["Fy"] ** 2)
                    #P_angle = np.atan2(P[0], P[1])
                elif n_lugs == 2:
                    Fa = load_cases[0]["Fx"] + load_cases[0]["F1"]
                    Fa1 = load_cases[1]["Fx"] + load_cases[1]["F1"]
                    Ftr = load_cases[0]["Fy"]
                    Ftr1 = load_cases[1]["Fy"]
                    P_abs = np.sqrt(load_cases[0]["Fx"]**2 + load_cases[0]["Fy"]**2)
                    P_abs1 = np.sqrt(load_cases[1]["Fx"] ** 2 + load_cases[1]["Fy"] ** 2)/2
                    #P_angle = np.atan2(P[0], P[1])


                F_tr_allow = Ktu * Abr * mprops[0]

                Rtr = Ftr/F_tr_allow
                Rtr1 = Ftr1 / F_tr_allow
                #Ra = ((1 / (MS + 1))**1.6 - Rtr**1.6)**(1 / 1.6)
                #Ra = Fa/F_a_allowed

                # calculate mass
                mass = mprops[1] * ts * Afr
                maxrtr=0

                if Rtr<1 and Rtr1<1:
                    if conf[3]>mass: #if mass of the working configuration is smaller than the previous working configuration
                        maxrtr=Rtr #set maximal safety margin as Rtr
                        conf[0]=Ds #set diameter of the final configuration as Ds
                        conf[1]=ts #set thickness of the final configuration as ts
                        conf[2]=ws #set width of the final configuration as ws
                        conf[3]=mass #set mass of the final configuration as mass
                        print(mass)
                    Dlist.append(Ds)
                    tlist.append(ts)
                    wlist.append(ws)
                    mlist.append(mass)

                sm.append(maxrtr)
#print(Dlist)
#print(tlist)
#print(wlist)
#print(mlist)
#print(min(mlist))
print(conf)
check=np.zeros(2)

for i in range(2):
    # Determine P
    if n_lugs == 1:
        Fa = load_cases[i]["Fx"] + load_cases[i]["F1"]
        Ftr = load_cases[i]["Fy"]
        P_abs = np.sqrt(load_cases[i]["Fx"] ** 2 + load_cases[i]["Fy"] ** 2)
        # P_angle = np.atan2(P[0], P[1])

    elif n_lugs == 2:
        Fa = load_cases[i]["Fx"] + load_cases[i]["F1"]
        Ftr = load_cases[i]["Fy"]
        P_abs = (np.sqrt(load_cases[i]["Fx"] ** 2 + load_cases[i]["Fy"] ** 2)) / 2

    At=(conf[2]-conf[0])/2*conf[1]
    Abr=conf[0]*conf[1]
    Kt=Kuf(conf[2]/conf[0])
    Kbr=Kbrf((conf[0]/2+(conf[2]-conf[0])/2)/conf[0])

    Pu=Kt*At*510E6
    Pbru=Kbr*Abr*510E6
    P=np.min([Pu,Pbru])
    Ra=Fa/P
    sm.append(Ra)

    if Ra<1: #check if the configuration is F_applied<F_allow
        check[i]=1


if check[0]==1 and check[1]==1: #if F_applied<F_allow for both load cases
    print(f"The design values are: diameter {np.round(conf[0],3)}m, thickness {conf[1]}m and width {conf[2]}, mass{conf[3]}kg")
    print(f"Safety margins are: Axial scenario 1: {sm[2]}, Axial scenario 2: {sm[3]}, transverse scenario 1 {sm[0]} and transverse scenario 2 {sm[1]}")
# Check for failure due to Fz/Fx