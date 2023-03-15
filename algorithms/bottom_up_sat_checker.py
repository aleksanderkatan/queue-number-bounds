import networkx as nx
from algorithms.encodings.abstract_sat_encoder import AbstractSatEncoder
from pysat.solvers import Solver


def process_bottom_up(graph: nx.Graph, encoder: AbstractSatEncoder, solver_name):
    for i in range(1, 10):
        # is qn <= i?
        encoder.initialize_with_graph(graph, i)
        formula = encoder.encode()
        with Solver(bootstrap_with=formula, name=solver_name) as solver:
            if solver.solve():
                sequence = encoder.decode(solver.get_model())
                return i, sequence
    raise RuntimeError("Qn not found")
