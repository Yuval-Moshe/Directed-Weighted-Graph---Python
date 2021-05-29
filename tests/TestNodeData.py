import unittest
from unittest import TestCase
from src.node_data import NodeData


class TestNodeData(TestCase):
    """Test Class for NodeData
       List of all the test in this Test class:
       basicFunctions():
       - Test 1.1 - create new node, the new node shouldn't be null.
       - Test 1.2 - node.getKey should be a number >= 0.
       - Test 1.3 - create a new node, the new node should have a different key from the previously created node.
       - Test 1.4 - set the tag of node_1 to 17, getTag should be 17 .
       - Test 1.5 - set the info of node_1 to "INFO", getInfo should be "INFO".
       - Test 1.6 - create a new 3D point with x=11, y=12, z=13 and set it as node_1's location, getLocation should be equals to that point.
       - Test 1.7 - adds edge from node2 to node1 with weight=6.5, and checks if get_edges_to_node() and get_edges_from_node() returns correct dict
       - Test 1.8 - get_edge_weight sholud return 6.5 (node2->node1 is with weight of 6.5)
    """

    def test_basicFunction(self):
        # Test 1.1
        node1 = NodeData(key=1)
        self.assertIsNotNone(node1)

        # Test 1.2
        self.assertTrue(node1.get_key() == 1)

        # Test 1.3
        node2 = NodeData(key=2)
        self.assertNotEqual(node1.get_key(), node2.get_key())

        # Test 1.4
        node1.set_tag(17)
        self.assertEqual(node1.get_tag(), 17)

        # Test 1.5
        node1.set_info("INFO")
        self.assertEqual(node1.get_info(), "INFO")

        # Test 1.6
        node1.set_pos((1,3,1.5))
        expected_pos = (1,3,1.5)
        self.assertEqual(node1.get_pos(), expected_pos)

        # Test 1.7
        node1.add_edge_to_node(2,6.5)
        expected = {2 : 6.5}
        self.assertEqual(node1.get_edges_to_node(), expected)
        node2.add_edge_from_node(1,6.5)
        expected = {1 : 6.5}
        self.assertEqual(node2.get_edges_from_node(), expected)

        # Test 1.8
        self.assertEqual(node2.get_edge_weight(1), 6.5)


if __name__ == '__main__':
    unittest.main()
