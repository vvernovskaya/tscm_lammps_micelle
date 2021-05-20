from ovito.io import import_file
import logging
import ovito.modifiers as md
import math
import ovito.vis as vis
import numpy as np
import sys


N_FRAMES = int(sys.argv[1])
STEP_STEPS = 50
BEGIN_FRAME = 0
CELL_SIZE = 30


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
	center = tuple([CELL_SIZE/2, CELL_SIZE/2, 0])
	position =  tuple([CELL_SIZE/2 + 3, CELL_SIZE/2 + 3, WALL])
	center_pos = tuple([0, 0, (-1)*WALL])
	return position, center_pos


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

#vp.render_image(size=(400,300), filename="micelle_vis.png", renderer=vis.TachyonRenderer())

vp.render_anim(size=(800,400), filename="micelle.mp4", \
	renderer=vis.TachyonRenderer(), range=(BEGIN_FRAME, BEGIN_FRAME + int(N_FRAMES/STEP_STEPS)))
