import tkinter
import math
import time
from World import World
from Walker import Walker

class Visualization:

	def __init__(self):
		# world variables
		self.world_height = 200
		self.world_width = 400
		self.counter = 0
		self.iteration_counter = 0
		# GUI
		self.window = tkinter.Tk()
		self.canvas = tkinter.Canvas(
			self.window,
			bg='white',
			height=self.world_height,
			width=self.world_width)
		# render
		self.world = World()
		self.reset()
		self.loop()


	def give_big_reward(self, amount):
		self.world.walker.give_reward(amount)


	def update_walker_before(self):
		self.world.walker.perform_action()


	def update_walker_after(self):
		self.world.walker.update_reward()


	def update_physics(self):
		self.world.apply_gravity()
		self.world.apply_rotation()


	def loop(self):
		while True:
			# if walker passes the checkpoint
			#if self.world.walker.torso_coordinates[0] > self.world_width - 50:
			#	self.give_big_reward(1000.0/self.counter)
			#	self.reset()
			# if walker falls down
			if self.world.walker.torso_coordinates[1] < 20:
				print('Fail')
				self.give_big_reward(-1000)
				self.reset()
			if self.counter == 100:
				reward = self.world.walker.torso_coordinates[0] - 100
				print('Finished Iterations: ' + str(reward))
				self.give_big_reward(reward)
				self.reset()
			#print('Iteration: ' + str(self.counter))
			self.counter += 1
			self.update_walker_before()
			self.update_physics()
			self.update_walker_after()
			self.render()
			self.window.update_idletasks()
			self.window.update()
			if self.iteration_counter > 1000:
				time.sleep(0.1)


	def reset(self):
		self.counter = 0
		self.iteration_counter += 1
		self.world.reset()


	def render(self):
		self.canvas.delete(tkinter.ALL)
		self.draw_walker()
		self.canvas.pack()


	def draw_walker(self):
		torso = self.world.walker.get_torso_info()
		legs = self.world.walker.get_limb_info()
		self.canvas.create_line(
			torso[0][0], self.world_height - torso[0][1],
			torso[1][0], self.world_height - torso[1][1],
			fill='green',
			width=4)
		for i in range(4):
			l = legs[i]
			self.canvas.create_line(
				l[0][0], self.world_height - l[0][1],
				l[1][0], self.world_height - l[1][1],
				fill=('blue' if i < 2 else 'red'),
				width=2)


