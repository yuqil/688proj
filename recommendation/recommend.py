import title_similarity
import ref_score
import similarity
import operator

class recommendation:
    def __init__(self):
        # set up citation reference score index
        self.ref_dict = ref_score.load_ref_dict()
        print 'index loading done'

        # set up title bigram feature
        self.bigram_dict = title_similarity.load_bigram_dict()
        print 'bigram load done'

        self.paper_dict = title_similarity.load_paper_dict()
        self.paper_inv_dict = title_similarity.load_paper_inv_dict()
        print 'paper load done'

        # set up abstract similarity feature
        self.simi_eva = similarity.abstract_similarity()
        print "abstract index done"


    def get(self, paper_title):
        if paper_title not in self.paper_inv_dict:
            return list()
        pid = self.paper_inv_dict[paper_title]

        title = self.paper_dict[pid]['title']
        # print title + "\n"
        abstract = self.paper_dict[pid]['abstract']
        # print abstract + "\n"

        # calculate title bigram feature
        idx_list = title_similarity.bigram_search(self.bigram_dict, title)
        # for idx in idx_list:
        #     # title_list.append(title_dict[idx])
        #     print idx_list[idx], self.paper_dict[idx]['title']

        # calculate citation feature
        cnt = ref_score.graph_count(self.ref_dict, pid, 3)
        # print cnt

        # calculate prior
        candidates = {}
        for k, v in idx_list.iteritems():
            if k in candidates:
                candidates[k] += v
            else:
                candidates[k] = v

        for k, v in cnt.iteritems():
            if k in candidates:
                candidates[k] += v
            else:
                candidates[k] = v

        # calculate total score
        for id, prior in candidates.iteritems():
            if id in self.paper_dict and type(self.paper_dict[id]['abstract']) == str:
                score = prior * self.simi_eva.getScore(abstract1=abstract, abstract2=self.paper_dict[id]['abstract'])
            else:
                score = prior * 0.5
            candidates[id] = score

        sort_score = sorted(candidates.items(), key=operator.itemgetter(1), reverse=True)
        # print sort_score

        retval = list()
        for item in sort_score:
            try:
                title = self.paper_dict[item[0]]['title']
                retval.append(title)
                # print title + " ", item[1]
            except KeyError:
                continue

        return retval[1:6]

re = recommendation()
print re.get("New unsupervised clustering algorithm for large datasets")

