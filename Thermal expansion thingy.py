import numpy as np

def thermal_forces(fr, E_b, d, alphac, alphab):
  Tmin = -90
  Tmax = 76.1
  Tref = 15
  DeltaTmin = Tmin - Tref
  DeltaTmax = Tmax - Tref
  fr = #import force ratio from compliance
  E_b = #import E_b from compliance

  d = #diameter of the shank
  A = np.pi / 4 * d**2 #stiffness area of the fastener
  alphac = #thermal expansion coefficient of the fastener
  alphab = #thermal expansion coefficient of clamped parts stuff

  FdTmax = (alphac - alphab) * DeltaTmax * E_b * A * (1 - fr)
  FdTmin = (alphac - alphab) * DeltaTmin * E_b * A * (1 - fr)
  return FdTmax, FdTmin
