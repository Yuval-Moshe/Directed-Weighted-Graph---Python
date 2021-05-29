from builtins import list
from collections import deque
from json.decoder import JSONDecodeError
from random import random
from typing import List
from queue import PriorityQueue
import json
from matplotlib.patches import ConnectionPatch
from src.GraphInterface import GraphInterface
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    """
    This class implements the dw_graph_algorithms interface which allows preforming complex algorithms on a
    directed, weighted graph, with the following class variables:
    GraphInterface graph - the graph to preform the algorithms on.
    """

    def __init__(self, graph: GraphInterface = None):
        """
        Constructor
        """
        self.graph = graph
        if graph is not None:
            self.__build_reversed()
            self.graph_mc = self.graph.get_mc()

    def get_graph(self) -> GraphInterface:
        """
        Returns the directed weighted graph in this directed weighted graph algorithm's as graph.
        :return: directed weighted graph
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a directed weighted graph from the provided location (in the file param) and if is successfully loaded,
        initializes the graph of this GraphAlgo to be the loaded graph
        :param file_name
        :return: true if successfully loaded and initialized, false otherwise.
        """
        try:
            with open(file_name, "r") as json_file:
                try:
                    data = json.load(json_file)
                    nodes = data["Nodes"]
                    edges = data["Edges"]
                    graph = DiGraph()

                    if nodes is not None and edges is not None:
                        for node_element in nodes:
                            if node_element.get("id") is not None:
                                key = node_element.get("id")
                                if node_element.get("pos") is not None:
                                    list = node_element.get("pos").split(",")
                                    pos = (float(list[0]), float(list[1]), float(list[2]))
                                    graph.add_node(key, pos)
                                else:
                                    graph.add_node(node_id=key)
                            else:
                                return False
                        for edge_element in edges:
                            if edge_element.get("src") is not None and edge_element.get(
                                    "w") is not None and edge_element.get("dest") is not None:
                                src = edge_element.get("src")
                                weight = edge_element.get("w")
                                dest = edge_element.get("dest")
                                graph.add_edge(src, dest, weight)
                            else:
                                return False
                        self.graph = graph
                        self.__build_reversed()
                        self.graph_mc = self.graph.get_mc()
                    return True

                except IOError as e:
                    print(e)
                    return False

                except JSONDecodeError as er:
                    print(er)
                    return False

        except IOError as e:
            print(e)
            return False
        return False

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the current graph of this GraphAlgo in json format to the provided file location given in the fle param
        :param file_name
        :return: true if the graph was successfully saved to the file, false otherwise.
        """
        if self.graph is None:
            return False
        nodes_list = []
        edges_list = []
        json_dict = dict()
        all_nodes = self.graph.get_all_v().values()
        for node in all_nodes:
            curr_node = dict()
            pos_tup = node.get_pos()
            pos_str = ""
            if pos_tup is not None:
                for i in pos_tup:
                    pos_str += str(i)
                    pos_str += ","
                pos_str = pos_str[:-1]
                curr_node["pos"] = pos_str
            curr_node["id"] = node.get_key()
            nodes_list.append(curr_node)

            all_edges_from_node = self.graph.all_out_edges_of_node(node.get_key())
            for edge in all_edges_from_node.keys():
                curr_edge = dict()
                curr_edge["src"] = node.get_key()
                curr_edge["w"] = all_edges_from_node.get(edge)
                curr_edge["dest"] = edge
                edges_list.append(curr_edge)
        json_dict["Edges"] = edges_list
        json_dict["Nodes"] = nodes_list
        try:
            with open(file_name, 'w') as file:
                json.dump(json_dict, indent=4, fp=file)
            return True
        except IOError as e:
            print(e)
            return False
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        This function returns the shortest path between 2 nodes in a directed, weighted graph by preforming the __dijkstra() algorithm
        function and the __reconstruct_path() function (explanations under these functions)
        :param id1: source node
        :param id2: destination node
        :return: a tuple with 2 elements - first one is the shortest path distance (float), and the second is a list of
        nodes representing the shortest path from id1 to id2.
        Note - if there isn't any path between id1 and id2, or if one of them does not exist - returns (float('inf'),[])
        """
        if self.graph is None:
            return (float('inf'), [])
        if id1 not in self.graph.get_all_v() or id2 not in self.graph.get_all_v():
            return (float('inf'), [])
        prev = self.__dijkstra(id1, id2)
        path = self.__reconstruct_path(prev, id1, id2)
        if path is None:
            return (float('inf'), [])
        else:
            nodes = self.graph.get_all_v()
            ans = (nodes.get(id2).get_tag(), path)
            return ans

    def __dijkstra(self, src: int, dest: int):
        """
        Initialization:
        - a priority queue pq, which is prioritized by the tag of each node which will be used to store the shortest distance
        of this current node from the src node.
        - a float dist - at first will be initialized to float('inf') and will store the current shortest distance from src to dest.
        - visited set, which will store all the already visited nodes
        - prev dict - parent (key) of each node (value) which is the closest (by path weight) to the src node.
        The steps:
        - Set src tag (distance from src) to 0, and add it to pq.
        - Start going over the pq until it is empty, extract the head (marked as curr) of the pq and go over its neighbors (if it is not visited yet).
        - For each neighbor, define the current distance from src (in the path that goes through curr), and check if the current distance
        is shortest then the current shortest distance from src to path, if not - there is no point to continue with this neighbor.
        - If so, check if the current neighbor is the dest node, if so, replace dist var with the ni_dist_from_src var.
        - Check if the current neighbor as a parent node marked in the prev dict,  if not - set curr as his parent and change the
        neighbor's tag to ni_dist_from_src, if it does have a parent node, change the parent node and the tag of the neighbor only if
        ni_dist_from_src is smaller than the current tag of this neighbor.
        - Add the neighbor to the pq.
        Go thorough this process for each edge in the graph until the pq is empty and return the prev hashmap.
        :param src: the source node
        :param dest: the destination node
        :return: prev dict which contains the parent of each node which is the closest to the src node (considering path weight)
        """
        pq = PriorityQueue()
        dist = float('inf')
        visited = set()
        prev = dict()
        nodes = self.graph.get_all_v()
        nodes[src].set_tag(0)
        pq.put((nodes[src].get_tag(), src))
        while len(pq.queue) != 0:
            curr_key = pq.get(0)[1]
            curr = nodes[curr_key]
            if curr_key not in visited and curr_key != dest:
                visited.add(curr_key)
                curr_ni = nodes[curr_key].get_edges_from_node().keys()
                for ni_key in curr_ni:
                    ni = nodes[ni_key]
                    if ni_key not in visited:
                        ni_dist_from_src = curr.get_tag() + curr.get_edge_weight(ni_key)
                        if ni_dist_from_src < dist:
                            if ni_key == dest:
                                dist = ni_dist_from_src
                        if prev.get(ni_key) is None:
                            ni.set_tag(ni_dist_from_src)
                            prev[ni_key] = curr_key
                        elif ni_dist_from_src < ni.get_tag():
                            ni.set_tag(ni_dist_from_src)
                            prev[ni_key] = curr_key
                        pq.put((ni.get_tag(), ni_key))
        return prev

    def __reconstruct_path(self, prev: dict, src: int, dest: int):
        """
        This function gets the prev dict, the src and dest nodes, and trying to construct a path between dest to src (the reversed way) by adding to a list the prev of dest,
        and then the prev of the prev of dest, and so on, until it reaches the src node, if it does - its the shortest path
        between src and dest, if it can't reach the src node - there is no path between src and dest.
        The function ends by reversing the path, to make it from src to dest and not from dest to src.
        :param prev: the dict that was returned from __dijkstra
        :param src: source node
        :param dest: destination node
        :return: list of nodes representing the shortest path from src to dest. If there is no such path, function will return None
        """
        path_temp = [dest]
        i = dest
        while prev.get(i) is not None:
            path_temp.append(prev.get(i))
            i = prev.get(i)

        if len(path_temp) != 0 and path_temp[len(path_temp) - 1] is src:
            path_temp.reverse()
            return path_temp
        else:
            return None

    def connected_component(self, id1: int) -> list:
        """
        This function checks and finally returns a list all component connected to the given node that its key id1 -
        it means that for each 2 nodes A and B in the list there is a path from A to B anf from B to A.
        So, the functions takes the given node, and adds to a dict all the nodes which are connected to him in some path, by preforming
        the BFS algorithm. Then, the functions build the reversed graph as described, and preform the same BFS algorithm.
        And finaly returns the intersection between them.
        :param id1: key of the node
        :return: list - of all nodes in the connected component of node id1
        """
        if self.graph is None:
            return []
        nodes = self.graph.get_all_v()
        if len(nodes) == 0 or id1 not in nodes.keys():
            return []
        if self.graph_mc != self.graph.get_mc():
            self.__build_reversed()
            self.graph_mc = self.graph.get_mc()
        q = deque()
        q.append(id1)
        connected = {id1: True}
        connections_list = [id1]
        while len(q) != 0:
            curr = q.popleft()
            curr_edges = self.graph.all_out_edges_of_node(curr)
            for curr_ni in curr_edges.keys():
                if connected.get(curr_ni) is None:
                    q.append(curr_ni)
                    connected[curr_ni] = True
                    connections_list.append(curr_ni)
        q.append(id1)
        r_connected = {id1: True}
        r_connections_list = [id1]
        while len(q) != 0:
            curr = q.popleft()
            curr_edges = self.reversed.all_out_edges_of_node(curr)
            for curr_ni in curr_edges.keys():
                if r_connected.get(curr_ni) is None:
                    q.append(curr_ni)
                    r_connected[curr_ni] = True
                    r_connections_list.append(curr_ni)
        return list(set(connections_list) & set(r_connections_list))

    def connected_components(self) -> List[list]:
        """
        This function checks and finally returns in a list of lists of all connected components in the graph.
        This function goes over all nodes in the graph and for each node, checks by using connected_component function, which
        list cintains its connected components.
        When going over a node, we first check that it doesn't appear aready in a connected component.
        :return: list of lists - each list in the list that is returned, contains all nodes that are connected to each other in some path,
        it means that for each 2 nodes A and B, there is a path from A to B and there is a path from B to A
        """
        if self.graph is None:
            return []
        nodes = self.graph.get_all_v()
        keys = nodes.keys()
        ans = []
        connected = []
        for key in keys:
            if key not in connected:
                key_connected = self.connected_component(key)
                connected.extend(key_connected)
                ans.append(key_connected)
        return ans


    def plot_graph(self) -> None:
        """
        This function plots the current DiGraph of this GraphAlgo using the matplotlib library, by first calling the
        private set_axis function (find explanation above the function) and then going over all the un-positioned
        nodes in the graph, and finding them a place based on the current other un-positioned nodes location,
        so that the un-positioned nodes of this graph will be equaly divided  in to the 4 quarter of this graph's area
        in order to create the possible best elegant representation of this graph.
        """
        if self.graph is None:
            return None
        nodes = self.graph.get_all_v()
        axis_return = self.__set_axis()
        un_positioned = axis_return[4]
        min_x = axis_return[0]
        max_x = axis_return[1]
        min_y = axis_return[2]
        max_y = axis_return[3]
        un_pos_quarter = [0, 0, 0, 0]
        ax = plt.axes()
        for node in un_positioned:
            quarter = un_pos_quarter.index(min(un_pos_quarter))
            un_pos_quarter[quarter] += 1
            if quarter == 0:
                x_min_range = min_x
                x_max_range = (min_x + max_x)/2
                y_min_range = min_y
                y_max_range = (min_y + max_y)/2
            elif quarter == 1:
                x_min_range = min_x
                x_max_range = (min_x + max_x)/2
                y_min_range = (min_y + max_y)/2
                y_max_range = max_y
            elif quarter == 2:
                x_min_range = (min_x + max_x)/2
                x_max_range = max_x
                y_min_range = (min_y + max_y)/2
                y_max_range = max_y
            else:
                x_min_range = (min_x + max_x)/2
                x_max_range = max_x
                y_min_range = min_y
                y_max_range = (min_y + max_y)/2
            x = x_min_range + random()*(x_max_range-x_min_range)
            y = y_min_range + random()*(y_max_range-y_min_range)
            node.set_pos((x, y, 0))
        for node in nodes.values():
            for ni_key in self.graph.all_out_edges_of_node(node.get_key()).keys():
                ni = nodes[ni_key]
                curr_pos = (node.get_pos()[0], node.get_pos()[1])
                ni_pos = (ni.get_pos()[0], ni.get_pos()[1])
                coordsA = "data"
                coordsB = "data"
                con = ConnectionPatch(curr_pos, ni_pos, coordsA, coordsB,
                                      arrowstyle="-|>", shrinkA=5, shrinkB=5,
                                      mutation_scale=15, fc="w")
                ax.plot([curr_pos[0], ni_pos[0]], [curr_pos[1], ni_pos[1]], "o")
                ax.add_artist(con)
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        plt.title("Graph Plot - Ex3")
        plt.show()

    def __set_axis(self) -> list:
        nodes = self.graph.get_all_v()
        max_y = float('-inf')
        min_y = float('inf')
        max_x = float('-inf')
        min_x = float('inf')
        un_positioned = []
        for node in nodes.values():
            if node.get_pos() is None:
                un_positioned.append(node)
            else:
                x = node.get_pos()[0]
                y = node.get_pos()[1]
                curr_x = float(node.get_pos()[0])
                curr_y = float(node.get_pos()[1])
                max_x = max(max_x, curr_x)
                min_x = min(min_x, curr_x)
                max_y = max(max_y, curr_y)
                min_y = min(min_y, curr_y)
        if len(un_positioned) == len(nodes):
            min_x = min_y = 0
            max_x = max_y = int(len(nodes)*1.5)
        elif len(un_positioned)==len(nodes)-1:
            upper_range = lower_range = int(len(nodes)*1.5)//2
            min_x = min_x - lower_range
            min_y = min_y - lower_range
            max_x = max_x + upper_range
            max_y = max_y + upper_range

            if min_y < 0:
                max_y = max_y - min_y
                min_y = 0
            if min_x < 0:
                max_x = max_x - min_x
                min_x = 0
        else:
            if max_x == min_x:
                range_y = max_y - min_y
                max_x = max_x + range_y/2
                min_x = min_x - range_y/2
            elif max_y == min_y:
                range_x = max_x - min_x
                max_y = max_y + range_x/2
                min_y = min_y - range_x/2
            else:
                range_x = (max_x - min_x)/(len(nodes)-len(un_positioned))
                range_y = (max_y - min_y)/(len(nodes)-len(un_positioned))
                min_x = min_x - range_x
                min_y = min_y - range_y
                max_x = max_x + range_x
                max_y = max_y + range_y
        return [min_x, max_x, min_y, max_y, un_positioned]

    def __build_reversed(self) -> DiGraph():
        reversed = DiGraph()
        nodes = self.graph.get_all_v()
        for node in nodes.values():
            node_key = node.get_key()
            reversed.add_node(node_key)
            edges = self.graph.all_out_edges_of_node(node_key)
            for ni in self.graph.all_out_edges_of_node(node_key).keys():
                reversed.add_node(ni)
                reversed.add_edge(ni, node_key, edges[ni])
        self.reversed = reversed
