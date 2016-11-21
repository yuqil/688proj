class Conference:
    OTHER = 0
    PROCEEDING = 1
    CONFNAME = 2
    CONFDETAIL = 3


    def __init__(self):
        self.key = ""
        self.name = ""
        self.detail = ""

    def get_element(self, name):
        if name == "proceedings":
            return self.PROCEEDING
        elif name == "booktitle":
            return self.CONFNAME
        elif name == "title":
            return self.CONFDETAIL
        else:
            return self.OTHER

    def get_element_name(self, index):
        if index == self.PROCEEDING:
            return "proceedings"
        elif index == self.CONFNAME:
            return "booktitle"
        elif index == self.CONFDETAIL:
            return "title"
        else:
            return "other"