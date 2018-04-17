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
			self.first_header = Header(None, None, None, None, False)
			current_header = self.first_header
			for i in range(1, len(values)):
				new_header = Header(None, None, current_header, self.first_header, False)
				self.first_header.left = new_header
				current_header.right = new_header
				current_header = new_header

		headers = self.get_number_of_headers()
		if len(values) != headers:
			raise ValueError("Invalid number of values for given number of rows. Matrix has "+str(headers)+" headers, but "+str(len(values))+" values were given.")

		current_node = Node(self.first_header.up, self.first_header, None, None, self.total_rows, 0, values[0])
		self.first_header.up = current_node
		current_node.up.down = current_node

		for i in range(1, len(values)):
			new_node = Node(current_node.up.left, current_node.down.left, current_node, self.first_header.up, self.total_rows, i, values[i])

			new_node.up.down = new_node
			new_node.down.up = new_node
			new_node.left.right = new_node
			new_node.right.left = new_node

			current_node = new_node

		self.tally_all_ones()
		self.total_rows += 1
		array_to_add = []
		for i in range(0, headers):
			array_to_add.append(None)
		self.removed_nodes.append(array_to_add)

	def get_number_of_headers(self):
		header = self.first_header.right
		total = 1
		while header is not self.first_header:
			total += 1
			header = header.right
		return total

	def tally_all_ones(self):
		current_header = self.first_header
		current_header.tally_ones()
		current_header = current_header.right
		while current_header is not self.first_header:
			current_header.tally_ones()
			current_header = current_header.right







"""
EVERYTHING BELOW IS FOR REFERENCE
DELETE WHEN DONE
"""

class UnitTest(unittest.TestCase):

	def test_node_creation(self):
		node = Node(None, None, None, None, None, None, 5)
		self.assertEqual(node.value, 5)

	def test_circular_node_creation(self):
		node = Node(None, None, None, None, None, None, 0)
		self.assertEqual(node.up, node)
		self.assertEqual(node.down, node)
		self.assertEqual(node.left, node)
		self.assertEqual(node.right, node)



def main():
	unittest.main()


if __name__ == '__main__':
	main()


