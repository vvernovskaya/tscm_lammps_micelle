import pickle
import copy

'''
This code separates dump.melt file into array of coords of
particles on all steps sorted by particle id and dumped into a pickle file.

Boundary conditions are also taken into account here.
'''

CELL_SIZE = 20		# CHECK THIS !!!!!!!!!!!!!!!!!
BOUND_LAYER = CELL_SIZE * 0.1
N_STEPS = 300
N_PARAMS = 5		# how many times we've modified the parameter
PARAM_STEP = 0.5
INPUT_TEMPLATE = "temp_" 	# same part of input filenames
INITIAL_PARAM = 0


def sort_by_first_el(it):
	return(it[0])


def check_bounds(prev_step_array, this_step_array):
	for i in range(len(this_step_array):
		if 


def dump_input_data_into_array(filename, output_data):
	read_flag = 0
	curr_step_data = []
	with open(filename) as f:
		lines = f.readlines()
	for i in range(len(lines)):
		curr_line = lines[i].split()
		if curr_line[1] == "ATOMS":
			read_flag = 1
			continue
		else if curr_line[1] == "TIMESTEP":
			read_flag = 0
			if len(curr_step_data) != 0:
				curr_step_data.sort(key=sort_by_first_el)
				output_data.append(copy.deepcopy(curr_step_data))
				curr_step_data.clear()
		else if read_flag == 1:
			curr_step_data.append(curr_line)


filenames = []
curr_param = INITIAL_PARAM
output_coords_array = [None] * N_PARAMS 	# element of this array is an array of sorted arrays of coords

for i in range(N_PARAMS):
	output_array[i] = []
	dump_input_data_into_array(INPUT_TEMPLATE + str(curr_param), output_coords_array[i])
	curr_param += PARAM_STEP

with open('coords.pickle', 'wb') as f:
	pickle.dump(output_coords_array, f)


