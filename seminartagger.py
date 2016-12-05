import os
from chunkers import NeChunker
from entityclassifier import WikiClassifier
import nltk
import re

chunker = NeChunker()
classifier = WikiClassifier()

test_seminar = """
<0.27.10.94.12.41.00.muir+@CS.CMU.EDU (Patrick Muir).0>
Type:     cmu.cs.robotics
Topic:    Antal Bejczy Lecture Nov. 11
Dates:    11-Nov-94
Time:     1:30
PostedBy: muir+ on 27-Oct-94 at 12:41 from CS.CMU.EDU (Patrick Muir)
Abstract:

The Pittsburgh Robotics and Automation Chapter of the IEEE is
sponsoring a lecture by Antal Bejczy of JPL under the IEEE
distinguished lecture program. Antal will speak on the topic:
Calibrated Virtual Reality in Telerobotics. The lecture will
be in Wean 4623 at 1:30 on Friday November 11. All are invited.
"""

class SeminarTagger:

    def __init__(self):
        self.regex_patterns = {
            "time": "[0-23]:[0-9][0-9]"
        }

        self.para_tokenizer = nltk.tokenize.TextTilingTokenizer()

    def tokenize_sentence(self, text):
        return nltk.sent_tokenize(text)

    def tokenize_paragraph(self, text):
        return self.para_tokenizer.tokenize(text)

    def extract_entities(self, seminar_text):
        entities = chunker.generate_chunks(seminar_text)

        for entity in entities:
            entity_type = classifier.classify(entity)
            print(entity)
            if entity_type == "PERSON":
                yield ("speaker", entity)
            elif entity_type == "LOCATION":
                yield ("location", entity)


        time_matches = re.findall(self.regex_patterns["time"], seminar_text)

        for time_match in time_matches:
            yield("time", time_match)
            break
        else:
            yield("time", "unknown")








def read_all(directory):
    """ read all of the text files in a directory, appending them into one string """
    data = ''

    for txtfile in os.listdir(directory):
        with open(os.path.join(directory, txtfile)) as training_data:
            data += training_data.read()

    return data


