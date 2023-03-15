## An algorithm for determining the ~~twin-width~~ queue number of a graph

To install missing dependencies:

`
pip install networkx;
pip install ortools;
pip install python-sat
`

(Do not trust PyCharm to install *pysat* it for you, it installs *pysat: Python Satellite Data Analysis Toolkit*)

`
for i in {1..5}; do ./plantri53/plantri -pm5va $i planar_graphs/graphs_"$i".txt; done
`

^ shell for generating planar graphs
