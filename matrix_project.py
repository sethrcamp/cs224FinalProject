import unittest

class Node(object):

	def __init__(self, up, down, left, right, x, y, value=None):
		self.up = up
		self.down = down
		self.left = left
		self.right = right
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


class UnitTest(unittest.TestCase):

	def test_node_creation(self):
		node =  Node(None, None, None, None, None, None, 5)
		self.assertEqual(node.value, 5)



def main3():
	unittest.main()


if __name__ == '__main3__':
	main3()


