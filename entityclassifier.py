import requests
import json

class WikiClassifier:
    """
    Classifies an entity into one of [ORGANIZATION, PERSON, LOCATION] using
    DBPedia and requests.
    """

    def __init__(self):
        self.request_url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString={0}"

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.entity_map = {
            "place": "LOCATION",
            "person": "PERSON",
            "organisation": "ORGANIZATION"
        }

        pass

    def classify(self, entity):

        r = requests.get(
            self.request_url.format(entity),
            headers=self.headers
        )

        results = json.loads(r.text)["results"]

        for result in results:
            for result_class in result["classes"]:
                label = result_class["label"]
                if label in self.entity_map:
                    return self.entity_map[label]

        return None


if __name__ == "__main__":
    classifier = WikiClassifier()

    while True:
        entity = input("Entity: ")
        result = classifier.classify(entity)
        print(result)
