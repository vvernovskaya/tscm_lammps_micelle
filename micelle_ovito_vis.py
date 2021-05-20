from ovito.io import import_file
import logging
import ovito.modifiers as md
import math
import ovito.vis as vis
import numpy as np
import sys


N_STEPS = int(sys.argv[1])
STEP_STEPS = 50
BEGIN_FRAME = 0
CELL_SIZE = 30
N_FRAMES = int(N_STEPS/STEP_STEPS)


def  modify_color_radius(frame, data):
	color_property = data.particles_.create_property("Color")
	radius_property = data.particles_.create_property("Radius")
	transparency_property = data.particles_.create_property("Transparency")
	type_property = data.particles['Particle Type']
	ke_property = data.particles['c_keatom']
	
	for i in range(len(color_property)):
		if type_property.array[i] == 1:		# solvent
			radius_property.marray[i] = 0.5
			color_property.marray[i] = ((ke_property.array[i]/2)**(1/8) * 205/255,\
							(ke_property.array[i]/2)**(1/8),\
							(ke_property.array[i]/2)**(1/8))
		elif type_property.array[i] == 2: 	# head
			radius_property.marray[i] = 0.7
			color_property.marray[i] = ((ke_property.array[i]/2)**(1/8) * 195/255,\
							(ke_property.array[i]/2)**(1/8) * 40/255,\
							(ke_property.array[i]/2)**(1/8) * 195/255)
		elif type_property.array[i] == 3 or type_property.array[i] == 4: 	#tail
			if type_property.array[i] == 3:
				radius_property.marray[i] = 0.5
			elif type_property.array[i] == 4:
				radius_property.marray[i] = 0.5
			color_property.marray[i] = (((ke_property.array[i]/2)**(1/8)) * 170/255,\
							((ke_property.array[i]/2)**(1/8)) * 145/255,\
							((ke_property.array[i]/2)**(1/8)) * 255/255)	



def get_pos_dir(frame):
	center = np.array([CELL_SIZE/2 + 3, CELL_SIZE/2 + 3, 0])
	
	if frame >= N_FRAMES*2/7 and frame < N_FRAMES/3:
		center = np.array([CELL_SIZE/2 + 3 - 5*(frame - 2/7*N_FRAMES)/N_FRAMES*21,\
				 CELL_SIZE/2 + 3 - 5*(frame - 2/7*N_FRAMES)/N_FRAMES*21, 0])
	elif frame < N_FRAMES*2/7:
		center = np.array([CELL_SIZE/2 + 3, CELL_SIZE/2 + 3, 0])
	elif frame >= N_FRAMES/3:
		center = np.array([CELL_SIZE/2 - 2, CELL_SIZE/2 - 2, 0])  
	if frame >= N_FRAMES/3 and frame <= 2/3 * N_FRAMES:
		height = [0, 0, WALL*(1 - 2*(frame - N_FRAMES/3)/N_FRAMES)]
	elif frame < N_FRAMES/3:
		height = [0, 0, WALL]
	elif frame > 2/3 * N_FRAMES:
		height = [0, 0, WALL*1/3]
	position = center + height
	
	return tuple(position), tuple(center-position)


def render_view(args):
	frame = args.frame
	logging.info("frame: {:d}".format(args.frame))
	pos, direction = get_pos_dir(frame)
	args.viewport.camera_pos = pos
	args.viewport.camera_dir = direction
	args.viewport.fov = math.radians(60.0)


pipeline = import_file('micelle.nve.lammpstrj')
pipeline.add_to_scene()

logging.basicConfig(filename="log.txt", level=logging.INFO)

pipeline.modifiers.append(md.PythonScriptModifier(function=modify_color_radius))
data = pipeline.compute()

WALL = data.cell[0][0]

vp = vis.Viewport()
vp.type = vis.Viewport.Type.Perspective

pos, direction = get_pos_dir(BEGIN_FRAME)

vp.camera_pos = pos
vp.camera_dir = direction
vp.fov = math.radians(60.0)
vp.overlays.append(vis.PythonViewportOverlay(function = render_view))

vp.render_image(size=(400,300), filename="micelle_vis.png", renderer=vis.TachyonRenderer())

vp.render_anim(size=(400,300), filename="micelle.mp4", \
	renderer=vis.TachyonRenderer(), range=(BEGIN_FRAME, BEGIN_FRAME + int(N_STEPS/STEP_STEPS)))
