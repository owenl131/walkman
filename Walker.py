import math
import random

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
		self.torso_coordinates = [100, 140]
		# torso rotation of 0 is upright
		# + is leaning forward, - is leaning backwards
		# in other words, angle is angle from the normal
		self.torso_rotation = 0
		self.torso_height = 50
		self.upper_limb_len = 40
		self.lower_limb_len = 40
		# used for computing Centre of Gravity
		self.torso_mass = 100
		self.upper_limb_mass = 50
		self.lower_limb_mass = 30
		# angles are + for forward relative to torso
		# and - for backwards
		# note that lower angles are nonpositive,
		# due to the nature of the knee
		self.delta_angle = 5
		self.joints = {
			'left': {
				'upper': 10,
				'lower': -20
			},
			'right': {
				'upper': 20,
				'lower': -10
			}
		}
		# policies
		self.previous_state = None
		self.previous_action = None
		self.actions = [
			lambda: self.knee_open('left'),
			lambda: self.knee_open('right'),
			lambda: self.knee_close('left'),
			lambda: self.knee_close('right'),
			lambda: self.hip_forward('left'),
			lambda: self.hip_forward('right'),
			lambda: self.hip_back('left'),
			lambda: self.hip_back('right'),
			self.do_nothing
		]
		#self.actions = [
		#	lambda: self.knee_close('right')
		#]
		self.alpha = 0.3  # 0 < alpha < 1
		self.reward = {}
		self.visited = {}


	# TODO fix these 4 functions up

	def knee_close(self, side):
		if self.joints[side]['lower'] - self.delta_angle < -135:
			return
		anchor_foot = self.get_anchor_foot()
		if anchor_foot == 'both' or side == anchor_foot:
			# fix leg and move body
			torso_lower = self.get_torso_bottom()
			knee = self.get_lower_point(torso_lower,
				self.upper_limb_len,
				self.torso_rotation - self.joints[side]['upper'])
			# fix knee
			torso_vector = (self.torso_coordinates[0] - knee[0],
							self.torso_coordinates[1] - knee[1])
			rotate_by_angle = self.delta_angle
			rotated = self.rotate_point_about_origin(torso_vector, math.radians(rotate_by_angle))
			self.torso_coordinates = [rotated[0] + knee[0], rotated[1] + knee[1]]
			self.torso_rotation -= rotate_by_angle
		
		self.joints[side]['lower'] = max(
			self.joints[side]['lower'] - self.delta_angle,
			-135)
		self.fix_sinking()


	def knee_open(self, side):
		if self.joints[side]['lower'] + self.delta_angle > 0:
			return
		anchor_foot = self.get_anchor_foot()
		if anchor_foot == 'both' or side == anchor_foot:
			# fix leg and move body
			torso_lower = self.get_torso_bottom()
			knee = self.get_lower_point(torso_lower,
				self.upper_limb_len,
				self.torso_rotation - self.joints[side]['upper'])
			# fix knee
			torso_vector = (self.torso_coordinates[0] - knee[0],
							self.torso_coordinates[1] - knee[1])
			rotate_by_angle = -self.delta_angle
			rotated = self.rotate_point_about_origin(torso_vector, math.radians(rotate_by_angle))
			self.torso_coordinates = [rotated[0] + knee[0], rotated[1] + knee[1]]
			self.torso_rotation -= rotate_by_angle
		
		self.joints[side]['lower'] = min(
			self.joints[side]['lower'] + self.delta_angle,
			0)
		self.fix_sinking()


	def hip_forward(self, side):
		if self.joints[side]['upper'] + self.delta_angle > 90:
			return
		anchor_foot = self.get_anchor_foot()
		if anchor_foot == 'both' or side == anchor_foot:
			torso_lower = self.get_torso_bottom()
			# fix hip
			torso_vector = (self.torso_coordinates[0] - torso_lower[0],
							self.torso_coordinates[1] - torso_lower[1])
			rotate_by_angle = -self.delta_angle
			rotated = self.rotate_point_about_origin(torso_vector, math.radians(rotate_by_angle))
			self.torso_coordinates = [rotated[0] + torso_lower[0], rotated[1] + torso_lower[1]]
			self.torso_rotation -= rotate_by_angle
		
		self.joints[side]['upper'] = min(
			self.joints[side]['upper'] + self.delta_angle,
			90)
		self.fix_sinking()


	def hip_back(self, side):
		anchor_foot = self.get_anchor_foot()
		if self.joints[side]['upper'] - self.delta_angle < -90:
			return
		if anchor_foot == 'both' or side == anchor_foot:
			torso_lower = self.get_torso_bottom()
			# fix torso
			torso_vector = (self.torso_coordinates[0] - torso_lower[0],
							self.torso_coordinates[1] - torso_lower[1])
			rotate_by_angle = self.delta_angle
			rotated = self.rotate_point_about_origin(torso_vector, math.radians(rotate_by_angle))
			self.torso_coordinates = [rotated[0] + torso_lower[0], rotated[1] + torso_lower[1]]
			self.torso_rotation -= rotate_by_angle
		
		self.joints[side]['upper'] = max(
			self.joints[side]['upper'] - self.delta_angle,
			-90)
		self.fix_sinking()


	def fix_sinking(self):
		# after movement, if other leg comes down and touches the ground,
		# ensure that that leg does not sink below the ground
		# raise the whole body if necessary
		foot_points = self.get_foot_points()
		self.torso_coordinates = [self.torso_coordinates[0],
			self.torso_coordinates[1] - min(foot_points[0][1], foot_points[1][1])]


	def do_nothing(self):
		pass


	def rotate_point_about_origin(self, vector, radians):
		# rotates point clockwise about origin
		return (
			math.cos(radians)*vector[0] - math.sin(radians)*vector[1],
			math.sin(radians)*vector[0] + math.cos(radians)*vector[1]
			)	


	# TODO check that the rewards propogate

	def update_reward(self):
		pstate = self.previous_state
		paction = self.previous_action
		state = self.get_state()
		if pstate is None:
			self.previous_state = state
			return
		if state not in self.reward:
			self.reward[state] = [0] * len(self.actions)
			self.visited[state] = 0
		if pstate not in self.reward:
			self.reward[pstate] = [0] * len(self.actions)
			self.visited[pstate] = 0
		self.reward[pstate][paction] = \
			(1 - self.alpha) * self.reward[pstate][paction] + \
			self.alpha * max(self.reward[state])
		self.visited[pstate] += 1
		self.previous_state = state


	def give_reward(self, amount):
		pstate = self.previous_state
		paction = self.previous_action
		if pstate not in self.reward:
			self.reward[pstate] = [0] * len(self.actions)
		self.reward[pstate][paction] = \
			(1 - self.alpha) * self.reward[pstate][paction] + \
			self.alpha * amount


	def perform_action(self):
		state = self.get_state()
		if state not in self.reward:
			# choose random
			action = random.randrange(0, len(self.actions))
			self.previous_action = action
			self.actions[action]()
		elif self.visited[state] > 1000 and \
			max(self.reward[state]) / sum(self.reward[state]) > 0.9:
			# use maximum
			action = 0
			max_r = self.reward[state][0]
			for i in range(len(self.actions)):
				if self.reward[state][i] > max_r:
					max_r = self.reward[state][i]
					action = i
			self.previous_action = action
			self.actions[action]()
		else:
			# choose random
			action = random.randrange(0, len(self.actions))
			self.previous_action = action
			self.actions[action]()


	def get_state(self):
		return (self.torso_rotation,
				self.joints['left']['upper'],
				self.joints['left']['lower'],
				self.joints['right']['upper'],
				self.joints['right']['lower'])


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
		angle_left_upper = self.torso_rotation - self.joints['left']['upper']
		angle_right_upper = self.torso_rotation - self.joints['right']['upper']
		
		left_knee = self.get_lower_point(
			torso_lower, self.upper_limb_len, angle_left_upper)
		right_knee = self.get_lower_point(
			torso_lower, self.upper_limb_len, angle_right_upper)
		
		ret.append([torso_lower, left_knee])
		ret.append([left_knee, self.get_lower_point(
			left_knee, self.lower_limb_len,
			angle_left_upper - self.joints['left']['lower'])])
		
		ret.append([torso_lower, right_knee])
		ret.append([right_knee, self.get_lower_point(
			right_knee, self.lower_limb_len,
			angle_right_upper - self.joints['right']['lower'])])
		# this function returns redundant information
		# since the knee point is duplicated
		return ret


	def get_foot_points(self):
		limbs = self.get_limb_info()
		impt_limbs = [limbs[1], limbs[3]]
		# assumes details about implementation of get_limb_info
		# assumes that the first coordinate given is the knee
		# and the second coordinate given is the foot
		return (impt_limbs[0][1], impt_limbs[1][1])


	def get_anchor_foot(self):
		foot_points = self.get_foot_points()
		# establish base
		if foot_points[0][1] < 1 and foot_points[1][1] < 1:
			return 'both'
		elif foot_points[0][1] < 1:
			return 'left'
		elif foot_points[1][1] < 1:
			return 'right'
		else:
			assert(False)


	def get_cg(self):
		points = []
		points.append((self.torso_coordinates[0],
			self.torso_coordinates[1], self.torso_mass))
		limbs = self.get_limb_info()
		# left lower
		masses = [self.lower_limb_mass, self.upper_limb_mass,
				  self.lower_limb_mass, self.upper_limb_mass]
		for i in range(4):
			points.append((
				(limbs[i][0][0]+limbs[i][1][0])/2,
				(limbs[i][0][1]+limbs[i][1][1])/2,
				masses[i]))
		total_mass = 0
		x, y = 0, 0
		for pt in points:
			total_mass += pt[2]
			x += pt[0] * pt[2]
			y += pt[1] * pt[2]
		x /= total_mass
		y /= total_mass
		return x, y
