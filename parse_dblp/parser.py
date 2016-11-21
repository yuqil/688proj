import xml.sax
import sys
from Paper import Paper
import time
from Element import Element
from Conference import Conference

PAPER = Paper()
ELEMENT = Element()
CONFERENCE = Conference()

class DBLPContentHandler(xml.sax.ContentHandler):
    """
    Reads the dblp.xml file and produces two output files.
          pubFile.txt = (key, pubtype) tuples
          fieldFile.txt = (key, fieldCnt, field, value) tuples
    Each file is tab-separated

    Once the program finishes,  load these two files in a relational database; run createSchema.sql
    """
    cur_element = -1
    ancestor = -1
    paper = None
    conf = None
    line = 0
    errors = 0
    author = ""

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        DBLPContentHandler.inproc_file = open('inproc.txt', 'w')
        DBLPContentHandler.cite_file = open('cite.txt', 'w')
        DBLPContentHandler.conf_file = open('conf.txt', "w")
        DBLPContentHandler.author_file = open("author.txt", "w")

    def startElement(self, name, attrs):
        if name == "inproceedings":
            self.ancestor = ELEMENT.INPROCEEDING
            self.cur_element = PAPER.INPROCEEDING
            self.paper = Paper()
            self.paper.key = attrs.getValue("key")
        elif name == "proceedings":
            self.ancestor = ELEMENT.PROCEEDING
            self.cur_element = CONFERENCE.PROCEEDING
            self.conf = Conference()
            self.conf.key = attrs.getValue("key")
        elif name == "author" and self.ancestor == ELEMENT.INPROCEEDING:
            self.author = ""

        if name == "cite":
            print "cite    ", self.ancestor
        if self.ancestor == ELEMENT.INPROCEEDING:
            self.cur_element = PAPER.get_element(name)
            if self.cur_element == PAPER.CITE:
                print "CITE ELEMENT"
        elif self.ancestor == ELEMENT.PROCEEDING:
            self.cur_element = CONFERENCE.get_element(name)
        elif self.ancestor == -1:
            self.ancestor = ELEMENT.OTHER
            self.cur_element = ELEMENT.OTHER
        else:
            self.cur_element = ELEMENT.OTHER

        self.line += 1

    def endElement(self, name):
        if name == "author" and self.ancestor == ELEMENT.INPROCEEDING:
            self.paper.authors.append(self.author)

        if ELEMENT.get_element(name) == ELEMENT.INPROCEEDING:
            self.ancestor = -1
            try:
                if self.paper.title == "" or self.paper.conference == "" or self.paper.year == 0:
                    print ("error in parsing " + self.paper.key)
                    print self.paper.title
                    print self.paper.conference
                    print self.paper.year
                    self.errors += 1
                    return

                keywords = ["machine learning", "data mining", "data analysis", "deep learning", "pattern recognition",
                            "reinforcement learning", "unsupervised learning", "supervised learning", "computer vision",
                            "semi-supervised learning", "knowledge discovery", "big data", "data analytic",
                            "graphical models", "bayesian learning"]

                for keyword in keywords:
                    if keyword in self.paper.title or keyword in self.paper.conference:
                        self.write_paper(self.paper)
                        for t in self.paper.authors:
                            self.write_author(t, self.paper)
                        for c in self.paper.citations:
                            if c != "...":
                                self.write_citation(c, self.paper)
                        return
                    
            except ValueError:
                print "error"

        elif ELEMENT.get_element(name) == ELEMENT.PROCEEDING:
            self.ancestor = -1
            try:
                if self.conf.name == "":
                    self.conf.name = self.conf.detail
                if self.conf.key == "" or self.conf.name == "" or self.conf.detail == "":
                    print "Line ", self.line
                    return
                self.write_conf(self.conf)
            except ValueError:
                print "error"

    def write_conf(self, conf):
        DBLPContentHandler.conf_file.write(conf.key + "\t")
        DBLPContentHandler.conf_file.write(conf.name + "\t")
        DBLPContentHandler.conf_file.write(conf.detail + "\n")

    def write_paper(self, paper):
        # print paper.toString()
        DBLPContentHandler.inproc_file.write(paper.title + "\t")
        DBLPContentHandler.inproc_file.write(str(paper.year) + "\t")
        DBLPContentHandler.inproc_file.write(paper.conference + "\t")
        DBLPContentHandler.inproc_file.write(paper.key + "\n")

    def write_author(self, t, paper):
        DBLPContentHandler.author_file.write(t + "\t")
        DBLPContentHandler.author_file.write(paper.key + "\n")

    def write_citation(self, c, paper):
        DBLPContentHandler.cite_file.write(paper.key + "\t")
        DBLPContentHandler.cite_file.write(c + "\n")

    def characters(self, content):
        content = content.encode('utf-8').replace('\\', '\\\\').replace('\n', "").replace('\r', "")
        if self.ancestor == ELEMENT.INPROCEEDING:
            if self.cur_element == PAPER.AUTHOR:
                self.author += content
            elif self.cur_element == PAPER.CITE:
                if len(content) == 0:
                    return
                self.paper.citations.append(content)
            elif self.cur_element == PAPER.CONFERENCE:
                self.paper.conference += content
            elif self.cur_element == PAPER.TITLE:
                self.paper.title += content
            elif self.cur_element == PAPER.YEAR:
                if len(content) == 0:
                    return
                try:
                    self.paper.year = int(content)
                except ValueError:
                    print "s" + content + "s"
                    print float(content)
        elif self.ancestor == ELEMENT.PROCEEDING:
            if self.cur_element == CONFERENCE.CONFNAME:
                self.conf.name = content
            elif self.cur_element == CONFERENCE.CONFDETAIL:
                self.conf.detail = content

def main(sourceFileName):
    print "starttime: ", time.time()
    source = open(sourceFileName)
    xml.sax.parse(source, DBLPContentHandler())
    print "endtime: ", time.time()


if __name__ == "__main__":
    main("dblp.xml")


