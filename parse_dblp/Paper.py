class Paper:
    OTHER = 0
    INPROCEEDING = 1
    AUTHOR = 2
    TITLE = 3
    YEAR = 4
    CITE = 5
    CONFERENCE = 6

    def __init__(self):
        self.key = ""
        self.title = ""
        self.conference = ""
        self.year = 0
        self.authors = []
        self.citations = []

    def toString(self):
        return str(self.year) + " " + self.title + " ##" + str(self.citations)

    def get_element(self, name):
        if name == "inproceedings":
            return self.INPROCEEDING
        elif name == "author":
            return self.AUTHOR
        elif name == "year":
            return self.YEAR
        elif name == "cite":
            return self.CITE
        elif name == "booktitle":
            return self.CONFERENCE
        elif name in ["title", "sub", "sup", "i", "tt"]:
            return self.TITLE
        else:
            return self.OTHER

    def get_element_name(self, index):
        if index == self.INPROCEEDING:
            return "inproceedings"
        elif index == self.AUTHOR:
            return "author"
        elif index == self.TITLE:
            return "name"
        elif index == self.YEAR:
            return "year"
        elif index == self.CITE:
            return "cite"
        elif index == self.CONFERENCE:
            return "booktitle"
        else:
            return "other"