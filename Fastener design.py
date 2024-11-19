import numpy as np


def number_of_fastners(D,w,mat): #maximal number of fasteners in one column
    #D is the diameter of one fastener
    #w is the width of the lug
    #mat is the material type, can be either composite or metal

    if mat=="metal": #defining safety factor
        c=2.5
    else:
        c=4.5 #for the composite

    n=np.floor((w-3*D)/c/D)+1 #maximal number of fastners
    return n


#A is an array with coordinates and diameters of all the fasteners in a form: [x,z,d]

def cg_position(A):
    m,n=np.shape(A)
    x_cg=0
    z_cg=0
    area=0
    for i in range(m):
        x_cg += np.pi*A[i][2]**2/4*A[i][0]
        z_cg += np.pi*A[i][2]**2/4*A[i][1]
        area += np.pi*A[i][2]**2 #calculate the total area
    x_cg=x_cg/area
    z_cg=z_cg/area

    return x_cg,z_cg #return position of the center of gravity

A=[[1,1,2],[-1,-1,1]]

print(cg_position(A))