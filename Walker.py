import math

class Walker:

	"""
	
	Walker consists of 5 body parts
	- Rectangular torso
	- 2 Upper limbs
	- 2 Lower limbs
	
	Walker is controlled by 4 angles
	- Angle between torso and upper limb moves between -90 and 90 degrees
	- Angle between Upper and Lower limb moves between 0 and -135 degrees

	This attempts the mimick the motion of a human being

	At each time frame, the walker has 9 options:
	- Increase/Decrease each of the 4 angles
	- Do nothing (let physics do its work)

	"""

	def __init__(self):
		self.reset()

	def reset(self):
		self.torso_angle = 0
		self.torso_coordinates = (50, 140)
		# torso rotation of 0 is upright
		# + is leaning forward, - is leaning backwards
		# in other words, angle is angle from the normal
		self.torso_rotation = 0
		self.torso_height = 50
		self.upper_limb_len = 40
		self.lower_limb_len = 40
		# angles are + for forward relative to torso
		# and - for backwards
		# note that lower angles are nonpositive,
		# due to the nature of the knee
		self.left = { 'upper': 10, 'lower': -20 }
		self.right = { 'upper': 5, 'lower': -10 }

	def get_torso_info(self):
		"""
		Returns the centre, width, height, rotation
		"""
		return [self.get_torso_top(), self.get_torso_bottom()]


	def get_torso_top(self):
		torso_top = [self.torso_coordinates[0],
					 self.torso_coordinates[1]]
		torso_top[0] += math.sin(math.radians(self.torso_rotation)) * (self.torso_height / 2.0)
		torso_top[1] += math.cos(math.radians(self.torso_rotation)) * (self.torso_height / 2.0)
		return torso_top

	
	def get_torso_bottom(self):
		torso_bottom = [self.torso_coordinates[0],
						self.torso_coordinates[1]]
		torso_bottom[0] -= math.sin(math.radians(self.torso_rotation)) * (self.torso_height / 2.0)
		torso_bottom[1] -= math.cos(math.radians(self.torso_rotation)) * (self.torso_height / 2.0)
		return torso_bottom
	

	def get_lower_point(self, upper_point, len, rotation):
		return [
			upper_point[0] - math.sin(math.radians(rotation)) * len,
			upper_point[1] - math.cos(math.radians(rotation)) * len
		]	


	def get_limb_info(self):
		"""
		For each section of the limbs, returns a pair 
		of coordinates representing a line segment
		"""
		ret = []
		
		torso_lower = self.get_torso_bottom()
		angle_left_upper = self.torso_rotation - self.left['upper']
		angle_right_upper = self.torso_rotation - self.right['upper']
		
		left_knee = self.get_lower_point(
			torso_lower, self.upper_limb_len, angle_left_upper)
		right_knee = self.get_lower_point(
			torso_lower, self.upper_limb_len, angle_right_upper)
		
		ret.append([torso_lower, left_knee])

		ret.append([left_knee, self.get_lower_point(
			left_knee, self.lower_limb_len,
			angle_left_upper - self.left['lower'])])
		
		ret.append([torso_lower, right_knee])
		
		ret.append([right_knee, self.get_lower_point(
			right_knee, self.lower_limb_len,
			angle_right_upper - self.right['lower'])])

		return ret




