import matplotlib.pyplot as plt
import pickle
import sys

N_TYPES = 4
N_PARAMS = int(sys.argv[1])
STEP_STEPS = int(sys.argv[2])	# how often we dump coordinates to dump.micelle 
N_STEPS = 1000

steps = []
curr_step = 0
for i in range(int(N_STEPS / STEP_STEPS)):
	steps.append(curr_step)
	curr_step += STEP_STEPS

with open('msds.pickle', 'rb') as f:
	all_msds = pickle.load(f)

fig, ax = plt.subplots()
curr_type = 1
for i in range(N_TYPES):
	ax.plot(steps, all_msds[2][i], label="Type " + str(curr_type))
	curr_type += 1

ax.legend()
plt.savefig("msds_plt.png")
