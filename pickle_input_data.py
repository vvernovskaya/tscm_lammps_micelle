import pickle
import copy
import multiprocessing as mp
import sys

'''
This code separates dump.melt file into array of coords of
particles on all steps sorted by particle id and dumped into a pickle file.

Boundary conditions are also taken into account here.
'''

CELL_SIZE = 30		# CHECK THIS !!!!!!!!!!!!!!!!!
BOUND_LAYER = CELL_SIZE * 0.1
N_STEPS = 1000
N_PARAMS = int(sys.argv[1])		# how many times we've modified the parameter
PARAM_STEP = 0.15
#INPUT_TEMPLATE = "temp_" 	# same part of input filenames
INITIAL_PARAM = 0
INPUT_FILENAME = "dump.micelle"

NUM_CPU = 4


def sort_by_first_el(it):
	return(it[0])


def check_bounds(prev_step_coords, this_step_coords):	
	for i in range(len(this_step_coords)):
		if prev_step_coords[i][2] >= 0 and prev_step_coords[i][2] <= BOUND_LAYER and this_step_coords[i][2] <= CELL_SIZE \
			and this_step_coords[i][2] >= CELL_SIZE - BOUND_LAYER:
			edge_x = -1
		elif prev_step_coords[i][2] <= CELL_SIZE and prev_step_coords[i][2] >= CELL_SIZE - BOUND_LAYER \
			and this_step_coords[i][2] >= 0 and this_step_coords[i][2] <= BOUND_LAYER:
			edge_x = 1
		else:
			edge_x = 0

		if prev_step_coords[i][3] >= 0 and prev_step_coords[i][3] <= BOUND_LAYER and this_step_coords[i][3] <= CELL_SIZE \
			and this_step_coords[i][3] >= CELL_SIZE - BOUND_LAYER:
                        edge_y = -1
		elif prev_step_coords[i][3] <= CELL_SIZE and prev_step_coords[i][3] >= CELL_SIZE - BOUND_LAYER \
			and this_step_coords[i][3] >= 0 and this_step_coords[i][3] <= BOUND_LAYER:
			edge_y = 1
		else:
			edge_y = 0

		this_step_coords[i][2] += edge_x * CELL_SIZE
		this_step_coords[i][3] += edge_y * CELL_SIZE


def dump_input_into_array(filename):
	print("-- -- -- started dumping")
	output_data = []
	read_flag = 0
	curr_step_data = []
	with open(filename) as f:
		lines = f.readlines()
	for i in range(len(lines)):
		curr_line = lines[i].split()
		
		if len(curr_line) > 1 and curr_line[1] == "ATOMS":
			read_flag = 1
			
			continue
		elif len(curr_line) > 1 and curr_line[1] == "TIMESTEP":
			
			read_flag = 0
			if len(curr_step_data) != 0:
				curr_step_data.sort(key=sort_by_first_el)
				if len(output_data) != 0:
					check_bounds(output_data[len(output_data)-1], curr_step_data)
				
				output_data.append(copy.deepcopy(curr_step_data))
				curr_step_data.clear()
				
		elif read_flag == 1:
			curr_line = list(map(float, curr_line))
			curr_step_data.append(curr_line)
	return output_data


filenames = []
curr_param = INITIAL_PARAM
#output_coords_array = [None] * N_PARAMS 	# element of this array is an array of sorted arrays of coords
input_filenames = []
for i in range(N_PARAMS):
	#print("curr_param = ", curr_param)
	#print("string from curr_param", str(curr_param))
	input_filenames.append(INPUT_FILENAME + "_" + str(curr_param))
	curr_param = (PARAM_STEP * 100 + curr_param * 100) / 100

#output_coords_array = []
#output_coords_array.append(dump_input_into_array(input_filenames[0]))

with mp.Pool(NUM_CPU) as p:
	output_coords_array = p.map(dump_input_into_array, input_filenames)
#print(len(output_coords_array[0]))
#print(output_coords_array[0][0])
#for i in range(N_PARAMS):
#	output_array[i] = []
#	dump_input_data_into_array(INPUT_FILENAME +"_" + str(curr_param), output_coords_array[i])
#	curr_param += PARAM_STEP

with open('coords.pickle', 'wb') as f:
	pickle.dump(output_coords_array, f)


