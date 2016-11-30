from bs4 import BeautifulSoup
import urllib
import requests
import json
url = "http://ieeexplore.ieee.org/document/855874/?arnumber=855874"
url1 = "http://ieeexplore.ieee.org/document/7750882/"

def get_springer_keywords(url):
    response = requests.get(url)
    file = open("tmp.html", "wb")
    file.write(response.content)
    file.close()
    for line in response.content.split("\n"):
        line = line.rstrip()
        if "global.document.metadata=" in line:
            metadata = line[line.find("global.document.metadata=") + len("global.document.metadata="):line.rindex("}") + 1]
            metadata = json.loads(metadata)
            try:
                result = metadata['keywords'][0]['kwd']
                print result
                return result
            except KeyError:
                return None
