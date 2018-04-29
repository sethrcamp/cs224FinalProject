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

	def tally_values(self):
		current_node = self.down
		self.value = 0

		while type(current_node) is not Header:
			self.value += current_node.value
			current_node = current_node.down


class Matrix:

	def __init__(self, values):
		self.removed_nodes = []
		self.first_header = None
		self.total_rows = 0
		self.zero_columns = False

		for row in values:
			self.add_row(row)

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
			new_node = Node(current_node.up.right, current_node.down.right, current_node, self.first_header.up, self.total_rows, i, values[i])

			new_node.up.down = new_node
			new_node.down.up = new_node
			new_node.left.right = new_node
			new_node.right.left = new_node

			current_node = new_node

		self.tally_all_values()
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

	def tally_all_values(self):
		current_header = self.first_header

		first = True
		while first or (current_header is not self.first_header):
			first = False
			current_header.tally_values()
			current_header = current_header.right

	def remove_row(self, index):
		self.remove_row_overlap(index)

		current_node = self.first_header
		for i in range(0, index+1):
			current_node = current_node.down

		first_node = current_node

		first = True
		while first or (current_node is not first_node):
			first = False

			current_node.up.down = current_node.down
			current_node.down.up = current_node.up
			current_node = current_node.right
			self.removed_nodes[index][current_node.y] = current_node

		self.tally_all_values()
		return first_node

	def remove_row_overlap(self, index):
		for i in range(0, len(self.removed_nodes[index])):
			current_node = self.removed_nodes[index][i]
			if current_node is not None:
				current_node.up.down = current_node.down
				current_node.down.up = current_node.up

	def restore_row(self, first_node):
		current_node = first_node

		first = True
		while first or (current_node is not first_node):
			first = False

			current_iterative_node = current_node.up
			while current_iterative_node.up.down is not current_iterative_node:
				current_iterative_node.down = current_node
				current_iterative_node = current_iterative_node.up
			current_iterative_node.down = current_node
			current_node.up = current_iterative_node

			current_iterative_node = current_node.down

			while current_iterative_node.down.up is not current_iterative_node:
				current_iterative_node.up = current_node
				current_iterative_node = current_iterative_node.down
			current_iterative_node.up = current_node
			current_node.down = current_iterative_node

			current_node = current_node.right
			self.removed_nodes[current_node.x][current_node.y] = None

		self.restore_row_overlap(first_node.x)
		self.tally_all_values()

	def restore_row_overlap(self, index):
		for i in range(0, len(self.removed_nodes[index])):
			current_node = self.removed_nodes[index][i]
			if current_node is not None:
				current_node.up.down = current_node
				current_node.down.up = current_node

	def remove_column(self, index):
		self.remove_column_overlap(index)

		current_node = self.first_header
		for i in range(0, index):
			current_node = current_node.right

		first_node = current_node.down

		if current_node is self.first_header:
			if current_node.right is current_node:
				self.zero_columns = True
				return first_node
			self.first_header = current_node.right

		first = True
		while first or (type(current_node) is not Header):
			current_node.left.right = current_node.right
			current_node.right.left = current_node.left

			if not first:
				self.removed_nodes[current_node.x][index] = current_node
			current_node = current_node.down
			first = False

		current_node.tally_values()
		return first_node

	def remove_column_overlap(self, index):
		for i in range(0, len(self.removed_nodes)):
			current_node = self.removed_nodes[i][index]
			if current_node is not None:
				current_node.left.right = current_node.right
				current_node.right.left = current_node.left

	def restore_column(self, first_node):
		current_node = first_node

		if current_node.y < self.first_header.down.y:
			self.first_header = current_node.up

		first = True
		while first or (current_node is not first_node):
			first = False

			current_iterative_node = current_node.left
			while current_iterative_node.left.right is not current_iterative_node:
				current_iterative_node.right = current_node
				current_iterative_node = current_iterative_node.left
			current_iterative_node.right = current_node
			current_node.left = current_iterative_node

			current_iterative_node = current_node.right

			while current_iterative_node.right.left is not current_iterative_node:
				current_iterative_node.left = current_node
				current_iterative_node = current_iterative_node.right
			current_iterative_node.left = current_node
			current_node.right = current_iterative_node

			if type(current_node) is not Header:
				self.removed_nodes[current_node.x][current_node.y] = None
			current_node = current_node.down

		self.restore_column_overlap(first_node.y)
		self.tally_all_values()

	def restore_column_overlap(self, index):
		for i in range(0, len(self.removed_nodes)):
			current_node = self.removed_nodes[i][index]
			if current_node is not None:
				current_node.left.right = current_node
				current_node.right.left = current_node

	def get_array_representation(self):
		if self.zero_columns:
			return []
		array = []
		current_node = self.first_header.down
		while type(current_node) is not Header:
			inner_array = []
			first_node_in_row = current_node
			first = True
			while first or (current_node is not first_node_in_row):
				first = False
				inner_array.append(current_node.value)
				current_node = current_node.right
			array.append(inner_array)
			current_node = current_node.down

		return array


class UnitTest(unittest.TestCase):

	def test_node_creation(self):
		node = Node(None, None, None, None, 1, 2, 5)
		self.assertEqual(node.value, 5)
		self.assertEqual(node.x, 1)
		self.assertEqual(node.y, 2)

	def test_circular_node_creation(self):
		node = Node(None, None, None, None, None, None)
		self.assertEqual(node.up, node)
		self.assertEqual(node.down, node)
		self.assertEqual(node.left, node)
		self.assertEqual(node.right, node)

	def test_header_creation(self):
		node = Header(None, None, None, None, False)
		self.assertEqual(node.value, None)
		self.assertEqual(node.x, None)
		self.assertEqual(node.y, None)
		self.assertEqual(node.is_primary, False)

	def test_circular_header_creation(self):
		node = Header(None, None, None, None, None)
		self.assertEqual(node.up, node)
		self.assertEqual(node.down, node)
		self.assertEqual(node.left, node)
		self.assertEqual(node.right, node)

	def test_header_tally_values(self):
		header = Header(None, None, None, None, False)
		node1 = Node(header, None, None, None, 1, 1, 1)
		node2 = Node(node1, None, None, None, 2, 1, 2)
		node3 = Node(node2, header, None, None, 3, 1, 3)

		header.up = node3
		header.down = node1
		node1.down = node2
		node2.down = node3

		header.tally_values()

		self.assertEqual(header.value, 6)

	def test_header_tally_values_when_negative(self):
		header = Header(None, None, None, None, False)
		node1 = Node(header, None, None, None, 1, 1, 1)
		node2 = Node(node1, None, None, None, 2, 1, 2)
		node3 = Node(node2, header, None, None, 3, 1, -3)

		header.up = node3
		header.down = node1
		node1.down = node2
		node2.down = node3

		header.tally_values()

		self.assertEqual(header.value, 0)

	def test_header_tally_values_after_change(self):
		header = Header(None, None, None, None, False)
		node1 = Node(header, None, None, None, 1, 1, 1)
		node2 = Node(node1, None, None, None, 2, 1, 2)
		node3 = Node(node2, header, None, None, 3, 1, 3)

		header.up = node3
		header.down = node1
		node1.down = node2
		node2.down = node3

		header.tally_values()

		self.assertEqual(header.value, 6)

		node3.value += 10
		header.tally_values()

		self.assertEqual(header.value, 16)

	def test_matrix_creation_no_values(self):
		matrix = Matrix([])
		self.assertEqual(matrix.removed_nodes, [])
		self.assertEqual(matrix.first_header, None)
		self.assertEqual(matrix.total_rows, 0)

	def test_matrix_add_row(self):
		matrix = Matrix([])
		matrix.add_row([1, 2, 3])

		header1 = Header(None, None, None, None, False)
		header2 = Header(None, None, header1, None, False)
		header3 = Header(None, None, header2, header1, False)

		header1.left = header3
		header1.right = header2
		header2.right = header3

		node1 = Node(header1, header1, None, None, 1, 1, 1)
		node2 = Node(header2, header2, node1, None, 1, 2, 2)
		node3 = Node(header3, header3, node2, node1, 1, 3, 3)

		header1.down = node1
		header2.down = node2
		header3.down = node3

		header1.up = node1
		header2.up = node2
		header3.up = node3

		node1.left = node3
		node1.right = node2
		node2.right = node3

		self.assertEqual(node1.value, matrix.first_header.down.value)
		self.assertEqual(node2.value, matrix.first_header.down.right.value)
		self.assertEqual(node3.value, matrix.first_header.down.left.value)

		self.assertEqual(node1.value, matrix.first_header.down.value)
		self.assertEqual(node2.value, matrix.first_header.down.right.value)
		self.assertEqual(node3.value, matrix.first_header.down.left.value)

	def test_matrix_add_multiple_rows(self):
		matrix = Matrix([])
		matrix.add_row([1, 2, 3])
		matrix.add_row([4, 5, 6])
		matrix.add_row([7, 8, 9])

		header1 = Header(None, None, None, None, False)
		header2 = Header(None, None, header1, None, False)
		header3 = Header(None, None, header2, header1, False)

		header1.left = header3
		header1.right = header2
		header2.right = header3

		node1 = Node(header1, None, None, None, 1, 1, 1)
		node2 = Node(header2, None, node1, None, 1, 2, 2)
		node3 = Node(header3, None, node2, node1, 1, 3, 3)

		node1.left = node3
		node1.right = node2
		node2.right = node3

		node4 = Node(node1, None, None, None, 2, 1, 4)
		node5 = Node(node2, None, node4, None, 2, 2, 5)
		node6 = Node(node3, None, node5, node4, 2, 3, 6)

		node4.left = node6
		node4.right = node5
		node2.right = node6

		node7 = Node(node4, header1, None, None, 3, 1, 7)
		node8 = Node(node5, header2, node7, None, 3, 2, 8)
		node9 = Node(node6, header3, node8, node7, 3, 3, 9)

		header1.down = node1
		header2.down = node2
		header3.down = node3

		header1.up = node7
		header2.up = node8
		header3.up = node9

		node1.down = node4
		node2.down = node5
		node3.down = node6

		node4.down = node7
		node5.down = node8
		node6.down = node9

		self.assertEqual(node1.value, matrix.first_header.down.value)
		self.assertEqual(node2.value, matrix.first_header.down.right.value)
		self.assertEqual(node3.value, matrix.first_header.down.left.value)

		self.assertEqual(node4.value, matrix.first_header.down.down.value)
		self.assertEqual(node5.value, matrix.first_header.down.down.right.value)
		self.assertEqual(node6.value, matrix.first_header.down.down.left.value)

		self.assertEqual(node7.value, matrix.first_header.down.down.down.value)
		self.assertEqual(node8.value, matrix.first_header.down.down.down.right.value)
		self.assertEqual(node9.value, matrix.first_header.down.down.down.left.value)


	def test_get_array_representation(self):
		matrix = Matrix([])
		matrix.add_row([1, 2, 3])
		matrix.add_row([4, 5, 6])
		matrix.add_row([7, 8, 9])

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_creation_with_values(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_tally_all_ones(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		matrix.tally_all_values()

		self.assertEqual(12, matrix.first_header.value)
		self.assertEqual(15, matrix.first_header.right.value)
		self.assertEqual(18, matrix.first_header.left.value)

	def test_matrix_add_row_over_bounds(self):
		matrix = Matrix([[1, 2, 3]])
		self.assertRaises(ValueError, matrix.add_row, [4, 5, 6, 7])

	def test_matrix_add_row_under_bounds(self):
		matrix = Matrix([[1, 2, 3]])
		self.assertRaises(ValueError, matrix.add_row, [4, 5])

	def test_matrix_get_number_of_headers(self):
		matrix = Matrix([[1, 2, 3]])
		self.assertEqual(3, matrix.get_number_of_headers())

	def test_matrix_remove_row_no_overlap(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		matrix.remove_row(1)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [7, 8, 9]])

	def test_matrix_remove_multiple_rows_non_successive(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]])

		matrix.remove_row(1)
		matrix.remove_row(2)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [7, 8, 9], [13, 14, 15]])

	def test_matrix_remove_multiple_rows_successive(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]])

		matrix.remove_row(1)
		matrix.remove_row(1)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [10, 11, 12], [13, 14, 15]])

	def test_matrix_remove_all_rows(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		matrix.remove_row(0)
		matrix.remove_row(0)
		matrix.remove_row(0)

		self.assertEqual(matrix.get_array_representation(), [])

	def test_matrix_remove_column_no_overlap(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		matrix.remove_column(0)

		self.assertEqual(matrix.get_array_representation(), [[2, 3], [5, 6], [8, 9]])

	def test_matrix_remove_multiple_columns_non_successive(self):
		matrix = Matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])

		matrix.remove_column(1)
		matrix.remove_column(2)

		self.assertEqual(matrix.get_array_representation(), [[1, 3, 5], [6, 8, 10], [11, 13, 15]])

	def test_matrix_remove_multiple_columns_successive(self):
		matrix = Matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])

		matrix.remove_column(1)
		matrix.remove_column(1)

		self.assertEqual(matrix.get_array_representation(), [[1, 4, 5], [6, 9, 10], [11, 14, 15]])

	def test_matrix_remove_column_with_first_header(self):
		matrix = Matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])

		new_header = matrix.first_header.right

		matrix.remove_column(0)

		self.assertEqual(matrix.first_header, new_header)
		self.assertEqual(matrix.get_array_representation(), [[2, 3, 4, 5], [7, 8, 9, 10], [12, 13, 14, 15]])

	def test_matrix_remove_column_with_first_header_where_next_column_is_non_adjacent(self):
		matrix = Matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])

		new_header = matrix.first_header.right.right

		matrix.remove_column(1)
		matrix.remove_column(0)

		self.assertEqual(matrix.first_header, new_header)
		self.assertEqual(matrix.get_array_representation(), [[3, 4, 5], [8, 9, 10], [13, 14, 15]])

	def test_matrix_remove_all_columns(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		matrix.remove_column(0)
		matrix.remove_column(0)
		matrix.remove_column(0)

		self.assertEqual(matrix.get_array_representation(), [])

	def test_matrix_remove_row_remove_column(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		matrix.remove_row(1)
		matrix.remove_column(1)

		self.assertEqual(matrix.get_array_representation(), [[1, 3], [7, 9]])

	def test_matrix_remove_column_remove_row(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		matrix.remove_column(1)
		matrix.remove_row(1)

		self.assertEqual(matrix.get_array_representation(), [[1, 3], [7, 9]])

	def test_matrix_restore_non_overlapping_row(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_row(1)
		matrix.restore_row(node_removed)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_restore_multiple_rows_same_order(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_row(1)
		node_removed2 = matrix.remove_row(1)
		matrix.restore_row(node_removed)
		matrix.restore_row(node_removed2)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_restore_multiple_rows_different_order(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_row(1)
		node_removed2 = matrix.remove_row(1)
		matrix.restore_row(node_removed2)
		matrix.restore_row(node_removed)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_restore_non_overlapping_column(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_column(1)
		matrix.restore_column(node_removed)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_restore_multiple_columns_same_order(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_column(1)
		node_removed2 = matrix.remove_column(1)
		matrix.restore_column(node_removed)
		matrix.restore_column(node_removed2)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_restore_multiple_columns_different_order(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_column(1)
		node_removed2 = matrix.remove_column(1)
		matrix.restore_column(node_removed2)
		matrix.restore_column(node_removed)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_restore_multiple_columns_difficult_order(self):
		matrix = Matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])

		node_removed = matrix.remove_column(1)
		node_removed2 = matrix.remove_column(1)
		node_removed3 = matrix.remove_column(1)
		node_removed4 = matrix.remove_column(1)
		matrix.restore_column(node_removed)
		matrix.restore_column(node_removed3)
		matrix.restore_column(node_removed4)
		matrix.restore_column(node_removed2)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])

	def test_matrix_remove_column_with_first_header_backtracking_header(self):

		matrix = Matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])

		new_header = matrix.first_header

		removed_node = matrix.remove_column(0)
		matrix.remove_column(0)
		matrix.restore_column(removed_node)

		self.assertEqual(matrix.first_header, new_header)
		self.assertEqual(matrix.get_array_representation(), [[1, 3, 4, 5], [6, 8, 9, 10], [11, 13, 14, 15]])

	def test_matrix_remove_and_restore_rows_and_columns_backtracking_order(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_row(1)
		node_removed2 = matrix.remove_column(1)
		matrix.restore_column(node_removed2)
		matrix.restore_row(node_removed)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

	def test_matrix_remove_and_restore_rows_and_columns_respective_order(self):
		matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

		node_removed = matrix.remove_row(1)
		node_removed2 = matrix.remove_column(1)
		matrix.restore_row(node_removed)
		matrix.restore_column(node_removed2)

		self.assertEqual(matrix.get_array_representation(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

def main():
	unittest.main()

if __name__ == '__main__':
	main()


