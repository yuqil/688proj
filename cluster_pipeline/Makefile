all:
	python add_name_to_graph.py
	python get_new_graph_node_and_edge.py
	g++ -std=c++11 cluster.cpp -o cluster
	./cluster new_person.txt new_edge.txt 100
	python add_cluster_label.py
