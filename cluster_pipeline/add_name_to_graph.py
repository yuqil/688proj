dic = {}
f1 = open("person.csv")
first = True
for line in f1:
    if first:
        first = False
        continue
    parts = line.rstrip().strip().split(',')
    id = parts[0]
    name = ' '.join(parts[1:])
    name = name.replace('&', '')
    name = name.replace('#', '')
    dic[id] = name

f2 = open("lcc-author-citation-graph-2010-2016.graphml")
f3 = open("lcc-author-citation-graph-2010-2016_with_name.graphml", "w")
for line in f2:
    if '<data key="v_name">' in line:
        id = line.split('>')[1].split('<')[0]
        assert(id in dic)
        line = line.replace(id, dic[id])
    f3.write(line)

print 'finish add_name_to_graph'
