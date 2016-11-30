from bs4 import BeautifulSoup
import urllib

url = "http://link.springer.com/article/10.1023/A:1020281327116"

def get_springer_keywords(url):
    soup = BeautifulSoup(urllib.urlopen(url).read())
    return [x.get_text() for x in soup.find_all("span", class_="Keyword")]


print get_springer_keywords(url)

