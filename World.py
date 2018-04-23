from Walker import Walker

class World:

	"""
	
	The world manages physics (gravity, friction)

	"""

	def __init__(self):
		self.walker = Walker()


	def reset(self):
		self.walker.reset()


	def apply_gravity(self):
		# applies gravity instantaneously,
		# that is to say, the walker drops till
		# one of his arms/legs touches the ground
		min_y = 1000
		# get minimum y
		for pt in self.walker.get_limb_info():
			min_y = min(min_y, pt[0][1])
			min_y = min(min_y, pt[1][1])
		min_y = min(min_y, self.walker.get_torso_info()[0][1])
		min_y = min(min_y, self.walker.get_torso_info()[1][1])
		# lower body
		self.walker.torso_coordinates[1] -= min_y


	def apply_rotation(self):
		# TODO fix this up
		# rotate forward or backwards
		pass


	def get_walker(self):
		return self.walker

