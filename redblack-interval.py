""" 
An interval tree is a type of self-balancing tree that stores intervals and allows efficient querying of overlapping intervals. 
For example, if you’re maintaining time intervals in a scheduling program, an interval tree would allow you to efficiently query 
if any existing intervals overlap with a new one.

Lets adapt the Red-Black Tree we you used before, augmenting it to store intervals instead of single values. 
Each node in the tree will represent an interval, and the augmented data will include the maximum endpoint of all 
intervals in the subtree rooted at each node. This allows us to efficiently query whether any intervals overlap with a given interval.

Plan:

	1.	Node Structure: Each node stores an interval [low, high] and will be augmented with the maximum endpoint of any interval in its subtree.
	2.	Insertion: During insertion, the tree is balanced as in a Red-Black Tree, and the augmented data (max endpoint) is updated accordingly.
	3.	Overlap Query: We’ll add a method to check whether a given interval overlaps with any of the intervals stored in the tree.

Interval Overlap Definition:

Two intervals [low1, high1] and [low2, high2] overlap if:
- low 1 is less than or equal to high 2 
- and
- low 2 is less than or equal to high 1

  """

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

class IntervalNode:
    def __init__(self, interval, NIL_LEAF=None):
        self.interval = interval  # Store the interval [low, high]
        self.color = 'RED'  # New nodes are always red
        self.left = NIL_LEAF  # Assign NIL_LEAF instead of None
        self.right = NIL_LEAF  # Assign NIL_LEAF instead of None
        self.parent = None
        self.max_endpoint = interval[1]  # Augmented data: maximum endpoint in the subtree

        # Debugging the node creation
        print(f"Created node with interval {self.interval} and max endpoint {self.max_endpoint}")

class IntervalTree:
    def __init__(self):
        # Step 1: Create the NIL_LEAF node with None for left and right
        self.NIL_LEAF = IntervalNode((float('-inf'), float('-inf')))
        # Step 2: Set the NIL_LEAF's left and right to itself after creation
        self.NIL_LEAF.color = 'BLACK'
        self.NIL_LEAF.left = self.NIL_LEAF
        self.NIL_LEAF.right = self.NIL_LEAF
        self.NIL_LEAF.max_endpoint = float('-inf')  # NIL nodes have a max endpoint of negative infinity
        self.root = self.NIL_LEAF

        print(f"Initialized NIL_LEAF: {self.NIL_LEAF}")

    def rotate_left(self, node):
        print(f"Rotate left on node {node.interval}")
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.NIL_LEAF:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

        # Update max_endpoint after rotation
        self.update_max_endpoint(node)
        self.update_max_endpoint(right_child)

    def rotate_right(self, node):
        print(f"Rotate right on node {node.interval}")
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.NIL_LEAF:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

        # Update max_endpoint after rotation
        self.update_max_endpoint(node)
        self.update_max_endpoint(left_child)

    def fix_insert(self, node):
        print(f"Fixing insert on node with interval {node.interval}")
        while node != self.root and node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self.rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self.rotate_left(node.parent.parent)
        self.root.color = 'BLACK'

    def insert(self, interval):
        print(f"Inserting interval {interval}")
        new_node = IntervalNode(interval, self.NIL_LEAF)  # Create a new node with NIL_LEAF as children

        parent = None
        current = self.root

        # Debug: Check root initialization
        if current is None:
            raise RuntimeError("Root is None, should be NIL_LEAF")

        while current != self.NIL_LEAF:
            parent = current
            if new_node.interval[0] < current.interval[0]:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.interval[0] < parent.interval[0]:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = 'RED'
        self.fix_insert(new_node)

        # Update max_endpoint from the inserted node upwards
        print(f"Calling update_max_endpoint_upwards for node {new_node.interval}")
        self.update_max_endpoint_upwards(new_node)

    def update_max_endpoint(self, node):
        if node == self.NIL_LEAF:
            return

        # Max endpoint is the maximum of the node's interval endpoint and the max_endpoints of its children
        node.max_endpoint = max(node.interval[1], node.left.max_endpoint, node.right.max_endpoint)
        print(f"Updated max endpoint for node {node.interval}: {node.max_endpoint}")

    def update_max_endpoint_upwards(self, node):
        while node != self.NIL_LEAF:
            print(f"Updating max endpoint for node {node.interval}")
            self.update_max_endpoint(node)
            if node.parent is None:  # Stop at root node
                break
            node = node.parent

    def overlap_search(self, interval):
        """Search for any interval in the tree that overlaps with the given interval."""
        return self._overlap_search(self.root, interval)

    def _overlap_search(self, node, interval):
        if node == self.NIL_LEAF:
            return None

        if self._do_overlap(node.interval, interval):
            return node.interval

        if node.left != self.NIL_LEAF and node.left.max_endpoint >= interval[0]:
            return self._overlap_search(node.left, interval)

        return self._overlap_search(node.right, interval)

    def _do_overlap(self, interval1, interval2):
        """Check if two intervals overlap."""
        return interval1[0] <= interval2[1] and interval2[0] <= interval1[1]

    def inorder_traversal(self, node):
        if node != self.NIL_LEAF:
            self.inorder_traversal(node.left)
            print(f'{node.interval} (max={node.max_endpoint})', end=' ')
            self.inorder_traversal(node.right)

    def visualize(self):
        G = nx.DiGraph()
        labels = {}
        self._build_visual(self.root, G, labels)
        pos = graphviz_layout(G, prog="dot")  # Tree-like layout using pydot and graphviz
        colors = [G.nodes[n]['color'] for n in G.nodes]
        nx.draw(G, pos, labels=labels, node_color=colors, with_labels=True, node_size=8000, font_size=10, font_color='white')
        plt.show()

    def _build_visual(self, node, G, labels):
        if node != self.NIL_LEAF:
            # Label includes both the interval and max endpoint in its subtree
            G.add_node(node.interval, color='red' if node.color == 'RED' else 'black')
            labels[node.interval] = f'{node.interval} (max={node.max_endpoint})'
            if node.left != self.NIL_LEAF:
                G.add_edge(node.interval, node.left.interval)
            if node.right != self.NIL_LEAF:
                G.add_edge(node.interval, node.right.interval)
            self._build_visual(node.left, G, labels)
            self._build_visual(node.right, G, labels)

# Example usage of the IntervalTree class:
if __name__ == '__main__':
    tree = IntervalTree()
    
    # List of intervals to insert into the tree (e.g., for a scheduling program)
    intervals = [(4, 5), (24, 29), (48, 58), (6, 12), (43, 45), (38, 43), 
        (5, 7), (41, 43), (66, 73), (47, 53), (64, 67), (72, 81), 
        (11, 12), (85, 89), (83, 90), (30, 35), (17, 27), (53, 57), 
        (51, 59), (81, 89), (40, 49), (85, 94), (58, 62), (25, 32), 
        (37, 45), (85, 94), (11, 21), (54, 60)]
    
    # Insert intervals into the tree
    for interval in intervals:
        tree.insert(interval)

    # Perform an inorder traversal to show the tree structure and max_endpoints
    print("Inorder traversal of the Interval Tree:")
    tree.inorder_traversal(tree.root)
    print("\nVisualizing the Interval Tree with Max Endpoints:")
    tree.visualize()

    # Search for overlapping intervals
    search_interval = (14, 16)
    result = tree.overlap_search(search_interval)
    if result:
        print(f"\nInterval {search_interval} overlaps with {result} in the tree.")
    else:
        print(f"\nNo overlapping interval found for {search_interval}.")


    """
The max_endpoint parameter (or simply max) in an interval tree is an augmented data field that helps efficiently manage and query intervals.

Purpose of max_endpoint:

	•	Definition: For any node in the interval tree, the max_endpoint stores the largest endpoint (high) of any 
        interval in the subtree rooted at that node, including the node itself and its children.
	•	Why It’s Useful:
            The max_endpoint allows the tree to efficiently check if an interval might overlap with others in the tree. 
            When querying for an overlapping interval, you can prune entire subtrees based on the max_endpoint values. 
            If a subtree’s maximum endpoint is less than the start of the query interval, there’s no need to search that subtree 
                further because no intervals in it can overlap with the query.

Example:

Let’s say we have the following intervals:

	•	(15, 20)
	•	(10, 30)
	•	(17, 19)
	•	(5, 20)
	•	(12, 15)
	•	(30, 40)

Here’s what max_endpoint would represent:

	1.	Node (10, 30):
	•	The interval is [10, 30].
	•	The subtree rooted at this node has a maximum endpoint of 40 (due to the right child (30, 40)), so max_endpoint = 40.
	2.	Node (5, 20):
	•	The interval is [5, 20].
	•	The maximum endpoint of the subtree rooted here is 30, so max_endpoint = 30.

How max_endpoint Works in Overlap Queries:

Let’s say you want to check if the interval [14, 16] overlaps with any intervals in the tree:

	1.	Start at the root:
        If the interval at the root overlaps with [14, 16], return it. 
        Otherwise, check if the left child needs to be searched.
	2.	Check the max_endpoint of the left child:
        If the max_endpoint of the left child is smaller than 14, you can skip the left child 
            because no intervals in that subtree can overlap with [14, 16].
	3.	Continue Searching:
        If necessary, move to the right child and repeat the process, only visiting subtrees 
            where there’s a chance of overlap based on max_endpoint.

Key Benefits:

	•	Efficient Overlap Queries: By using max_endpoint, you can prune entire subtrees during overlap queries, improving efficiency.
	•	Faster Interval Management: When combined with the balancing of a red-black tree, managing intervals (insertion, deletion, overlap checking) 
        becomes logarithmic in time complexity.

In summary, the max_endpoint field augments each node to store the maximum interval endpoint in its subtree, 
making interval queries efficient by allowing the tree to skip searching certain branches that cannot possibly 
contain overlapping intervals.

    """