import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

class Node:
    def __init__(self, data, depth=0):
        self.data = data
        self.color = 'RED'  # New nodes are always red
        self.left = None
        self.right = None
        self.parent = None
        self.depth = depth  # Track the depth of the node

class RedBlackTree:
    def __init__(self):
        self.NIL_LEAF = Node(None)
        self.NIL_LEAF.color = 'BLACK'
        self.root = self.NIL_LEAF

    def rotate_left(self, node):
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

        # Update depths after rotation
        right_child.depth = node.depth
        node.depth += 1

    def rotate_right(self, node):
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

        # Update depths after rotation
        left_child.depth = node.depth
        node.depth += 1

    def fix_insert(self, node):
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
        new_node = Node(data)
        new_node.left = self.NIL_LEAF
        new_node.right = self.NIL_LEAF

        parent = None
        current = self.root
        depth = 0  # Keep track of the depth of the current node

        while current != self.NIL_LEAF:
            parent = current
            depth += 1  # Increment depth as we move down the tree
            if new_node.data < current.data:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        new_node.depth = depth  # Assign the calculated depth to the new node

        if parent is None:
            self.root = new_node
        elif new_node.data < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = 'RED'
        self.fix_insert(new_node)

    def inorder_traversal(self, node):
        if node != self.NIL_LEAF:
            self.inorder_traversal(node.left)
            print(f'{node.data} ({node.color}, depth={node.depth})', end=' ')
            self.inorder_traversal(node.right)

    def visualize(self):
        G = nx.DiGraph()
        labels = {}
        self._build_visual(self.root, G, labels)
        pos = graphviz_layout(G, prog="dot")  # Tree-like layout using pydot and graphviz
        colors = [G.nodes[n]['color'] for n in G.nodes]
        nx.draw(G, pos, labels=labels, node_color=colors, with_labels=True, node_size=1500, font_size=10, font_color='white')
        plt.show()

    def _build_visual(self, node, G, labels):
        if node != self.NIL_LEAF:
            # Label includes both the data and depth
            G.add_node(node.data, color='red' if node.color == 'RED' else 'black')
            labels[node.data] = f'{node.data} (d={node.depth})'
            if node.left != self.NIL_LEAF:
                G.add_edge(node.data, node.left.data)
            if node.right != self.NIL_LEAF:
                G.add_edge(node.data, node.right.data)
            self._build_visual(node.left, G, labels)
            self._build_visual(node.right, G, labels)

# Example usage of the RedBlackTree class:
if __name__ == '__main__':
    tree = RedBlackTree()
    elements = [20, 15, 25, 10, 5, 1, 17, 22, 27,8,99,101,7,2,33,34,35,103,77,78,79]

    for element in elements:
        tree.insert(element)

    print("Inorder traversal of the Red-Black Tree:")
    tree.inorder_traversal(tree.root)
    print("\nVisualizing Red-Black Tree with Depth Information:")
    tree.visualize()