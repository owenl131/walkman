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
		# get all control points

		# get minimum y

		# lower body


	def apply_rotation(self):
		pass


	def get_walker(self):
		return self.walker

