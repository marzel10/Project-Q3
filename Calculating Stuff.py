import numpy as np


# Calculates the center of gravity of the fasteners
def cg_position(fasteners):
	positions = np.array([f[0] for f in fasteners])  # Extract positions [[x, y, z]]
	diameters = np.array([f[1] for f in fasteners])  # Extract diameters
	areas = np.pi * (diameters / 2) ** 2  # Area of each fastener
	total_area = areas.sum()
	cg = (positions.T @ areas) / total_area  # Weighted average
	return cg  # Return as [x, y, z]

# Returns areas of the fasteners
def get_areas(fasteners):
	diameters = np.array([f[1] for f in fasteners])  # Extract diameters
	return np.pi * (diameters / 2) ** 2

#Returns the vector distances of the fasteners from the origin.
def get_vector_distances(fasteners):
	return np.array([f[0] for f in fasteners])  # [[x, y, z]]

# Returns the scalar distances (magnitudes) of vectors.
def get_scalars(distances):
	return np.linalg.norm(distances, axis=1)

# Calculates force in each fastener to counteract the applied forces and moments
def get_forces(fasteners, F, r_force, M):
	"""
	Parameters:
		fasteners: Array of fasteners, each in the form [[x, y, z], d].
		F: Applied force vector [Fx, Fy, Fz].
		r_force: Location vector of the applied force.
		M: Moment vector [Mx, My, Mz].
	
	Returns:
		Array of forces per fastener in the form [[Fx, Fy, Fz], ...].
	"""
	fasteners_positions = np.array([f[0] for f in fasteners])
	areas = get_areas(fasteners)
	cg = cg_position(fasteners)

	rel_distances = fasteners_positions - cg
	scalar_distances = get_scalars(rel_distances)

	# Reaction forces to counteract the applied force
	F_react_force_1 = (F * areas[:, None]) / areas.sum()

	# Moment due to the applied force
	r_force_rel_cg = np.array(r_force) - cg
	Moment = np.cross(r_force_rel_cg, F) + M  # Moment is now a 3D vector: Mx, My, Mz

	# Forces to counteract the moment
	F_react_force_M = (
		areas[:, None] 
		* np.cross( Moment, rel_distances)  # Cross product with the position relative to CG
	) / (areas * scalar_distances**2).sum()
	return F_react_force_1 + F_react_force_M


# Returns the in-plane bearing stress on the lug and wall in array format [lug, wall][fastener1, fastener2, ...]
def get_inplane_bearing_stress(forces, fasteners, t2, t3):
	diameters = np.array([item[1] for item in fasteners])
	lug_stresses = get_scalars(forces[:,[0,2]])/diameters/t2
	wall_stresses = get_scalars(forces[:,[0,2]])/diameters/t3
	
	return np.vstack((lug_stresses, wall_stresses))

# Returns the safety Margin of 	Each of these thingies
def get_MS_inplane_bearing_stress(inplane_stresses, yield_lug, yield_wall):
	return np.vstack((yield_lug/inplane_stresses[0], yield_wall/inplane_stresses[1]))
	
# Returns the shear stress on the wall and the lug in array format [lug, wall][fastener1, fastener2, ...]
def get_shear_stress(forces, fasteners, t2, t3):
	diameters = np.array([item[1] for item in fasteners])
	shearlug = forces[:,1]/(diameters*np.pi*t2)
	shearwall = forces[:,1]/(diameters*np.pi*t3)
	return np.vstack((shearlug, shearwall))


# Example Usage
fasteners = [
	[[1, 0, 1], 1],
	[[-1, 0, -1], 1]
]

F = np.array([1000, 20, 1000])  # Force vector in 3D [Fx, Fy, Fz]
r_force = [0, 0, 0]  # Applied force location
M = np.array([0,1000, 0])  # Moment vector [Mx, My, Mz]
t2 = .2 # thickness of the lug at connection
t3 = .2 # thickness of the wall


# Moments and forces are in same direction as applied force (they represent the force the structure applies on the fasteners)
# For many forces, do superposition of this function (everything is nice and linear (i think))
print(get_forces(fasteners, F, r_force, M))
forces = get_forces(fasteners, F, r_force, M)
stresses = get_inplane_bearing_stress(forces, fasteners, t2,t3)
shearstresses = get_shear_stress(forces, fasteners, t2, t3)

print(stresses)
print(shearstresses)