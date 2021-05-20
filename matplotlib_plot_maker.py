import matplotlib.pyplot as plt
import pickle
import sys

N_TYPES = 4
N_STEPS = int(sys.argv[1])
N_PARAMS = int(sys.argv[2])
STEP_STEPS = 50	# how often we dump coordinates to dump.micelle 

steps = []
curr_step = 0
for i in range(int(N_STEPS / STEP_STEPS)):
	steps.append(curr_step)
	curr_step += STEP_STEPS

with open('msds.pickle', 'rb') as f:
	all_msds = pickle.load(f)

fig, ax = plt.subplots()
curr_type = 1
types = ['(solvent)', '(head)', '(tail)', '(tail)']
for i in range(N_TYPES):
	ax.plot(steps, all_msds[2][i], label="Type " + str(curr_type) + " " + types[i])
	curr_type += 1

ax.legend()
plt.xlabel('Steps')
plt.ylabel('MSD')
plt.title('MSDs for different particle types, T = 0.6')
plt.savefig("msds_plt.png")
