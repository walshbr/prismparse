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
        self.recreated_text = self.recreate_text_from_spans()

    def recreate_text_from_spans(self):
        """Gives a tokenized list of the text in the prism"""
        return [word.text for word in
                BeautifulSoup(self.content, 'lxml').select('.word')]


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

    def get_all_markings_for_a_uuid(self, prism_uuid):
        return [marking for marking
                in self.word_markings if marking.prism_id == prism_uuid]

    def markings_by_facet_num(self, list_of_markings):
        """Need to """
        markings_count_by_facets = {1: [], 2: [], 3: []}
        for marking in list_of_markings:
            markings_count_by_facets[marking.facet_id].append(marking.index)
        # markings_count_by_facets[marking.facet_id] =\
        #     markings_count_by_facets.append(marking.index)
        return(markings_count_by_facets)

    def get_counts_for_all_words(self, prism):
        """Given a prism, produce a list of counts for each word."""
        markings = self.get_all_markings_for_a_uuid(prism.uuid)
        sorted_markings = self.markings_by_facet_num(markings)
        tokenized_text = prism.recreated_text
        words_with_markings = []
        for index, word in enumerate(tokenized_text):
            markings = {1: 0, 2: 0, 3: 0}
            for key in [1, 2, 3]:
                if index in sorted_markings[key]:
                    markings[key] += 1
            words_with_markings.append((word, markings))
        print(words_with_markings)
        # appears to be working - I think you just don't have any
        # words that have been marked more than once. should check when you
        # get a real database dump.

        return words_with_markings

    def produce_models(self):
        """Generates data models from a given database file."""
        prisms = [Prism(record) for record in self.json['prisms']['records']]
        facets = [Facet(record) for record in self.json['facets']['records']]
        word_markings = [WordMarking(record) for record in
                         self.json['word_markings']['records']]
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


def main():
    """Functions for when called from CLI."""
    print(ParsedData())
    # uuids = get_all_prism_uuids(the_json)
    # words = recreate_text_from_spans(the_json)


if __name__ == '__main__':
    main()
