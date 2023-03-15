from algorithms.encodings.qn_sat_encoder import QnSatEncoder
from algorithms.bottom_up_sat_checker import process_bottom_up
from algorithms.other.helpers import read_graph
import networkx as nx
import matplotlib.pyplot as plt
import os

INSTANCES_PATH = 'instances'


def draw_graph(g: nx.Graph):
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_size=256, node_color='green')
    nx.draw_networkx_edges(g, pos, edgelist=g.edges(), edge_color='black')
    nx.draw_networkx_labels(g, pos)
    plt.show()



if __name__ == '__main__':
    file_names = os.listdir(INSTANCES_PATH)
    expected_results = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    for file_name, expected_result in zip(sorted(file_names), expected_results):
        file_path = os.path.join(INSTANCES_PATH, file_name)
        graph = read_graph(file_path)

        qn, sequence = process_bottom_up(graph, QnSatEncoder(), "cadical")
        print(f"{file_path}: {expected_result}/{qn}")
        print(f"Sequence: {sequence}")
        print()

        draw_graph(graph)
