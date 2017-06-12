"""Provides a wrapper for interacting with database data pulled from Prism."""
# yaml parsing adapted from:
# gist https://gist.github.com/noahcoad/51934724e0896184a2340217b383af73

# ( POSITION INDEX; WORD; MARKINGS TOPIC0; MARKINGS TOPIC1; MARKINGS TOPIC2 …)

# get a list of texts
# for each text, get the words and their indexes
# for each word, get the markings for each facets and total them
# in the word_markings table - collect them by text by using the prism_id.
# collect all word_markings for a particular prism
# then group by index position

import csv
import json
import yaml
from bs4 import BeautifulSoup


class Prism(object):
    """Generate facet objects from YML/JSON."""
    def __init__(self, record):
        self.uuid = record[0]
        self.created_at = record[1]
        self.updated_at = record[2]
        self.title = record[3]
        self.author = record[4]
        self.content = record[5]
        self.num_words = record[6]
        self.description = record[7]
        self.user_id = record[8]
        self.unlisted = record[9]
        self.publication_date = record[10]
        self.language = record[11]
        self.license = record[12]


class WordMarking(object):
    """Generate facet objects from YML/JSON."""
    def __init__(self, record):
        self.id_num = record[0]
        self.index = record[1]
        self.created_at = record[2]
        self.updated_at = record[3]
        self.user_id = record[4]
        self.facet_id = record[5]
        self.prism_id = record[6]


class Facet(object):
    """Generate facet objects from YML/JSON."""
    def __init__(self, record):
        self.id_num = record[0]
        self.color = record[1]
        self.description = record[2]
        self.created_at = record[3]
        self.updated_at = record[4]
        self.order = record[5]
        self.prism_id = record[6]


class ParsedData(object):
    """Provides data parsing methods for working with Prism data."""
    def __init__(self):
        self.filename = 'data.yml'
        self.json = self.get_yaml_and_convert_to_json()
        self.prisms, self.facets, self.word_markings = self.produce_models()

    def get_all_prism_uuids(self):
        """Returns all uuids pertaining to a particular Prism."""
        return [prism.uuid for prism in self.prisms]

    def recreate_text_from_spans(self):
        """Gives a tokenized list of the text in the prism"""
        all_words = []
        for prism in self.prisms:
            words = [word.text for word in BeautifulSoup(prism.content, 'lxml').select('.word')]
            all_words.append(words)
        return all_words

    def produce_models(self):
        """Generates data models from a given database file."""
        prisms = [Prism(record) for record in self.json['prisms']['records']]
        facets = [Facet(record) for record in self.json['facets']['records']]
        word_markings = [WordMarking(record) for record in self.json['word_markings']['records']]
        return prisms, facets, word_markings

    def get_yaml_and_convert_to_json(self):
        """Works from filename -> YML -> json"""
        with open(self.filename, 'r') as fin:
            raw_text = fin.read()
            proc_yaml = yaml.load(raw_text)
            proc_json = json.dumps(proc_yaml, sort_keys=True, indent=2)
            return json.loads(proc_json)

    def write_to_csv(self, data):
        """Write to CSV"""
        with open('output.csv', 'w') as fout:
            writer = csv.writer(fout)
            for row in data:
                writer.writerow(row)

# word_markings = ['id', 'index', 'created_at', 'updated_at', 'user_id', 'facet_id', 'prism_id']
# we care about index, facet_id, and prism_id
#
# def get all_markings_for_a_prism('uuid'):
#     """take a uuid and return only the word_markings for that prism."""
#     pass


def main():
    """Functions for when called from CLI."""
    print(ParsedData())
    # uuids = get_all_prism_uuids(the_json)
    # words = recreate_text_from_spans(the_json)

if __name__ == '__main__':
    main()
