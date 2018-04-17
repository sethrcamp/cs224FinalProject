import unittest

class Node:

	def __init__(self, up, down, left, right, x, y, value=None):
		
		self.up = up
		self.down = down
		self.left = left
		self.right = right
		self.x = x
		self.y = y
		self.value = value



class UnitTest(unittest.TestCase):

	def test_node_creation(self):
		node =  Node(None, None, None, None, None, None, 5)
		self.assertEqual(node.value, 5)



def main3():
	unittest.main()


if __name__ == '__main3__':
	main3()


