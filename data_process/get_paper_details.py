import requests
from bs4 import BeautifulSoup
import codecs

def extract_reviews(url):
    """
    Parse the title and abstract of icml 2016
    """
    path = "icml_abstracts.txt"
    file = codecs.open(path, 'w', encoding='utf8')

    if url != None:
        response = requests.get(url)
        root = BeautifulSoup(response.content, 'html.parser')
        papers = root.find_all("div", {"id" : "schedule"})[0].find_all("li")
        print len(papers)

        for paper in papers:
            title = paper.find("span", {"class" : "titlepaper"}).find("a").get_text()
            abstract = paper.find("div", {"class" : "abstract"}).get_text()
            file.write(title + "\n")
            file.write(abstract + "\n")
    file.close()
    print "end"

extract_reviews("http://icml.cc/2016/?page_id=1649")
