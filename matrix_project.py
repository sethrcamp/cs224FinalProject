import unittest

class Node(object):

	def __init__(self, up, down, left, right, x, y, value=None):

		self.up = up
		self.down = down
		self.left = left
		self.right = right

		if up is None:
			self.up = self
		if down is None:
			self.down = self
		if left is None:
			self.left = self
		if right is None:
			self.right = self

		self.x = x
		self.y = y
		self.value = value

class Header(Node):

	def __init__(self, up, down, left, right, primary):
		super(Header, self).__init__(up, down, left, right, None, None)

		self.is_primary = primary

	def tally_ones(self):
		current_node = self
		self.value = 0
		while type(current_node.down) is not Header:
			current_node = current_node.down
			self.value += current_node.value

class Matrix:

	def __init__(self):
		self.removed_nodes = []
		self.first_header = None
		self.total_rows = 0

	def add_row(self, values):
		if self.first_header is None:
			self.first_header = Header(self, self, self, self, False)
			current_header = self.first_header






"""
EVERYTHING BELOW IS FOR REFERENCE
DELETE WHEN DONE
"""

class UnitTest(unittest.TestCase):

	def test_node_creation(self):
		node = Node(None, None, None, None, None, None, 5)
		self.assertEqual(node.value, 5)

	def test_circular_node_creation(self):
		node = Node(None, None, None, None, None, None, 10)
		self.assertEqual(node.up, node)



def main():
	unittest.main()


if __name__ == '__main__':
	main()


