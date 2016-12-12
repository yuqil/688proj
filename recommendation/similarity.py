import string
from nltk.corpus import stopwords
import config
import os


class abstract_similarity:
    lam = 0.1
    mu = 0.1

    def __init__(self, path=os.path.join(config.filtered_dir, 'paper-1985-2015.csv')):
        file = open(path)
        stop = set(stopwords.words('english'))
        stop.add("using")
        stop.add("based")

        self.dict = {}
        self.total = 0
        for line in file:
            line = line.rstrip().lower()
            line = line[line.find('"'):]
            title = line.lower().rstrip().translate(None, string.punctuation)
            words = title.split(" ")
            for i in range(0, len(words)):
                word = words[i]
                if words[i] in stop :
                    continue
                if word in self.dict:
                    self.dict[word] += 1
                else:
                    self.dict[word] = 1
                self.total += 1
        file.close()

    def getScore(self, abstract1, abstract2):
        '''
        :param abstract1: input
        :param abstract2: another doc that needs to be compared
        :return: similarity score
        '''
        counter2 = {}
        stop = set(stopwords.words('english'))
        words1 = abstract1.rstrip().lower().rstrip().translate(None, string.punctuation).split(" ")
        words2 = abstract2.rstrip().lower().rstrip().translate(None, string.punctuation).split(" ")
        stop.add("using")
        stop.add("based")
        doclen = 0
        for word in words2:
            if word in stop:
                continue
            doclen += 1
            if word in counter2:
                counter2[word] += 1
            else:
                counter2[word] = 1

        score = 0.0
        for word in words1:
            tf = 0.0
            if word in stop:
                continue
            if word in counter2:
                tf = counter2[word]
            if word in self.dict:
                ctf = self.dict[word]
            else:
                ctf = 0.0
            score += (1-self.lam) * ((tf + self.mu * ctf / self.total) / (doclen + self.mu)) + self.lam * (ctf / self.total)
        return score

#
# abstract1 = "A novel set of moment invariants based on the Krawtchouk moments are introduced in this paper. These moment invariants are computed over a finite number of image intensity slices, extracted by applying an innovative image representation scheme, the image slice representation (ISR) method. Based on this technique an image is decomposed to a several non-overlapped intensity slices, which can be considered as binary slices of certain intensity. This image representation gives the advantage to accelerate the computation of image's moments since the image can be described in a number of homogenous rectangular blocks, which permits the simplification of the computation formulas. The moments computed over the extracted slices seem to be more efficient than the corresponding moments of the same order that describe the whole image, in recognizing the pattern under processing. The proposed moment invariants are exhaustively tested in several well known computer vision datasets, regarding their rotation, scaling and translation (RST) invariant recognition performance, by resulting to remarkable outcomes."
#
# abstract2 = "A novel set of moment invariants based on the Krawtchouk moments are introduced in this paper. These moment invariants are computed over a finite number of image intensity slices, extracted by applying an innovative image representation scheme, the image slice representation (ISR) method. Based on this technique an image is decomposed to a several non-overlapped intensity slices, which can be considered as binary slices of certain intensity. This image representation gives the advantage to accelerate the computation of image's moments since the image can be described in a number of homogenous rectangular blocks, which permits the simplification of the computation formulas. The moments computed over the extracted slices seem to be more efficient than the corresponding moments of the same order that describe the whole image, in recognizing the pattern under processing. The proposed moment invariants are exhaustively tested in several well known computer vision datasets, regarding their rotation, scaling and translation (RST) invariant recognition performance, by resulting to remarkable outcomes."
#
# simi_eva = abstract_similarity()
# print simi_eva.getScore(abstract1, abstract2)
