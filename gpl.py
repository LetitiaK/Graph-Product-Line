import unittest


class Base:

    # Created nested class Graph
    class Graph:
        # Define initialization
        def __init__(self, representation, directed, weight):
            self.directed = directed
            self.weight = weight

            # Differentiate between the EdgeList and the NeighbourList
            # representation
            if (representation is "EdgeList"):
                self.representation = Base.EdgeList(directed)
            else:
                self.representation = Base.NeighbourList(directed)

        def add(self, *args):
            ''' The method add takes a varibale number of arguments and checks
            whether the number of given arguments suits the given type of
            graph. This add function does not create an edge instance, but
            rather calls the add function for the respective representation '''
            # For an unweighted graph, 2 arguments are expected
            if((len(args) == 2) and (self.weight is False)):
                self.representation.add(args[0], args[1])
            # For a weighted graph, 3 arguments are expected and
            # the weight must be positive
            elif((len(args) == 3) and (self.weight is True) and
                    (args[2] >= 0)):
                self.representation.add(args[0], args[1], args[2])
            # If the type of the graph and the number of given arguments
            # doesn't match an error message is printed
            elif ((len(args) == 2) and (self.weight is True)):
            	print("""Error: This is a weighted graph,
                but the weight is missing.""")
            elif ((len(args) == 3) and (self.weight is False)):
            	print("""Error: This is an unweighted graph,
                but a weight was assigned.""")
            elif((len(args) == 3) and (self.weight is True) and (args[2] < 0)):
                print("Error: The weight is negative.")
            elif(len(args) < 2):
                print("Error: Not enough arguments.")
            else:
                print("Error: Too many arguments.")

        def getEdgeList(self):
            '''Method returns the Edgelist -
            required when DOT pretty printing is desired '''
            edges = self.representation.setEdgeList()
            return edges

        def getNeighbourList(self):
            '''Method returns the NeighbourList -
            required when DOT pretty printing is desired '''
            nodes = self.representation.setNeighbourList()
            return nodes

    # Nested class EdgeList
    class EdgeList:
        # Define initialization
        def __init__(self, directed):
            self.directed = directed
            self.edges = set()
            self.nodes = set()
            self.name = "EdgeList"

        # Define add function, which is used to create edge instances
        def add(self, *args):
            # Add a new edge to the edgelist without weights
            if (len(args) == 2):
                self.m = args[0]
                self.n = args[1]
                # Check whether the edge is directed
                if (self.directed is True):
                    # If the edge is directed only (m,n) needs to be checked
                    if((self.m, self.n) not in self.edges):
                        # If the edge does not already exists,
                        # create a new edge instance
                        edge = Base.Edge(self.m, self.n)
                        # Add the new edge instance to the edgelist
                        self.edges.add((edge.m, edge.n))
                        # Call the addNewNode function in order
                        # to add the nodes, if needed
                        Base.EdgeList.addNewNode(self, self.m)
                        Base.EdgeList.addNewNode(self, self.n)
                # If the edge is undirected, the constraints are different
                else:
                    # In case of undirected edges both (m,n) as well as (n,m)
                    # must be checked
                    if (((self.m, self.n) not in self.edges) and
                       (self.n, self.m) not in self.edges):
                        # If the edge does not yet exist,
                        # an edge instance is created
                        edge = Base.Edge(self.m, self.n)
                        # The edge instance is added to the edgelist
                        self.edges.add((edge.m, edge.n))
                        # Call the addNewNode function in order
                        # to add the nodes, if needed
                        Base.EdgeList.addNewNode(self, self.m)
                        Base.EdgeList.addNewNode(self, self.n)
            # Add a new edge to the edgelist with weights
            else:
                self.m = args[0]
                self.n = args[1]
                self.weight = args[2]
                # Check if directed
                if (self.directed is True):
                    if((self.m, self.n) not in self.edges):
                        edge = Base.Edge(self.m, self.n, self.weight)
                        self.edges.add((edge.m, edge.n, self.weight))
                        Base.EdgeList.addNewNode(self, self.m)
                        Base.EdgeList.addNewNode(self, self.n)
                # Undirected
                else:
                    if (((self.m, self.n) not in self.edges) and
                       (self.n, self.m) not in self.edges):
                        edge = Base.Edge(self.m, self.n, self.weight)
                        self.edges.add((edge.m, edge.n, self.weight))
                        Base.EdgeList.addNewNode(self, self.m)
                        Base.EdgeList.addNewNode(self, self.n)

        # Method addNewNode
        def addNewNode(self, node):
            self.node = node

            # Check whether the node is not yet in the nodes set
            # Only if the node does not already exist,
            # a node instance is created
            if (self.node not in self.nodes):
                # A node instance is created
                node = Base.Node(node)
                # The node is added to the nodes set
                self.nodes.add(node.node)

        # Method needed to get the Edgelist
        def setEdgeList(self):
            return self.edges

    # Create nested class NeighbourList
    class NeighbourList:

        # Initialization
        def __init__(self, directed):
            self.directed = directed
            # The neighbour list is a dictionary
            # In case of unweighted graphs the dictionary is built as follows:
            # Key = Node, Values = Neighbours as List
            # In case of weighted graphs the dictionary is built as follows:
            # Key = Node, Values = List of Tuples: First value of
            # Tuple = Neighbour, second value of Tuple = Weight
            self.nodes = dict()
            self.name = "NeighbourList"

        # Add method
        def add(self, *args):
            # Differentiate between directed and undirected graphs
            # TODO: Simplify using not
            # TODO: do you see a way to avoid redundancy between
            # directed & undirected?
            if (not self.directed):
                # Differentiate between unweighted and weighted graphs
                if (len(args) == 2):
                    self.node = args[0]
                    self.neighbour = args[1]
                    # Add a new node instance if needed
                    if(self.node not in self.nodes):
                        node = Base.Node(self.node)
                        self.nodes[node.node] = []
                    if(self.neighbour not in self.nodes):
                        neighbour = Base.Node(self.neighbour)
                        self.nodes[neighbour.node] = []

                    # Check the dictionary and add the neighbour
                    # (symmetrically)
                    for key, value in self.nodes.items():
                        # Check for node in the dictionary and check if the
                        # neighbour is already stored as value
                        if ((key is self.node) and
                           (self.neighbour not in value)):
                            # If needed create a new neighbour instance
                            neighbour =
                            Base.Neighbour(self.neighbour, self.node)
                            # Add the neighbour instance to the dictionary
                            self.nodes[key].append(neighbour.node)
                        # Same, but vice versa
                        if ((key is self.neighbour) and
                           (self.node not in value)):
                            neighbour = Base.Neighbour(self.node, self.neighbour)  # NOQA
                            self.nodes[key].append(neighbour.node)

                # Weighted undirected graphs
                else:
                    self.node = args[0]
                    self.neighbour = args[1]
                    self.weight = args[2]
                    if(self.node not in self.nodes):
                        node = Base.Node(self.node)
                        self.nodes[node.node] = []
                    if(self.neighbour not in self.nodes):
                        neighbour = Base.Node(self.neighbour)
                        self.nodes[neighbour.node] = []

                    for key, value in self.nodes.items():
                        if ((key is self.node) and
                           (self.neighbour not in value)):
                            neighbour = Base.Neighbour(self.neighbour, self.node, self.weight)  # NOQA
                            self.nodes[key].append((neighbour.node, neighbour.weight))  # NOQA
                        if ((key is self.neighbour) and
                           (self.node not in value)):
                            neighbour = Base.Neighbour(self.node, self.neighbour, self.weight)  # NOQA
                            self.nodes[key].append((neighbour.node, neighbour.weight))  # NOQA

            else:
                # In general, this is the same as for undirected,
                # unweighted graphs, with the one difference
                # that the neighbour is not added symetrically,
                # but just according to the arrow
                if (len(args) == 2):
                    self.node = args[0]
                    self.neighbour = args[1]
                    if(self.node not in self.nodes):
                        node = Base.Node(self.node)
                        self.nodes[node.node] = []
                    if(self.neighbour not in self.nodes):
                        neighbour = Base.Node(self.neighbour)
                        self.nodes[neighbour.node] = []

                    for key, value in self.nodes.items():
                        if ((key is self.node) and
                           (self.neighbour not in value)):
                            neighbour = Base.Neighbour(self.neighbour, self.node)  # NOQA
                            self.nodes[key].append(neighbour.node)

                else:
                    self.node = args[0]
                    self.neighbour = args[1]
                    self.weight = args[2]
                    if(self.node not in self.nodes):
                        node = Base.Node(self.node)
                        self.nodes[node.node] = []
                    if(self.neighbour not in self.nodes):
                        neighbour = Base.Node(self.neighbour)
                        self.nodes[neighbour.node] = []

                    # Iterate through the NeighbourList
                    for key, value in self.nodes.items():
                        if ((key is self.node) and
                           (self.neighbour not in value)):
                            neighbour = Base.Neighbour(self.neighbour, self.node, self.weight)  # NOQA
                            self.nodes[key].append((neighbour.node, neighbour.weight))  # NOQA

        # Method needed to get the Edgelist
        def setNeighbourList(self):
            return self.nodes

    # Create nested class Edge
    class Edge:
        def __init__(self, *args):
            if (len(args) == 2):
                self.m = args[0]
                self.n = args[1]
            else:
                self.m = args[0]
                self.n = args[1]
                self.weight = args[2]

    # Create nested class Node
    class Node:
        def __init__(self, node):
            self.node = node

    # Created nested class Neighbour
    class Neighbour:
        def __init__(self, *args):
            if(len(args) == 2):
                self.node = args[0]
                self.opposite = args[1]
            else:
                self.node = args[0]
                self.opposite = args[1]
                self.weight = args[2]

    # The class dotGraph is a subclass of Graph
    class DotGraph(Graph):

        # Define method dotPrint, which takes no arguments
        def dotPrint(self):
            if(self.representation.name is "EdgeList"):
                edges = Base.Graph.getEdgeList(self)
                # Sort the edges in order to define a test case later on
                edges = sorted(edges)
                # TODO: Simplify using 'not'
                if(not self.weight):
                    # Get the Edgelist
                    # Check whether the graph is directed or undirected
                    # Undirected Graphs
                    if(self.directed is False):
                        # Define the initial DOT String
                        # Using node [label=""] in order to disable
                        # labels in the output
                        dotString = 'graph G {node [label=""] '
                        # Concatenate the edges to the dotString
                        for i in edges:
                            dotString = dotString + str(i[0]) + " -- " +
                            str(i[1]) + " "
                        dotString = dotString + '}'
                        return(dotString)
                    # Directed Graphs
                    else:
                        dotString = 'digraph G {node [label=""] '
                        for i in edges:
                            dotString = dotString + str(i[0]) +
                            " -> " + str(i[1]) + " "
                        dotString = dotString + '}'
                        return(dotString)
                else:
                    if(self.directed is False):
                        dotString = 'graph G {node [label=""] '
                        for i in edges:
                            dotString = dotString + str(i[0]) + " -- " +
                            str(i[1]) + "[label=" + str(i[2]) + "]" + " "
                        dotString = dotString + '}'
                        # Return the dotString
                        return(dotString)
                    else:
                        dotString = 'digraph G {node [label=""] '
                        for i in edges:
                            dotString = dotString + str(i[0]) + " -> " +
                            str(i[1]) + "[label=" + str(i[2]) + "]" + " "
                        dotString = dotString + '}'
                        # Return the dotString
                        return(dotString)

            # DOT Pretty Printing with neighbour list representation
            else:
                nodes = Base.Graph.getNeighbourList(self)
                # Unweighted graphs
                if(self.weight is False):
                    # Undirected Graphs
                    if(self.directed is False):
                        dotString = 'graph G {node [label=""] '
                        # Iterate through the NeighbourList
                        for key, value in nodes.items():
                            # Iterate through the value list
                            for i in range(0, len(value)):
                                # Check if the counterpart of the edge
                                # already exists
                                # Important for undirected graphs, because of
                                # the symetrically added neighbours
                                # one would otherwise receive double edges
                                if ((str(value[i]) + " -- " + str(key)) not in dotString):  # NOQA
                                    dotString = dotString + str(key) + " -- " + str(value[i]) + " "  # NOQA
                        dotString = dotString + '}'
                        return(dotString)
                    # Directed Graphs
                    else:
                        dotString = 'digraph G {node [label=""] '
                        for key, value in nodes.items():
                            for i in range(0, len(value)):
                                dotString = dotString + str(key) + " -> " +
                                str(value[i]) + " "
                        dotString = dotString + '}'
                        return(dotString)

                # Weighted Graphs
                else:
                    # Undirected Graphs
                    if(self.directed is False):
                        dotString = 'graph G {node [label=""] '
                        for key, value in nodes.items():
                            for i in range(0, len(value)):
                                # Check for the first value of the tuple,
                                # i.e. the neighbour
                                if ((str(value[i][0]) + " -- " + str(key)) not in dotString):  # NOQA
                                    # Add the weight as label
                                    # (weight = second value of tuple)
                                    dotString = dotString + str(key) + " -- " +
                                    str(value[i][0]) + "[label=" + str(value[i][1]) + "]" + " "  # NOQA
                        dotString = dotString + '}'
                        return(dotString)
                    else:
                        dotString = 'digraph G {node [label=""] '
                        for key, value in nodes.items():
                            for i in range(0, len(value)):
                                dotString = dotString + str(key) + " -> " +
                                str(value[i][0]) + "[label=" + str(value[i][1]) + "]" + " "  # NOQA
                        dotString = dotString + '}'
                        return(dotString)


class Test(unittest.TestCase):

    def test_acceptance(self):
        # Acceptance tests
        self.assertEqual(hasattr(Base, "Graph") and
                         isinstance(Base.Graph, type), True)
        self.assertEqual(hasattr(Base, "Edge") and
                         isinstance(Base.Edge, type), True)
        self.assertEqual(hasattr(Base, "Node") and
                         isinstance(Base.Node, type), True)
        self.assertEqual(hasattr(Base.Graph, "add") and
                         callable(Base.Graph.add), True)

    # Homework 1 - Test 1 - Adjusted
    def test_nodot(self):
        gpl1 = Base.Graph("EdgeList", False, False)
        gpl1.add(1, 2)
        gpl1.add(1, 3)
        gpl1.add(1, 4)
        gpl1.add(1, 5)
        gpl1.add(5, 6)
        gpl1.add(5, 7)
        gpl1.add(5, 8)
        edgelist = {(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (5, 7), (5, 8)}
        self.assertEqual(gpl1.getEdgeList(), edgelist)

    # Homework 1 - Test 2 - Adjusted
    def test_dot(self):
        gpl2 = Base.DotGraph("EdgeList", False, False)
        gpl2.add(1, 2)
        gpl2.add(1, 3)
        gpl2.add(1, 4)
        gpl2.add(1, 5)
        gpl2.add(5, 6)
        gpl2.add(5, 7)
        gpl2.add(5, 8)
        edgelist = {(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (5, 7), (5, 8)}
        self.assertEqual(gpl2.getEdgeList(), edgelist)

    # Homework 1 - Test 3 - Adjusted
    def test_dotOutput(self):
        gpl3 = Base.DotGraph("EdgeList", False, False)
        gpl3.add(1, 2)
        gpl3.add(1, 3)
        gpl3.add(1, 4)
        gpl3.add(1, 5)
        gpl3.add(5, 6)
        gpl3.add(5, 7)
        gpl3.add(5, 8)
        dotString = gpl3.dotPrint()
        comparisonString = '''graph G {node [label=""] 1 -- 2 1 -- 3 1 -- 4
        1 -- 5 5 -- 6 5 -- 7 5 -- 8 }'''
        self.assertEqual(dotString, comparisonString)

    # Homework 2 - Test 1
    def test_nodot2(self):
        gpl4 = Base.DotGraph("EdgeList", False, True)
        gpl4.add(1, 2, 1)
        gpl4.add(1, 3, 4)
        gpl4.add(1, 4, 5)
        gpl4.add(1, 5, 1)
        gpl4.add(5, 6, 10)
        gpl4.add(5, 7, 2)
        gpl4.add(5, 8, 7)
        dotString = gpl4.dotPrint()
        comparisonString = '''graph G {node [label=""] 1 -- 2[label=1]
        1 -- 3[label=4] 1 -- 4[label=5] 1 -- 5[label=1] 5 -- 6[label=10]
        5 -- 7[label=2] 5 -- 8[label=7] }'''
        self.assertEqual(dotString, comparisonString)

    # Homework 2 - Test 2
    def test_nodot2(self):
        gpl5 = Base.DotGraph("NeighbourList", True, True)
        gpl5.add(1, 2, 1)
        gpl5.add(2, 3, 4)
        gpl5.add(2, 4, 5)
        gpl5.add(2, 5, 1)
        gpl5.add(6, 5, 10)
        gpl5.add(5, 7, 2)
        gpl5.add(5, 8, 7)
        dotString = gpl5.dotPrint()
        comparisonString = '''digraph G {node [label=""] 1 -> 2
        [label=1] 2 -> 3[label=4] 2 -> 4[label=5] 2 -> 5[label=1]
        5 -> 7[label=2] 5 -> 8[label=7] 6 -> 5[label=10] }'''
        self.assertEqual(dotString, comparisonString)


if __name__ == '__main__':
    unittest.main()
