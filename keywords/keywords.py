from bs4 import BeautifulSoup
import urllib
import scholarly

url = "http://link.springer.com/article/10.1023/A:1020281327116"

def get_springer_keywords(url):
    soup = BeautifulSoup(urllib.urlopen(url).read())
    return [x.get_text() for x in soup.find_all("span", class_="Keyword")]


# print get_springer_keywords(url)


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

title = 'Face image retrieval by shape manipulation'
print get_url_from_title(title)


def get_all_urls(pub_file, out_file):
    fin = open(pub_file, "r")
    fout = open(out_file, "w")

    for line in fin:
        parts = line.strip().split('\t')
        out_list = list()
        title = parts[0]
        year = parts[1]
        out_list.append(title) # title
        out_list.append(get_url_from_title(title)) # url
        out_list.append(year) # year

        fout.write('\t'.join(out_list) + '\n')
        print out_list

    fin.close()
    fout.close()

get_all_urls('/Users/ynwang/Projects/688-team/688proj/keywords/inproc.txt', '/Users/ynwang/Projects/688-team/688proj/keywords/url.txt')
