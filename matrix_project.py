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


"""
EVERYTHING BELOW IS FOR REFERENCE
DELETE WHEN DONE
"""

class Node2():

	def __init__(self, key=None, left=None, right=None, parent=None, depth=0):
		self.key = key
		self.left = left
		self.right = right
		self.parent = parent
		self.depth = depth

	def add_left(self, left):
		self.left = left
		left.parent = self
		left.depth = self.depth + 1

	def add_right(self, right):
		self.right = right
		right.parent = self
		right.depth = self.depth + 1

	def __str__(self):
		return str(self.key)


class BinaryTree():

	def __init__(self, root=None, array=None):
		self.root = root
		self.height = -1

		if array is not None:
			self.update_from_array(array)

	def preorder_walk(self, node=None):
		if node is None:
			node = self.root

		toReturn = [node.key]
		if node.left is not None:
			toReturn += self.preorder_walk(node.left)
		if node.right is not None:
			toReturn += self.preorder_walk(node.right)
		return toReturn


class BinaryTree_UnitTest(unittest.TestCase):

	def test_preorder_walk(self):
		" Test pre-order tree walk """
		bst = BinaryTree(array=(15, (7, (3, 2, 3), (10, 8, (14, 12, None))), (21, 19, (24, 24, 67))))
		print("test pre-order walk")
		bst.display()
		self.assertEqual(bst.preorder_walk(), [15, 7, 3, 2, 3, 10, 8, 14, 12, 21, 19, 24, 24, 67])


def main3():
	unittest.main()


if __name__ == '__main3__':
	main3()

