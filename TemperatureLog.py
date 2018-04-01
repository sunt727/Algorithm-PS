################################################
# Scroll down! You should not modify this code #
################################################

class BST:
	def __init__(self, key = None, parent = None):
		'''Initialize a BST node'''
		self.key = key
		self.parent = parent
		self.left = None
		self.right = None

	def minimum(self):
		'''Return a node with minimum key of self's sub-tree, else None'''
		if self.key is not None:
			if self.left:
				return self.left.minimum()
			return self
		return None

	def find(self, key):
		'''Return a highest node having key in self's sub-tree, else None'''
		if self.key is not None:
			if key == self.key:
				return self
			if key < self.key and self.left:
				return self.left.find(key)
			if key > self.key and self.right:
				return self.right.find(key)
		return None

	def successor(self):
		'''Return a node in tree with next larger key, else None'''
		if self.key is not None:
			if self.right:
				return self.right.minimum()
			node = self                         # (might be None)
			while (node.parent and
				   node.parent.right is node):
				node = node.parent
			return node.parent
		return None

	def insert(self, key):
		'''Insert key into self's sub-tree'''
		if self.key is None:
			self.key = key
			self.maintain()
		elif key < self.key:
			if self.left is None:
				self.left = self.__class__(None, self)
			self.left.insert(key)
		else:
			if self.right is None:
				self.right = self.__class__(None, self)
			self.right.insert(key)

	def replace(self, node):
		'''Replace self's attributes with node's attributes'''
		self.key = node.key
		self.left = node.left
		self.right = node.right
		if self.left:
			self.left.parent = self
		if self.right:
			self.right.parent = self

	def delete(self):
		'''Remove self's key from sub-tree'''
		if self.left and self.right:
			node = self.right.minimum()
			self.key = node.key
			node.delete()
			return
		if self.right:
			self.replace(self.right)
		elif self.left:
			self.replace(self.left)
		else:
			if self.parent is None:
				self.key = None
			elif self.parent.right is self:
				self.parent.right = None
			elif self.parent.left is self:
				self.parent.left = None
		self.maintain()

	def maintain(self):
		'''
		Perform maintenance after a dynamic operation
		Called by lowest node with sub-tree modified by insert or delete
		'''
		pass

	def iterative_traversal(self):
		A = []
		node = self.minimum()
		while node:
			A.append(node.key)
			node = node.successor()
		return A

	def recursive_traversal(self, A = None):
		if A is None:
			A = []
		if self.left:
			self.left.recursive_traversal(A)
		A.append(self.key)
		if self.right:
			self.right.recursive_traversal(A)
		return A

	def __str__(self):
		'''Return ASCII drawing of the tree'''
		s = str(self.key)
		if self.left is None and self.right is None:
			return s
		sl, sr = [''], ['']
		if self.left:
			s = '_' + s
			sl = str(self.left).split('\n')
		if self.right:
			s = s + '_'
			sr = str(self.right).split('\n')
		wl, cl = len(sl[0]), len(sl[0].lstrip(' _'))
		wr, cr = len(sr[0]), len(sr[0].rstrip(' _'))
		a = [(' ' * (wl - cl)) + ('_' * cl) + s +
			 ('_' * cr) + (' ' * (wr - cr))]
		for i in range(max(len(sl), len(sr))):
			ls = sl[i] if i < len(sl) else ' ' * wl
			rs = sr[i] if i < len(sr) else ' ' * wr
			a.append(ls + ' ' * len(s) + rs)
		return '\n'.join(a)

class AVL(BST):
	def __init__(self, key = None, parent = None):
		'''Augment BST with height and skew'''
		super().__init__(key, parent)
		self.height = 0
		self.skew = 0

	def update(self):
		'''Update height and skew'''
		left_height  = self.left.height  if self.left  else -1
		right_height = self.right.height if self.right else -1
		self.height = max(left_height, right_height) + 1
		self.skew = right_height - left_height

	def right_rotate(self):
		'''
		Rotate left to right, assuming left is not None
		 __s__      __n__
		_n_  c  =>  a  _s_
		a b            b c
		'''
		node, c = self.left, self.right
		a, b = self.left.left, self.left.right
		self.key, node.key = node.key, self.key
		if a:
			a.parent = self
		if c:
			c.parent = node
		self.left, self.right = a, node
		node.left, node.right = b, c
		node.update()
		self.update()

	def left_rotate(self):
		'''
		Rotate right to left, assuming right is not None
		__s__        __n__
		a  _n_  =>  _s_  c
		   b c      a b
		'''
		node, a = self.right, self.left
		b, c = self.right.left, self.right.right
		self.key, node.key = node.key, self.key
		if a:
			a.parent = node
		if c:
			c.parent = self
		self.left, self.right = node, c
		node.left, node.right = a, b
		node.update()
		self.update()

	def maintain(self):
		'''Update height and skew and rebalance up the tree'''
		self.update()
		if self.skew == 2:      # must have right child
			if self.right.skew == -1:
				self.right.right_rotate()
			self.left_rotate()
		elif self.skew == -2:   # must have left child
			if self.left.skew == 1:
				self.left.left_rotate()
			self.right_rotate()
		if self.parent:
			self.parent.maintain()

	def __str__(self):
		'''Return ASCII drawing of the tree (visualize skew)'''
		key = self.key
		self.key = str(key) + (
			'=' if self.skew == 0 else
			'>' if self.skew < 0 else
			'<')
		s = super().__str__()
		self.key = key
		return s

####################
# Your code below! #
####################

class TemperatureLog(AVL):
	def __init__(self, key = None, parent = None):
		'''Augment AVL with additional attributes'''
		super().__init__(key, parent)
		#####################################################
		# TODO: Add any additional sub-tree properties here #
		#####################################################
		self.sum_yi, self.count_yi = 0,0
		self.right_max = self.key
		self.left_min = self.key

	def maximum(self):
		'''Return a node with maximum key of self's sub-tree, else None'''
		if self.key is not None:
			if self.right:
				return self.right.maximum()
			return self
		return None


	def get_subtree(self):
		'''get the extra information of this subtree'''
		# sum, count = 0, 0
		# if self.key is not None:
		# 	sum += self.key[1]
		# 	count += 1

		self.left_min = self.key
		self.right_max = self.key

		if self.left:
			# Lsum, Lcount, LLmin, LRmax = self.left.get_subtree()
			self.left.get_subtree()
			# sum += self.left.sum_yi
			# count += self.left.count_yi
			self.left_min = self.left.left_min
		if self.right:
			# Rsum, Rcount, RLmin, RRmax = self.right.get_subtree()
			self.right.get_subtree()
			# sum += self.right.sum_yi
			# count += self.right.count_yi
			self.right_max = self.right.right_max


		# self.sum_yi = sum
		# self.count_yi = count

		# print(self.left_min)
		# print(self.right_max)
		# print(self.sum_yi)
		# print(self.count_yi)


		# return self.sum_yi, self.count_yi, self.left_min, self.right_max

	def pre_com(self):
		# update left min and right max (this subtree's range)
		if self.right:
			self.right_max = self.right.maximum().key
		else:
			self.right_max = self.key
		if self.left:
			self.left_min = self.left.minimum().key
		else:
			self.left_min = self.key

		# store the sum yi and count of subtree
		# self.sum_yi, self.count_yi = self.get_subtree()
		#
		# if self.left:
		# 	self.left.pre_com()
		# if self.right:
		# 	self.right.pre_com()


	def update(self):
		'''Augment AVL update() to fix any properties calculated from children'''
		super().update()




	def add_sample(self, x, y):
		'''Add a transaction to the transaction log'''

		super().insert((x, y))  # insert will call maintenance and then update

	def predict(self, x, w):
		'''
		Return a temperature estimate given:
			x: yesterday's temperature
			w: confidence interval
		If there are no samples within the confidence interval, return 0.
		'''
		self.get_subtree()

		result = self.predict_helper(x, w)
		total, count = result
		if result is None:
			return None
		return 0 if count is 0 else total/count

	def predict_helper(self, x, w):
		'''return sum of yi and count separately to help calculating the average'''
		total, count = 0, 0
		# empty tree
		if self.key is None:
			return None
		# range[x-w, x+w]
		# if range not in this subtree
		if x+w < self.left_min[0] or x-w > self.right_max[0]:
			return 0, 0
		# if this subtree is entirely in the range
		# elif x-w <= self.left_min[0] and self.right_max[0] <= x+w:
		# 	total += self.sum_yi
		# 	count += self.count_yi
		# if not the entire subtree in the range
		else:
			# cum the root in the range
			if x-w <= self.key[0] <= x+w:
				count += 1
				total += self.key[1]
			# go through left subtrees if the maximum one is in the range
			if self.left: # and x-w <= self.left_min[0]: # and x-w <= self.left.maximum().key[0]:
				t, c = self.left.predict_helper(x, w)
				total += t
				count += c
			# go through right subtrees if the minimum one is in the range
			if self.right: # and self.right_max[0] <= x+w: # and x+w >= self.right.minimum().key[0]:
				t, c = self.right.predict_helper(x, w)
				total += t
				count += c

		return total, count

# Returns the gradient of hinge(v) with respect to v.
def d_hinge(v):
	print(np.where(v >= 1, 0, 1-v))
	return np.where(v >= 1, 0, 1-v)

# Returns the gradient of hinge_loss(x, y, th, th_0) with respect to th
def d_hinge_loss_th(x, y, th, th0):
	return np.where(y*(np.dot(th.T, x)+th0) < 1, -y*x, 0)

# Returns the gradient of hinge_loss(x, y, th, th_0) with respect to th0
def d_hinge_loss_th0(x, y, th, th0):
	return np.where(y*(np.dot(th.T, x)+th0) < 1, -y, 0)

# Returns the gradient of svm_obj(x, y, th, th_0) with respect to th
def d_svm_obj_th(x, y, th, th0, lam):
	return np.mean(d_hinge_loss_th(x, y, th, th0), axis=1, keepdims=True)+ 2*lam

# Returns the gradient of svm_obj(x, y, th, th_0) with respect to th0
def d_svm_obj_th0(x, y, th, th0, lam):
	return np.mean(d_hinge_loss_th0(x, y, th, th0), axis=1, keepdims=True)

# Returns the full gradient as a single vector
def svm_obj_grad(X, y, th, th0, lam):
	return np.vstack((d_svm_obj_th(X, y, th, th0, lam), d_svm_obj_th0(X, y, th, th0, lam))
