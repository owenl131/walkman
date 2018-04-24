from Walker import Walker
import math

class World:

	"""
	
	The world manages physics (gravity, friction)

	"""

	def __init__(self):
		self.walker = Walker()
		self.apply_gravity()


	def reset(self):
		self.walker.reset()
		self.apply_gravity()


	def apply_gravity(self):
		# applies gravity instantaneously,
		# that is to say, the walker drops till
		# one of his arms/legs touches the ground
		foot_points = self.walker.get_foot_points()
		# lower body
		self.walker.torso_coordinates[1] -= min(foot_points[0][1], foot_points[1][1])


	def apply_rotation(self):
		# TODO fix this up
		# rotate forward or backwards
		foot_points = self.walker.get_foot_points()
		base_left_bound = None
		base_right_bound = None
		legs_down = None
		# establish base
		if foot_points[0][1] < 1 and foot_points[1][1] < 1:
			base_left_bound = min(foot_points[0][0], foot_points[1][0])
			base_right_bound = max(foot_points[0][0], foot_points[1][0])
			legs_down = 'both'
		elif foot_points[0][1] < 1:
			base_left_bound = foot_points[0][0]
			base_right_bound = foot_points[0][0]
			legs_down = 'left'
		elif foot_points[1][1] < 1:
			base_left_bound = foot_points[1][0]
			base_right_bound = foot_points[1][0]
			legs_down = 'right'
		else:
			assert(False)
		# compute CG
		centre_of_gravity = self.walker.get_cg()
		# fix point of contact, rotate body
		# find new coordinate of body
		if centre_of_gravity[0] <= base_right_bound and \
			centre_of_gravity[0] >= base_left_bound:
			# no moment due to gravity
			#print('Stable')
			return
		elif centre_of_gravity[0] > base_right_bound:
			# rotate to the right
			#print('Rotate to right')
			self.rotate_walker((base_right_bound, 0), 1)
		elif centre_of_gravity[0] < base_left_bound:
			# rotate to the left
			#print('Rotate to left')
			self.rotate_walker((base_left_bound, 0), -1)
		else:
			assert(False) 


	def rotate_walker(self, about_pt, angle):
		body_vector = (
			self.walker.torso_coordinates[0] - about_pt[0],
			self.walker.torso_coordinates[1] - about_pt[1])
		rads = -math.radians(angle)
		rotated = (
			math.cos(rads)*body_vector[0] - math.sin(rads)*body_vector[1],
			math.sin(rads)*body_vector[0] + math.cos(rads)*body_vector[1])
		#print(body_vector, rotated)
		self.walker.torso_rotation += angle
		self.walker.torso_coordinates = [
			rotated[0] + about_pt[0],
			rotated[1] + about_pt[1]
			]


	def get_walker(self):
		return self.walker

