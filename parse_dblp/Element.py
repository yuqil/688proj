class Element:
    OTHER = 0
    INPROCEEDING = 1
    PROCEEDING = 2

    def get_element(self, name):
        if name == "inproceedings":
            return self.INPROCEEDING
        elif name == "proceedings":
            return self.PROCEEDING
        else:
            return self.OTHER

    def get_element_name(self, index):
        if index == self.INPROCEEDING:
            return "inproceedings"
        elif index == self.PROCEEDING:
            return "proceedings"
        else:
            return "other"