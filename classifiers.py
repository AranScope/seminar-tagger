import os
import seminarparser

def read_all(directory):
    """ read all of the text files in a directory, appending them into one string """
    data = ''

    for txtfile in os.listdir(directory):
        with open(os.path.join(directory, txtfile)) as training_data:
            data += training_data.read()

    return data


class SeminarClassifier:

    def __init__(self):
        seminar_text = read_all('./seminars_training/training')
        self.entities = [e for e in seminarparser.extract_entities_iter(seminar_text)]
