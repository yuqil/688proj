all:
	python add_name_to_graph.py
	python get_new_graph_node_and_edge.py
	g++ -std=c++11 *.cpp -o cluster
	./cluster new_person.txt new_edge.txt
	python add_cluster_label.py

clean:
	rm lcc-author-citation-graph-2010-2016_final.graphml
	rm lcc-author-citation-graph-2010-2016_with_name.graphml
	rm new_edge.txt
	rm new_person.txt
	rm output.txt
	rm output_ml.txt
	rm cluster

