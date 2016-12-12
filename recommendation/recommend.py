import title_similarity
import ref_score
import similarity
import operator

# set up citation reference score index
ref_dict = ref_score.load_ref_dict()
print 'index loading done'

# set up title bigram feature
bigram_dict = title_similarity.load_bigram_dict()
print 'bigram load done'
paper_dict = title_similarity.load_paper_dict()
print 'paper load done'

# set up abstract similarity feature
simi_eva = similarity.abstract_similarity()
print "abstract index done"

pid = 296375
title = paper_dict[pid]['title']
print title + "\n"
abstract = paper_dict[pid]['abstract']
print abstract + "\n"

# calculate title bigram feature
idx_list = title_similarity.bigram_search(bigram_dict, title)
for idx in idx_list:
    # title_list.append(title_dict[idx])
    print idx_list[idx], paper_dict[idx]['title']

# calculate citation feature
cnt = ref_score.graph_count(ref_dict, pid, 3)
print cnt

# calculate prior
candidates = {}
for k,v in idx_list.iteritems():
    if k in candidates:
        candidates[k] += v
    else:
        candidates[k] = v

for k,v in cnt.iteritems():
    if k in candidates:
        candidates[k] += v
    else:
        candidates[k] = v

# calculate total score
for id,prior in candidates.iteritems():
    if id in paper_dict and type(paper_dict[id]['abstract']) == str:
        score = prior * simi_eva.getScore(abstract1=abstract, abstract2=paper_dict[id]['abstract'])
    else:
        score = prior * 0.5
    candidates[id] = score

sort_score = sorted(candidates.items(), key=operator.itemgetter(1), reverse=True)
print sort_score

for item in sort_score:
    try:
        title = paper_dict[item[0]]['title']
        print title + " ", item[1]
    except KeyError:
        continue
