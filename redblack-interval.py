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

