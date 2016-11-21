f1 = open("final.graphml")
f2 = open("new_person.txt", "w")
f3 = open("new_edge.txt", "w")
past_line = ''
for line in f1:
    if '<data key="v_name">' in line:
        id = past_line.split('"')[1]
        name = line.split('>')[1].split('<')[0]
        f2.write(id + ',' + name + '\n')
    if '<edge source="' in line:
        id1 = line.split('"')[1]
        id2 = line.split('"')[3]
        f3.write(id1 + ' ' + id2 + '\n')
    past_line = line

print 'finish'
