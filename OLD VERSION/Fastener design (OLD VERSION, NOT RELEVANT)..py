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
		area += np.pi*A[i][2]**2/4 #calculate the total area
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

#print(cg_position(A))

def getAreas(fasteners):
	areas = []
	for fastener in fasteners:
		areas.append(fastener[2]*fastener[2]*np.pi/2)
	return np.array(areas)

def getVectorDistances(fasteners):
	 return [[i[0],i[1]] for i in fasteners]

def getScalarDistances(distances):
	return np.sqrt([np.dot(vector,vector) for vector in distances])


## Calculates the force in each fastener to counteract the overall in plane force and moment it may generate + additional moment
##--------------------------------force as 2d vector, location of force, additional moment----  
def getInPlaneFperFastener(fasteners, F, r_force, My):

	x,z =  cg_position(fasteners)
	cg_fasteners = [x,z]
	A_fasteners = getAreas(fasteners)
	distances = getVectorDistances(fasteners)
	dist_rel_center_of_mass = np.array(distances) - np.array(cg_fasteners)
	r_force_REL_center_of_mass = np.array(r_force) - np.array(cg_fasteners)
	scalar_distances_rel_center_of_mass = getScalarDistances(dist_rel_center_of_mass)

	#force in fastener to counteract overall inplane force
	F_react_force_1 = np.full_like(A_fasteners, F) * np.array(A_fasteners)[:, None] / sum(A_fasteners)


	#Moment generated due to force: 
	Moment = r_force_REL_center_of_mass[0]*F[1] - r_force_REL_center_of_mass[1]*F[0]
	Moment += My
	
	#Forces to counteract moment (Net Force = 0, net moment = - Moment
	F_react_force_M = A_fasteners[:,None] * Moment * np.array([[-v[1],v[0]] for v in dist_rel_center_of_mass]) / sum(A_fasteners * scalar_distances_rel_center_of_mass*scalar_distances_rel_center_of_mass)

	return F_react_force_1 + F_react_force_M


print(getInPlaneFperFastener([[1,1,2],[-1,-1,1]], [1000,1000], [0,0], 1000))
