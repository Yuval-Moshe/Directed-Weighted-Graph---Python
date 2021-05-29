import unittest
from unittest import TestCase
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    """Test Class for GraphAlgo
    List of all the test in this Test class:
    - test_get_graph - checks if the simple method get_graph returns the algo_graph graph
    - test_saveNload_to_json1 - creates a graph with 6 nodes and 11 edges, save it to a file, load it back to another graph algo and see if both graph's are equal
    - test_saveNload_to_json2 - saves an empty graph a file, load it back to another graph algo and see if both graph's are equal (both empty)
    - test_load - trying to load to a graph from an empty file - return False, trying yo load to a graph from a file that does not exist - return False
    - test_save - trying to save a graph to a directory/file that does not exist - return False
    - test_shortest_path1 - a graph which 0 and 1 are connected by an edge from 0 to 1 with weight 10, but the shortest path is 0->2->3->1 with dist 8.
    - test_shortest_path2 - a graph with 5 nodes (0,1,2,3,4) and 2 edges 0->1, 2->3 : shortest_path(0,0) == [0,0] , shortest_path(1,0) == [float(inf), []], shortest_path(2,4) == [float(inf), []], shortest_path(2,7) == [float(inf), []], shortest_path(9,7) == [float(inf), []]
    - test_shortest_path3 - a graph with 30 nodes wich each node i is connected to i+1 by an edge i-> i+1, shortes_path(29,0) == (float('inf'), [])
    - test_connected_component1 - adding 5 nodes: add 7 edges, when node 4 is not connected to any other node, checks connected component on node 4 -> return [4]
                                  checks connected_component on node 2 -> returns all nodes except 4: [0,1,2,3]
                                  removes 2 edges - now connected component of 2 -> return: [2,3]
    - test_connected_component2 - adding 5 nodes and connected them all, now connected component of 2 -> reurns all nodes: [0,1,2,3,4]
    - test_connected_component3 - checks connected component for a node 1 when graph is empty, and when there is no node 1 in graph: returns []
    - test_connected_component4 - adding 5 nodes: add 7 edges, when node 4 is not connected to any other node, checks connected component on node 4 -> return [4]
                                  checks connected_component on node 2 -> returns all nodes except 4: [0,1,2,3]
                                  connect 4 in both direction edges - now connected component of 2 -> return: [0,1,2,3,4]
    - test_connected_components1 - adding 5 nodes to a graph and some edges, checks if connected_components returns correct list of lists
                                   it checks also when all nodes are connected -> returns [[0,1,2,3,4]]
    - test_connected_components2 - adding 5 nodes to the graph (no edges), checks connected_components - there are 5 -> returns [[0],[1],[2],[3],[4]]
    - test_connected_components3 - checks connected_components on an empty graph -> returns []
    """

    def test_get_graph(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.get_graph(), graph)

    def test_saveNload_to_json1(self):
        graph = DiGraph()
        for i in range(0, 6):
            graph.add_node(i)
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 0, 1)
        graph.add_edge(1, 3, 3)
        graph.add_edge(1, 2, 8)
        graph.add_edge(1, 5, 10)
        graph.add_edge(2, 1, 1)
        graph.add_edge(2, 4, 3)
        graph.add_edge(3, 0, 1)
        graph.add_edge(3, 1, 1)
        graph.add_edge(3, 4, 2)
        graph.add_edge(4, 5, 2)
        graph_algo = GraphAlgo(graph)
        graph_algo.save_to_json(r'..\data\new')
        graph_algo2 = GraphAlgo()
        graph_algo2.load_from_json(r'..\data\new')
        self.assertTrue(graph_algo.graph.__eq__(graph_algo2.graph))

    def test_saveNload_to_json2(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        flag_save = graph_algo.save_to_json(r'..\data\new_test')
        graph_algo2 = GraphAlgo()
        flag_load = graph_algo2.load_from_json(r'..\data\new_test')
        self.assertTrue(flag_save)
        self.assertTrue(flag_load)
        flag_save2 = graph_algo.save_to_json(r'..\data\new_test')
        self.assertTrue(flag_save2)

    def test_load(self):
        graph_algo = GraphAlgo()
        flag = graph_algo.load_from_json(r'..\data\empty_file')
        self.assertFalse(flag)
        flag = graph_algo.load_from_json(r'..\data\blabla.json')
        self.assertFalse(flag)

    def test_save(self):
        graph = DiGraph()
        for i in range(0, 6):
            graph.add_node(i)
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 0, 1)
        graph.add_edge(1, 3, 3)
        graph.add_edge(1, 2, 8)
        graph.add_edge(1, 5, 10)
        graph.add_edge(2, 1, 1)
        graph.add_edge(2, 4, 3)
        graph.add_edge(3, 0, 1)
        graph.add_edge(3, 1, 1)
        graph.add_edge(3, 4, 2)
        graph.add_edge(4, 5, 2)
        graph_algo = GraphAlgo(graph)
        flag = graph_algo.save_to_json(r'..\hello\bla.json')
        self.assertFalse(flag)


    def test_shortest_path1(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 3)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 1, 1)
        graph_algo = GraphAlgo(graph)
        comp_path = [0, 2, 3, 1]
        expected = (8, comp_path)
        self.assertEqual(graph_algo.shortest_path(0, 1), expected)

    def test_shortest_path2(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph.add_edge(0, 1, 2)
        graph.add_edge(2, 3, 2)
        graph_algo = GraphAlgo(graph)
        expected = (0, [0])
        self.assertEqual(graph_algo.shortest_path(0, 0), expected)
        expected = (float('inf'), [])
        self.assertEqual(graph_algo.shortest_path(1, 0), expected)
        self.assertEqual(graph_algo.shortest_path(2, 4), expected)
        self.assertEqual(graph_algo.shortest_path(2, 7), expected)
        self.assertEqual(graph_algo.shortest_path(9, 7), expected)

    def test_shortest_path3(self):
        graph = DiGraph()
        for i in range(0, 30):
            graph.add_node(i)
        for i in range(0, 29):
            graph.add_edge(i, i + 1, i + 3)
        graph_algo = GraphAlgo(graph)
        expected = (float('inf'), [])
        self.assertEqual(graph_algo.shortest_path(29, 0), expected)

    def test_connected_component1(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 3)
        graph.add_edge(2, 0, 3)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 2, 4)
        graph.add_edge(3, 1, 1)
        graph.add_edge(1, 3, 1)
        graph_algo = GraphAlgo(graph)
        expected = [4]
        self.assertEqual(graph_algo.connected_component(4), expected)
        self.assertTrue(set(graph_algo.connected_component(2)) == set([0, 1, 2, 3]))
        graph.remove_edge(2, 0)
        graph.remove_edge(1, 3)
        self.assertTrue(set(graph_algo.connected_component(2)) == set([2, 3]))

    def test_connected_component2(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 3)
        graph.add_edge(2, 0, 3)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 2, 4)
        graph.add_edge(3, 1, 1)
        graph.add_edge(1, 3, 1)
        graph.add_edge(1, 4, 1)
        graph.add_edge(4, 1, 1)
        graph_algo = GraphAlgo(graph)
        expected = [0, 1, 4, 3, 2]
        self.assertTrue(set(graph_algo.connected_component(2)) == set(expected))

    def test_connected_component3(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.connected_component(1), [])
        graph.add_node(2)
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.connected_component(1), [])

    def test_connected_component4(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 3)
        graph.add_edge(2, 0, 3)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 2, 4)
        graph.add_edge(3, 1, 1)
        graph.add_edge(1, 3, 1)
        graph_algo = GraphAlgo(graph)
        expected = [4]
        self.assertEqual(graph_algo.connected_component(4), expected)
        self.assertTrue(set(graph_algo.connected_component(2)) == set([0, 1, 2, 3]))
        graph.add_edge(2, 4, 3)
        graph.add_edge(4, 2, 3)
        self.assertTrue(set(graph_algo.connected_component(2)) == set([0, 1, 2, 3, 4]))

    def test_connected_components1(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 3)
        graph.add_edge(2, 0, 3)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 2, 4)
        graph.add_edge(3, 1, 1)
        graph.add_edge(1, 3, 1)
        graph_algo = GraphAlgo(graph)
        expected = [[0, 1, 2, 3], [4]]
        self.assertEqual(graph_algo.connected_components(), expected)
        graph.add_edge(4, 1, 1)
        graph_algo = GraphAlgo(graph)
        expected = [[0, 1, 2, 3], [4]]
        self.assertEqual(graph_algo.connected_components(), expected)
        graph.add_edge(1, 4, 3.5)
        graph_algo = GraphAlgo(graph)
        expected = [[0, 1, 2, 3, 4]]
        self.assertEqual(graph_algo.connected_components(), expected)


    def test_connected_components2(self):
        graph = DiGraph()
        for i in range(0, 5):
            graph.add_node(i)
        graph_algo = GraphAlgo(graph)
        expected = [[0], [1], [2], [3], [4]]
        self.assertEqual(graph_algo.connected_components(), expected)

    def test_connected_components3(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.connected_components(), [])

    # def test_plot_graph(self):
    #     self.fail()


if __name__ == '__main__':
    unittest.main()
