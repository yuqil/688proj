import config
import pickle
from collections import Counter
import os
import pandas as pd
from Queue import Queue

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def build_ref_dict():
    ref_df = pd.read_csv(os.path.join(config.base_csv_dir, 'refs.csv'))
    ref_dict = dict()
    for _, row in ref_df.iterrows():
        pid = int(row['paper_id'])
        if pid not in ref_dict:
            ref_dict[pid] = list()
        ref_dict[pid].append(int(row['ref_id']))
    save_obj(ref_dict, 'ref_idx')


def graph_count(ref_idx, paper_id, niter=3):
    vertices = list()
    queue = Queue()
    queue.put(paper_id)
    for i in range(niter):
        n = queue.qsize()
        for j in range(n):
            pid = queue.get()
            try:
                citations = ref_idx[pid]
                for cite in citations:
                    queue.put(cite)
                    vertices.append(cite)
            except:
                continue

    return Counter(vertices)

# build_ref_dict()

def test():
    ref_idx = load_obj('ref_idx')
    print 'index loading done'
    # paper_df = pd.read_csv(os.path.join(config.base_csv_dir, 'paper.csv'))
    # title_dict = dict()
    # for index, row in paper_df.iterrows():
    #     title_dict[int(row['id'])] = row['title']
    # print 'paper loading done'

    pid = 93258
    cnt = graph_count(ref_idx, pid, 3)
    print cnt

test()