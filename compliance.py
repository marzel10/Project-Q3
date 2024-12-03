import numpy as np



def compliance_b(d_nom, d_minor, E_b, E_n,ht,t_1,t_2):
    #d_nom - nominal diameter of the fastener (from the standard specs)
    #d_minor - minor diameter of the fastener (from the standard specs)
    #t1 - thickness of the lug (from previous design steps)
    #t2 - thickness of the spacecraft wall (from prevoius work packedges*)
    #E_b, E_n - youngs modulus of the bolt and nut
    #ht - head type (Hexagon or cylindrical)
    #st - shank type (nut tightened or threaded hole)

    if ht=="Hexagon":
        Lh=0.5*d_nom
    else:
        Lh=0.4*d_nom


    Ls=0.4*d_nom

    Ls=0.33*d_nom

    Ln=0.4*d_nom
    A_nom=np.pi*d_nom**2/4
    A_min=np.pi*d_minor**2/4


    com_b=(Lh/A_nom+Ls/A_min+(t_1+t_2)/A_nom)/E_b+Ln/E_n/A_nom

    return com_b

def compliance_a(t,D_out,D_in,E_a):
    #t thickness of the plate
    #D_out diameter of the head
    #D_in diameter of the shank
    #E_a young modulus of the attached part (lug plate or the s/c wall)
    com_a=4*t/(E_a*np.pi*(D_out**2-D_in**2))

    return com_a

def force_ratio(d_nom, d_minor, E_b, E_n,ht,t_1,D_out,E_p,t_2,E_w):
    # t_1 - thickness of the lug (from previous design steps)
    # t_2 - thickness of the spacecraft wall (from prevoius work packedges*)
    # E_p - young modulus of the plate
    # E_w - young modulus of the wall

    fr=(compliance_a(t_1,D_out,d_nom,E_p)+compliance_a(t_2,D_out,d_nom,E_w))/(compliance_a(t_1,D_out,d_nom,E_p)+compliance_a(t_2,D_out,d_nom,E_w)+compliance_b(d_nom,d_minor, E_b, E_n,ht,t_1,t_2))

    return fr

