## README
## Authors
Mayan Bashan & Yuval Moshe 

## Background <br />

This project is a part of an OOP class in Python which is divided into 2 main parts:<br />

### <ins>First part</ins> - 
In this part we implemented  a directed weighted graph with the following classes: <br />
* NodeData - represents the a node that is a vertex in a graph a directed weighted graph. <br />
* DiGraph - implements the GraphInterface interface, which represents the graph itself. <br />
* GraphAlgo - implements the GraphAlgoInterface interface, which allows performing algorithmic queries on a specific graph. <br />
The graph was realized by using dictionary structure, and the operations were written by realizing Dijkstra algorithm (please see explanation in the algorithm itself). <br />
### <ins>Second part</ins> -
In this part we compared our performance, to [NetworkX](https://networkx.org/) performance (*NetworkX is a python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks).

   
## Project Requirments
- Python 3+ compiler | [Download Python ](https://www.python.org/downloads/)
- Networkx grpahs python package  | [View Networkx Install Manual ](https://networkx.org/documentation/stable/install.html)
- matplotlib python package  | [View matplotlib Install Guide ](https://matplotlib.org/3.3.3/users/installing.html)
- Python IDE (Pycharm, Visual Studio Code, etc') | [Pycharm Download](https://www.jetbrains.com/pycharm/download/) / [Visual Studio Code Download](https://code.visualstudio.com/download)

## How to run
In order to gain more specific imformation on how to run this project please view the attached wiki pages:
- [How to run](https://github.com/MayanBashan/Ex3/wiki/How-To-Run-Weighted-&-Directed-Graph)

## Definitions
 * *directed graph - a set of nodes that are connected together, where all the edges are directed from one vertex to another*
 * *weighted graph - edges of the graph are holding a weight*
  
## Example:
 
![](data/dw_graph_image.png)
 
**This graph contains 6 nodes and 9 edges.**
- connected_component() with 1 as input will return the list [0,1,2,3,4] (we can get from each node in the list to each other node from the list).<br />
- connected_components() function will return [[5],[0,1,2,3,4]] - no path from node 5 to any other node, and if we take any 2 nodes from [0,1,2,3,4], <br />
  there will be a path from first node to second node, and a path from second node to first node.<br />
- shortest_path() method between node 0 to node 5 will return a dict - {**14** , [0,1,3,4,5]} (14=4+2+2+6).<br />
Do notice that the shortest path depends on the sum of the weights of the edges between the 2 nodes
and not on the sum of the nodes between 2 nodes.

###### For more information please check the [Wiki](https://github.com/MayanBashan/Ex3/wiki)
