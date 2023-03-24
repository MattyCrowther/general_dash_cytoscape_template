from builders.abstract_view import AbstractViewBuilder
from graph import Graph
class FullViewBuilder(AbstractViewBuilder):
    def __init__(self,graph):
        super().__init__(graph)

    def _subgraph(self, edges=[], nodes=[],new_graph=None):
        return Graph(super()._subgraph(edges,nodes,new_graph))
        
    def build(self):
        edges = self._graph.edges()
        return self._subgraph(edges)