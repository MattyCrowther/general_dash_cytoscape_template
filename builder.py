from graph import Graph 
from builders.full import FullViewBuilder

class Builder:
    def __init__(self,graph=None):
        if graph is None:
            self._graph = Graph()
        else:
            self._graph = graph
        self.view = Graph()
        self._view_builder = FullViewBuilder(self._graph)
    
    def set_graph(self,graph):
        self._graph = graph

    def build(self,*args,**kwargs):
        self.view = self._view_builder.build(*args,**kwargs)
        
    def set_full_view(self):
        self._view_builder = FullViewBuilder(self._graph)

    def v_nodes(self):
        return self.view.nodes()

    def v_edges(self,n=None):
        return self.view.edges(n)

    def in_edges(self, n=None):
        return self.view.in_edges(n)

    def out_edges(self, n=None):
        return self.view.out_edges(n)