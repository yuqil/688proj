from nltk.corpus import stopwords
import sys
from collections import Counter
# sys.path.insert(0, '../pipeline/')

import config
import os
import pandas as pd
import pickle


def bigram_add(bigram_dict, key, value):
    if key not in bigram_dict:
        bigram_dict[key] = set()
    bigram_dict[key].add(value)


def bigram_index(titles):
    """ Build the bigram index from the vocabulary words
    Inputs:
        words_dict(dict): The vocabulary words
    Outputs:
        dict: A python dictionary with the key of str, value of set of str
    """
    bigram = dict()

    for key, title in titles.iteritems():
        # filter stopwords
        # print key, title
        stop_words = set(stopwords.words('english'))
        try:
            words = [w.lower() for w in title.split(' ') if w not in stop_words]

            if len(words) < 2:
                bigram_add(bigram, words[0], key)
                continue
            for i in range(len(words) - 1):
                bi = words[i: i + 2]
                bigram_add(bigram, ' '.join(bi), key)
        except:
            print 'exception:', key, title
            continue
    return bigram


def bigram_search(bigram_dict, title):
    """ Vague search the query word in the bigram index
    Inputs:
        bigram_dict(dict): The bigram index
        word(str): The query word
    Outputs:
        list: A list of potential matching vocabulary
    """
    stop_words = set(stopwords.words('english'))
    words = [w.lower() for w in title.split(' ') if w not in stop_words]

    bi_list = list()
    for i in range(len(words) - 1):
        bi = ' '.join(words[i: i + 2])
        if bi in bigram_dict:
            bi_list += list(bigram_dict[bi])
    bi_cnt = Counter(bi_list)
    return [w for w in bi_cnt if bi_cnt[w] >= 2]


def build_bigram_index():
    paper_df = pd.read_csv(os.path.join(config.base_csv_dir, 'paper.csv'))
    title_dict = dict()
    for index, row in paper_df.iterrows():
        title_dict[int(row['id'])] = row['title']

    print type(title_dict)
    print title_dict.keys()[0], title_dict[title_dict.keys()[0]]

    return bigram_index(title_dict)


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def test():
    paper_df = pd.read_csv(os.path.join(config.base_csv_dir, 'paper.csv'))
    title_dict = dict()
    for index, row in paper_df.iterrows():
        title_dict[int(row['id'])] = row['title']
    bigram_dict = load_obj('bigram_idx')

    idx_list = bigram_search(bigram_dict, 'Novel approach on object recognition based on convolutional neural network')
    # title_list = list()

    for idx in idx_list:
        # title_list.append(title_dict[idx])
        print title_dict[idx]




# bigram_dict = build_bigram_index()
# save_obj(bigram_dict, 'bigram_idx')
# print bigram_search(bigram_dict, 'Novel approach on object recognition based on convolutional neural network')
#

test()
