import multiprocessing
import threading
import time
import scholarly

def task(id, startnumber, pub_file, out_file):
    print id, " start!"
    fin = open(pub_file, "r")
    fout = open(out_file, "w")

    for i in xrange(0, startnumber):
        line = fin.readline()

    for i in xrange(0, 10000):
        line = fin.readline()
        parts = line.strip().split('\t')
        out_list = list()
        title = parts[0]
        year = parts[1]

        url = get_url_from_title(title)
        if url is None:
            continue
        out_list.append(title)  # title
        out_list.append(url)  # url
        out_list.append(year)  # year

        fout.write('\t'.join(out_list) + '\n')
        print out_list

    fin.close()
    fout.close()


def get_url_from_title(title):
    pub_query = scholarly.search_pubs_query(title)
    retval = None

    while True:
        try:
            pub = next(pub_query)
            pub_url = pub.bib['url']
            ext_idx = pub_url.rfind('.pdf')
            if ext_idx >= 0 and ext_idx + 4 == len(pub_url):
                continue
            retval = pub_url
            break
        except StopIteration:
            break

    return retval


def get_all_urls(pub_file, out_file):
    fin = open(pub_file, "r")
    fout = open(out_file, "w")

    for line in fin:
        parts = line.strip().split('\t')
        out_list = list()
        title = parts[0]
        year = parts[1]

        url = get_url_from_title(title)
        if url is None:
            continue
        out_list.append(title) # title
        out_list.append(url) # url
        out_list.append(year) # year

        fout.write('\t'.join(out_list) + '\n')
        print out_list

    fin.close()
    fout.close()


print "multiple process start"
jobs = []
startnum = 0
inputpath = "/Users/yuqil/Desktop/16fall/15688/final project/code/688proj/parse_dblp/inproc.txt"
for i in xrange(0, 20):
    p = multiprocessing.Process(target=task, args=(i, startnum, inputpath, str(i) + ".txt"))
    startnum += 10000
    jobs.append(p)
    p.start()
