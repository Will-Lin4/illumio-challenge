from typing import Tuple
import csv

# Individual node for class below
class IntervalNode:
	def __init__(self, start_interval : int, end_interval : int):
		self.left_node = None
		self.right_node = None
		self.next_node = None

		self.start_interval = start_interval
		self.end_interval = end_interval

# Implements a BST based on the start in a range iteratively (to prevent recursion depth from exceeding for large rule sets)
# Each node in the tree is optionally connected to another tree (like a linked list)
class LinkedIntervalTree:
	def __init__(self):
		self.root = None

	# Intervals in this case would be the a tuple of tuples. Each tuple represents the ranges of the port and each part of the ip address
	def add_intervals(self, intervals : Tuple[Tuple]):
		if len(intervals) == 0:
			return

		start_interval, end_interval = intervals[0]

		# If the root doesn't exist, initialize the root
		if self.root is None:
			self.root = IntervalNode(start_interval, end_interval)

		# currNode specifies the tree we are in. We want to add the the first of the intervals into this tree
		currNode = self.root
		
		# We traverse through the tree iteratively, trying to add the first value of the intervals
		while len(intervals) > 0:

			# When we find the appropriate node (either it already existed or we created it in the previous loop), we need to add next interval in the next tree
			if start_interval == currNode.start_interval and end_interval == currNode.end_interval:

				# We want to add the rest of the interval into the node's next tree
				intervals = intervals[1:]

				if len(intervals) > 0:
					start_interval, end_interval = intervals[0]

					# If the next tree doesn't exist, make it
					if currNode.next_node is None:
						currNode.next_node = IntervalNode(start_interval, end_interval)

					currNode = currNode.next_node

			# The tree is a BST, so we place the nodes depending on if the start interval is greater or less than the node's start interval
			elif start_interval <= currNode.start_interval:
				if currNode.left_node is None:
					currNode.left_node = IntervalNode(start_interval, end_interval)

				currNode = currNode.left_node
			else:
				if currNode.right_node is None:
					currNode.right_node = IntervalNode(start_interval, end_interval)

				currNode = currNode.right_node

	def contains_values(self, values : Tuple[int]) -> bool:
		if self.root is None or len(values) == 0:
			return False

		# The list acts as a stack
		nodes = [self.root]

		while len(nodes) > 0:
			# Stores our current node on top of the stack
			i = len(nodes) - 1
			value = values[i]
			node = nodes[i]

			# There is nothing more to do in this tree, so remove it from the stack
			if node is None:
				nodes.pop()
				continue

			# Prepares the next value in the stack and replaces the node we stored with the next node down the tree if needed
			if value <= node.start_interval:
				if node.left_node is not None:
					nodes[i] = node.left_node
				else:
					nodes[i] = None
			else:
				if node.right_node is not None:
					nodes[i] = node.right_node
				else:
					nodes[i] = None


			# Checks if the value is in the interval. If it is, then add the next tree into the stack
			# Even if the node was replaced above, we would still add its next tree if it matches the criteria
			# When we pop it out, we will encounter the next node to evaluate
			if node.start_interval <= value and value <= node.end_interval:
				if len(values) == i + 1:
					return True
				elif node.next_node is not None:
					nodes.append(node.next_node)

		return False

class Rules:
	DIRECTION_INBOUND = 0
	DIRECTION_OUTBOUND = 1
	PROTOCOL_TCP = 0
	PROTOCOL_UDP = 1

	def __init__(self):
		self.trees = {}

	# We have four different trees, each corresponding with the direction and protocol. This just gets the key to access the tree
	def to_key(self, direction : str, protocol : str):
		if direction == "inbound":
			direction_key = Rules.DIRECTION_INBOUND
		else:
			direction_key = Rules.DIRECTION_OUTBOUND

		if protocol == "tcp":
			protocol_key = Rules.PROTOCOL_TCP
		else:
			protocol_key = Rules.PROTOCOL_UDP

		return (direction_key, protocol_key)

	# Converts port and ip_address into a tuple of tuples. Everything is a range, so even a single value is a range. x-x
	# Tuples specify the lower and upper bound (inclusive)
	def to_intervals(self, port : str, ip_address : str) -> Tuple[Tuple]:
		ports = port.split("-")
		if len(ports) == 1:
			port_start, port_end = int(ports[0]), int(ports[0])
		else:
			port_start, port_end = int(ports[0]), int(ports[1])

		address_range = ip_address.split("-")
		if len(address_range) == 1:
			address_start, address_end = address_range[0], None
		else:
			address_start, address_end = address_range[0], address_range[1]

		address_start = address_start.split(".")
		if address_end is not None:
			address_end = address_end.split(".")
		else:
			address_end = address_start

		return (
			(port_start, port_end),
			(int(address_start[0]), int(address_end[0])),
			(int(address_start[1]), int(address_end[1])),
			(int(address_start[2]), int(address_end[2])),
			(int(address_start[3]), int(address_end[3]))
		)

	# Converts ports and ip_address into a tuple of ints representation
	def to_values(self, port : str, ip_address : str) -> Tuple[int]:
		ip_address = ip_address.split(".")
		return (int(port), int(ip_address[0]), int(ip_address[1]), int(ip_address[2]), int(ip_address[3]))

	# Imports the rules into the appropriate tree
	def add_rule(self, direction : str, protocol : str, port : str, ip_address : str):
		tree_key = self.to_key(direction, protocol)
		if tree_key not in self.trees:
			self.trees[tree_key] = LinkedIntervalTree()

		interval_tree = self.trees[tree_key]
		intervals = self.to_intervals(port, ip_address)
		interval_tree.add_intervals(intervals)

	# Converts the rule into a tuple representation and accesses the tree to check the value
	def check_rule(self, direction : str, protocol : str, port : int, ip_address : str) -> bool:
		tree_key = self.to_key(direction, protocol)
		if tree_key not in self.trees:
			return False

		interval_tree = self.trees[tree_key]
		values = self.to_values(str(port), ip_address)
		return interval_tree.contains_values(values)

class Firewall:
	def __init__(self, file_path : str):
		self.rules = Rules()
		self.import_rules(file_path)

	# Import the rules from the csv file
	def import_rules(self, file_path : str):
		with open(file_path, 'r', encoding='utf-8') as rules:
			reader = csv.reader(rules, delimiter = ",")
			for row in reader:
				if len(row) > 0:
					self.rules.add_rule(row[0], row[1], row[2], row[3])

	def accept_packet(self, direction : str, protocol : str, port : int, ip_address : str) -> bool:
		return self.rules.check_rule(direction, protocol, port, ip_address)
