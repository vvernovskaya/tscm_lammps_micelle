import pickle
import multiprocessing as mp
import sys

N_STEPS = 1000
STEP_STEPS = 50
N_TYPES = 4
'''
Number of particles of each type (had to count here since 
no information is in data.micelle or def.micelle).
'''
N_PARTICLES = [0] * N_TYPES
N_PARAMS = int(sys.argv[1])

NUM_CPU = 4


def count_particles(step_coords):
	for i in range(len(step_coords)):
		N_PARTICLES[int(step_coords[i][1])-1] += 1 


def count_msd(start_coords, curr_step_coords, all_types_msds):
	for i in range(N_TYPES):
		all_types_msds[i].append(0)
	for i in range(len(curr_step_coords)): 	# going through all the particles on this step
		all_types_msds[int(curr_step_coords[i][1])-1][len(all_types_msds[int(curr_step_coords[i][1])-1])-1] += \
								(curr_step_coords[i][2] - start_coords[i][2])**2 + \
							      (curr_step_coords[i][3] - start_coords[i][3])**2
	for i in range(N_TYPES):
		all_types_msds[i][len(all_types_msds[i])-1] /= N_PARTICLES[i]


def run_msd_one_param(all_coords):
	print("-- -- -- started msd calculation function")
	all_msds_one_param = [ [] for _ in range(N_TYPES) ]
	start_coords = all_coords[0]
	for j in range(int(N_STEPS / STEP_STEPS)):
                count_msd(start_coords, all_coords[j], all_msds_one_param)
	
	return all_msds_one_param


with open('coords.pickle', 'rb') as f:
	'''
	This is an array of arrays (different parameters) of 
	arrays (different steps) of arrays (different particles).
	'''
	all_coords = pickle.load(f)

count_particles(all_coords[0][0])

#all_params_msds = [ [ [0] * N_TYPES ] for _ in range(N_PARAMS) ] 

with mp.Pool(NUM_CPU) as p:
	all_params_msds = p.map(run_msd_one_param, all_coords)

#for i in range(N_PARAMS):
#	start_coords = all_coords[i][0]
#	for j in range(N_STEPS):
#		count_msd(start_coords, all_coords[i][j], all_params_msds[i])

with open('msds.pickle', 'wb') as f:
	pickle.dump(all_params_msds, f)


