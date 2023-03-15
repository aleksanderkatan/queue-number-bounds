from algorithms.encodings.abstract_sat_encoder import AbstractSatEncoder
from pysat.formula import IDPool
from pysat.formula import CNF
from pysat.card import CardEnc
import networkx as nx


# implies([p_1, p_2, p_3], q) returns a clause equivalent to
# p_1 && p_2 && p_3 => q
def _implies(p, q):
    return [-p_i for p_i in p] + [q]


# tests whether qn is viable
class QnSatEncoder(AbstractSatEncoder):
    def __init__(self):
        self.g = None
        self.qn = None
        self.pool = None
        self.v = {}

    # has to be multiple use
    def initialize_with_graph(self, graph: nx.Graph, qn):
        self.g = graph
        self.qn = qn
        self.pool = IDPool()
        self.v = {}
        self._initialize_variables()

    def _initialize_variables(self):
        n = len(self.g.nodes)

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                self.v["o", i, j] = self.pool.id(("o", i, j))
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                for k in range(1, self.qn+2):
                    self.v["r", i, j, k] = self.pool.id(("r", i, j, k))

    # there is a k-rainbow between v_i and v_j
    def r(self, i, j, k):
        if i < j:
            return self.v["r", i, j, k]
        return self.v["r", j, i, k]

    # v_i << v_j
    def o(self, i, j):
        if i < j:
            return self.v["o", i, j]
        return -self.v["o", j, i]

    def encode(self):
        formula = CNF()
        n = len(self.g.nodes)

        # ordering
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                for k in range(1, n + 1):
                    if len({i, j, k}) < 3:
                        continue
                    clause = _implies(
                        [self.o(i, j), self.o(j, k)],
                        self.o(i, k)
                    )
                    formula.append(clause)

        # 1-rainbows
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if len({i, j}) < 2:
                    continue
                clause = _implies(
                    [self.o(i, j)],
                    self.r(i, j, 1)
                )
                formula.append(clause)

        # bigger rainbows
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                for k in range(1, n + 1):
                    for l in range(1, n + 1):
                        if len({i, j, k, l}) < 4:
                            continue
                        if not (self.g.has_edge(i, l) and self.g.has_edge(j, k)):
                            continue
                        for q in range(1, self.qn+1):
                            clause = _implies(
                                [self.o(i, j), self.o(j, k), self.o(k, l), self.r(j, k, q)],
                                self.r(i, l, q+1)
                            )
                            formula.append(clause)

        # actual qn is smaller than given value
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if len({i, j}) < 2:
                    continue
                formula.append([-self.r(i, j, self.qn+1)])

        return formula

    def decode(self, model: list[int]):
        n = len(self.g.nodes)

        def value_of(variable_index):
            # variable_index might be negative
            # variables start with index 1
            if variable_index > 0:
                return model[variable_index - 1] > 0
            return model[-variable_index - 1] < 0

        # skip last element
        order = [0] * n
        for i in range(1, n+1):
            bigger_than_i = [j for j in range(1, n + 1) if (j != i and value_of(self.o(i, j)))]
            order[n - len(bigger_than_i) - 1] = i

        return order

