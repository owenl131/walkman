import tkinter
import math
import time
from World import World
from Walker import Walker

class Visualization:

	def __init__(self):
		# world variables
		self.world_height = 200
		self.world_width = 600
		self.counter = 0
		# GUI
		self.window = tkinter.Tk()
		self.canvas = tkinter.Canvas(
			self.window,
			bg='white',
			height=self.world_height,
			width=self.world_width)
		# render
		self.world = World()
		self.reset(self.world)
		self.loop()


	def update_walker(self):
		pass


	def update_physics(self):
		pass



	def loop(self):
		while True:
			print('Hello ' + str(self.counter))
			self.counter += 1
			self.update_walker()
			self.update_physics()
			self.render()
			#tkinter.update_idletasks()
			#tkinter.update()
			self.window.update_idletasks()
			self.window.update()
			time.sleep(0.2)


	def reset(self, world):
		world.reset()


	def render(self):
		self.canvas.delete(tkinter.ALL)
		#self.canvas.create_rectangle(
		#	0, self.world_height - 20,
		#	self.world_width, self.world_height,
		#	fill='black')
		self.draw_walker()
		self.canvas.pack()


	def draw_walker(self):
		torso = self.world.get_walker().get_torso_info()
		legs = self.world.get_walker().get_limb_info()
		self.canvas.create_line(
			torso[0][0], self.world_height - torso[0][1],
			torso[1][0], self.world_height - torso[1][1],
			fill='green',
			width=4
			)

		for i in range(4):
			l = legs[i]
			self.canvas.create_line(
				l[0][0], self.world_height - l[0][1],
				l[1][0], self.world_height - l[1][1],
				fill=('blue' if i < 2 else 'red'),
				width=2
				)


