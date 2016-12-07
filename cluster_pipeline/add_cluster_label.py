dic = {}
f1 = open("output_ml.txt")
for line in f1:
    parts = line.rstrip().strip().split(',')
    id = parts[0]
    cluster = parts[1]
    dic[id] = cluster

f2 = open("lcc-author-citation-graph-2010-2016_with_name.graphml")
f3 = open("lcc-author-citation-graph-2010-2016_final.graphml", "w")
for line in f2:
    f3.write(line)
    if '<key id="v_id"' in line:
        f3.write('<key id="v_cluster" for="node" attr.name="cluster" attr.type="string"/>\n')
    if '<node id=' in line:
        id = line.split('"')[1]
        cluster = dic[id]
        f3.write('      <data key="v_cluster">' + cluster + '</data>\n')

print 'finish add_cluster_label'
