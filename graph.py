import re
import networkx as nx
from graph_objects.node import Node
from graph_objects.edge import Edge

class Graph:
    def __init__(self, graph=None): 
        self._graph = graph if graph is not None else nx.MultiDiGraph()

    def resolve_node(func):
        def inner(self,n=None):
            if isinstance(n,Node):
                n = n.id
            return func(self,n)
        return inner
        
    def __len__(self):
        return len(self._graph)

    def __eq__(self, obj):
        if isinstance(obj, self.__class__):
            return nx.is_isomorphic(self._graph, obj._graph)
        if isinstance(obj, nx.MultiDiGraph):
            return nx.is_isomorphic(self._graph, obj)
        return False

    def __iter__(self):
        for n in self._graph.nodes:
            yield n

    def _node(self,labels,id=None,properties=None):
        if properties is None:
            props = {}
        else:
            props = properties
        return Node(labels,id=id,**props)
    
    def _edge(self,n,v,e,properties=None):
        if properties is None:
            props = {}
        else:
            props = properties
        return Edge(n,v,e,**props)

    def nodes(self):
        for n,data in self._graph.nodes(data=True):
            props = data.copy()
            labels = props["key"]
            del props["key"]
            yield self._node(labels,id=n,properties=props)

    @resolve_node
    def edges(self,n=None):
        for n,v,e,d in self._graph.edges(n,keys=True,data=True):
            props = self._graph.nodes[n].copy()
            labels = props["key"]
            del props["key"]
            n = self._node(labels,id=n,properties=props)

            props = self._graph.nodes[v].copy()
            labels = props["key"]
            del props["key"]
            v = self._node(labels,id=v,properties=props)
            yield self._edge(n,v,e,properties=d)

    def get_node(self,n=None):
        if n is None:
            return list(self.nodes())
        data = self._graph.nodes[n]
        props = data.copy()
        labels = props["key"]
        del props["key"]
        return self._node(labels,id=n,properties=props)

    @resolve_node
    def in_edges(self, node=None):
        for n,v,e,d in self._graph.in_edges(node,keys=True,data=True):
            props = self._graph.nodes[n].copy()
            labels = props["key"]
            del props["key"]
            n = self._node(labels,id=n,properties=props)

            props = self._graph.nodes[v].copy()
            labels = props["key"]
            del props["key"]
            v = self._node(labels,id=v,properties=props)
            yield self._edge(n,v,e,properties=d)

    @resolve_node
    def out_edges(self, node=None):
        for n,v,e,d in self._graph.out_edges(node,keys=True,data=True):
            props = self._graph.nodes[n].copy()
            labels = props["key"]
            del props["key"]
            n = self._node(labels,id=n,properties=props)

            props = self._graph.nodes[v].copy()
            labels = props["key"]
            del props["key"]
            v = self._node(labels,id=v,properties=props)
            yield self._edge(n,v,e,properties=d)



    def has_edge(self,edge):
        return self._graph.has_edge(edge.n.id,edge.v.id,key=edge.get_type())
    
    def add_edge(self, edge):
        self._graph.add_edge(edge.n.id,edge.v.id,key=edge.get_type(),**edge.get_properties())

    def add_node(self, node):
        self._graph.add_node(node.id,key=node.get_key(),type=node.get_type(),**node.get_properties())

    def remove_edge(self, edge):
        self._graph.remove_edge(edge.n.id, edge.v.id, edge.get_type())

    def remove_node(self, node):
        self._graph.remove_node(node)

    def merge_nodes(self, subject, nodes):
        if not isinstance(subject,Node):
            props = self._graph.nodes[subject].copy()
            labels = props["key"]
            del props["key"]
            subject = self._node(labels,id=subject,properties=props)
        for node in nodes:
            if isinstance(node,Node):
                node = node.id
            in_edges = list(self.in_edges(node))
            out_edges = list(self.out_edges(node))
            for edge in in_edges:
                self.remove_edge(edge)
                if edge.n != subject:
                    self.add_edge(self._edge(edge.n, subject, edge.get_type(), properties=edge.get_properties()))
            for edge in out_edges:
                self.remove_edge(edge)
                if edge.v != subject:
                    self.add_edge(self._edge(subject,edge.v, edge.get_type(), properties=edge.get_properties()))
            self.remove_node(node)

            
    @resolve_node
    def degree(self, node):
        return self._graph.degree(node)

    @resolve_node
    def bfs(self, source):
        for n,v in nx.bfs_tree(self._graph, source).edges():
            props = self._graph.nodes[n].copy()
            labels = props["key"]
            del props["key"]
            n = self._node(labels,id=n,**props)

            props = self._graph.nodes[v].copy()
            labels = props["key"]
            del props["key"]
            v = self._node(labels,id=v,**props)
            yield n,v


    @resolve_node
    def dfs(self, source):
        for n,v,e,k in nx.dfs_tree(self._graph, source).edges(keys=True,data=True):
            yield self._edge(n,v,e,**k)

    @resolve_node
    def is_isolate(self, node):
        return nx.is_isolate(self._graph, node)
    
    def node_connectivity(self):
        return nx.node_connectivity(self._graph)

    def degree_assortativity_coefficient(self):
        return nx.degree_assortativity_coefficient(self._graph)

    def triangles(self):
        g = nx.Graph(self._graph)
        return len(nx.triangles(g))

    def transitivity(self):
        g = nx.Graph(self._graph)
        return nx.transitivity(g)

    def average_clustering(self):
        g = nx.Graph(self._graph)
        return nx.average_clustering(g)

    def is_at_free(self):
        g = nx.Graph(self._graph)
        return nx.is_at_free(g)

    def is_bipartite(self):
        g = nx.Graph(self._graph)
        return nx.is_bipartite(g)

    def has_bridges(self):
        g = nx.Graph(self._graph)
        return nx.has_bridges(g)

    def is_chordal(self):
        g = nx.Graph(self._graph)
        return nx.is_chordal(g)

    def graph_number_of_cliques(self):
        g = nx.Graph(self._graph)
        return nx.graph_number_of_cliques(g)

    def is_strongly_connected(self):
        return nx.is_strongly_connected(self._graph)

    def number_strongly_connected_components(self):
        return nx.number_strongly_connected_components(self._graph)

    def is_weakly_connected(self):
        return nx.is_weakly_connected(self._graph)

    def number_weakly_connected_components(self):
        return nx.number_weakly_connected_components(self._graph)

    def is_attracting_component(self):
        return nx.is_attracting_component(self._graph)

    def number_attracting_components(self):
        return nx.number_attracting_components(self._graph)

    def diameter(self):
        try:
            return nx.diameter(self._graph)
        except nx.NetworkXError:
            return -1

    def radius(self):
        try:
            return nx.radius(self._graph)
        except nx.NetworkXError:
            return -1

    def is_eulerian(self):
        return nx.is_eulerian(self._graph)

    def is_semieulerian(self):
        return nx.is_semieulerian(self._graph)

    def is_aperiodic(self):
        return nx.is_aperiodic(self._graph)

    def is_biconnected(self):
        g = nx.Graph(self._graph)
        return nx.is_biconnected(g)

    def is_tree(self):
        return nx.is_tree(self._graph)

    def is_forest(self):
        return nx.is_forest(self._graph)

    def is_arborescence(self):
        return nx.is_arborescence(self._graph)

    def is_branching(self):
        return nx.is_branching(self._graph)

    def pagerank(self):
        g = nx.Graph(self._graph)
        return nx.pagerank(g)

    def degree_centrality(self):
        return nx.degree_centrality(self._graph)

    def closeness_centrality(self):
        return nx.closeness_centrality(self._graph)

    def betweenness_centrality(self):
        g = nx.Graph(self._graph)
        return nx.betweenness_centrality(g)

    def number_of_cliques(self):
        g = nx.Graph(self._graph)
        return nx.number_of_cliques(g)

    def clustering(self):
        g = nx.Graph(self._graph)
        return nx.clustering(g)

    def square_clustering(self):
        return nx.square_clustering(self._graph)

    def _get_name(self, subject):
        split_subject = self._split(subject)
        if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
            return split_subject[-2]
        elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
            return split_subject[-2]
        else:
            return split_subject[-1]

    def _node_from_attr(self, attribute,generator):
        nodes = []
        for n, data in self.generator():
            if attribute in data.values():
                labels = data["key"].copy()
                del data["key"]
                nodes.append(self._node(labels,id=n,properties=data))
        if nodes == []:
            raise ValueError("Unable to find.")
        return nodes

    def _split(self, uri):
        return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
