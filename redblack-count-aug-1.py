#	1.	Subtree Node Count Augmentation: Each node will track how many nodes exist 
#       in the subtree rooted at that node, including itself.
#	2.	Update Count During Insert and Rotation: Each time we insert a node or perform a rotation, 
#       we will update the subtree node counts for the affected nodes.
#	3.	Subtree Count Formula: The count at each node is 1 + left_subtree_count + right_subtree_count.

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

class Node:
    def __init__(self, data, NIL_LEAF=None):
        self.data = data
        self.color = 'RED'  # New nodes are always red
        self.left = NIL_LEAF  # Assign NIL_LEAF instead of None
        self.right = NIL_LEAF  # Assign NIL_LEAF instead of None
        self.parent = None
        self.subtree_count = 1  # Track the number of nodes in the subtree (including this node)

        # Debugging the node creation
        print(f"Created node {self.data} with left: {self.left} and right: {self.right}")

class RedBlackTree:
    def __init__(self):
        # Step 1: Create the NIL_LEAF node with None for left and right
        self.NIL_LEAF = Node(None)
        # Step 2: Set the NIL_LEAF's left and right to itself after creation
        self.NIL_LEAF.color = 'BLACK'
        self.NIL_LEAF.left = self.NIL_LEAF
        self.NIL_LEAF.right = self.NIL_LEAF
        self.NIL_LEAF.subtree_count = 0  # NIL nodes have a subtree count of 0
        self.root = self.NIL_LEAF

        print(f"Initialized NIL_LEAF: {self.NIL_LEAF}")

    def rotate_left(self, node):
        print(f"Rotate left on node {node.data}")
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

        # Update subtree counts after rotation
        self.update_subtree_count(node)
        self.update_subtree_count(right_child)

    def rotate_right(self, node):
        print(f"Rotate right on node {node.data}")
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

        # Update subtree counts after rotation
        self.update_subtree_count(node)
        self.update_subtree_count(left_child)

    def fix_insert(self, node):
        print(f"Fixing insert on node {node.data}")
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

    def insert(self, data):
        print(f"Inserting {data}")
        new_node = Node(data, self.NIL_LEAF)  # Create a new node with NIL_LEAF as children

        parent = None
        current = self.root

        # Debug: Check root initialization
        if current is None:
            raise RuntimeError("Root is None, should be NIL_LEAF")

        while current != self.NIL_LEAF:
            parent = current
            if new_node.data < current.data:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.data < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = 'RED'
        self.fix_insert(new_node)

        # Update subtree count from the inserted node upwards
        print(f"Calling update_subtree_count_upwards for node {new_node.data}")
        self.update_subtree_count_upwards(new_node)

    def update_subtree_count(self, node):
        if node == self.NIL_LEAF:
            return

        # Subtree count is 1 (itself) + left subtree count + right subtree count
        node.subtree_count = 1 + node.left.subtree_count + node.right.subtree_count
        print(f"Updated node count for node {node.data}: {node.subtree_count}")

    def update_subtree_count_upwards(self, node):
        while node != self.NIL_LEAF:
            if node is None:
                raise RuntimeError("update_subtree_count_upwards() called on None node!")
            print(f"Updating count for node {node.data}")
            self.update_subtree_count(node)
            if node.parent is None:  # Stop at root node
                break
            node = node.parent

    def inorder_traversal(self, node):
        if node != self.NIL_LEAF:
            self.inorder_traversal(node.left)
            print(f'{node.data} ({node.color}, count={node.subtree_count})', end=' ')
            self.inorder_traversal(node.right)

    def visualize(self):
        G = nx.DiGraph()
        labels = {}
        self._build_visual(self.root, G, labels)
        pos = graphviz_layout(G, prog="dot")  # Tree-like layout using pydot and graphviz
        colors = [G.nodes[n]['color'] for n in G.nodes]
        nx.draw(G, pos, labels=labels, node_color=colors, with_labels=True, node_size=5000, font_size=10, font_color='white')
        plt.show()

    def _build_visual(self, node, G, labels):
        if node != self.NIL_LEAF:
            # Label includes both the data and count of nodes in its subtree
            G.add_node(node.data, color='red' if node.color == 'RED' else 'black')
            labels[node.data] = f'{node.data} (count={node.subtree_count})'
            if node.left != self.NIL_LEAF:
                G.add_edge(node.data, node.left.data)
            if node.right != self.NIL_LEAF:
                G.add_edge(node.data, node.right.data)
            self._build_visual(node.left, G, labels)
            self._build_visual(node.right, G, labels)

# Example usage of the RedBlackTree class:
if __name__ == '__main__':
    tree = RedBlackTree()
    elements = [400, 20, 15, 25, 10, 5, 1, 17, 22, 27,8,99,101,7,2,33,34,35,103,77,78,79]

    for element in elements:
        tree.insert(element)

    print("Inorder traversal of the Red-Black Tree:")
    tree.inorder_traversal(tree.root)
    print("\nVisualizing Red-Black Tree with Subtree Count Information:")
    tree.visualize()