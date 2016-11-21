
file = open("author.txt")

coaurhors = {}
pre_paper = None
author_list = []

for line in file:
    tokens = line.split('\t')
    paper = tokens[1]
    author = tokens[0]

    if pre_paper == None or pre_paper == paper:
        pre_paper = paper
        author_list.append(author)
    else:
        author_list = list(set(author_list))
        coaurhors[pre_paper] = author_list
        pre_paper = paper
        author_list = []
        author_list.append(author)

author_list = list(set(author_list))
coaurhors[pre_paper] = author_list
file.close()

node_map = {}
author_map = open("author_node_map.txt", 'w')
edge_list = open("edge_list.txt", "w")

for paper, authors in coaurhors.iteritems():
    for author in authors:
        if author not in node_map:
            node_map[author] = str(len(node_map))

    for i in range(0, len(authors)):
        for j in range(i + 1, len(authors)):
            firstauthor = node_map[authors[i]]
            secondauthor = node_map[authors[j]]
            edge_list.write(firstauthor + "," + secondauthor + "\n")
edge_list.close()

for author, key in node_map.iteritems():
    author_map.write(key + "," + author + "\n")
author_map.close()
