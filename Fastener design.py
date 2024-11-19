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

def position_matrix(zs,xs,col,c,D,H,n):
    if zs<c*D:
        zs=c*D
    if xs<c*D:
        xs=c*D
    l=(n-1)*zs #lenght of the fasteners line
    z1=np.arange(-l/2,l/2+zs,zs) #fasteners will be placed symetrically from 0 axis, +zs included to include the end
    z2=np.arange(-l/2,l/2+zs,zs)
    z=np.concatenate((z1,z2),axis=None)
    xn=np.arange(-(H/2-1.5*D),-(H/2-1.5*D)+(col/2-1)*xs+xs,xs)
    xp=np.arange((H/2-1.5*D)-(col/2-1)*xs,(H/2-1.5*D)+xs,xs)
    x=np.concatenate((xn,xp,xp,xn),axis=None)
    A=np.concatenate((x.reshape(-1,1),z.reshape(-1,1)),axis=1)
    return A

A=[[1,1,2],[-1,-1,1]]

print(cg_position(A))
print(number_of_fastners(2,11,"metal"))
print(position_matrix(0,0,2,2.5,2,50,number_of_fastners(2,11,"metal")))