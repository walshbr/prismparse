# convert yaml to json
# pip3 install pyyaml
# http://pyyaml.org/wiki/PyYAMLDocumentation
# py3 yaml2json.py < ~/code/manpow/homeland/heartland/puphpet/config.yaml
# gist https://gist.github.com/noahcoad/51934724e0896184a2340217b383af73

# ( POSITION INDEX; WORD; MARKINGS TOPIC0; MARKINGS TOPIC1; MARKINGS TOPIC2 …)

# get a list of texts
# for each text, get the words and their indexes
# for each word, get the markings for each facets and total them
# in the word_markings table - collect them by text by using the prism_id.
# collect all word_markings for a particular prism
# then group by index position

import csv
import yaml, json, sys
from bs4 import BeautifulSoup

def write_to_csv(data):
    with open('output.csv', 'w') as fout:
        writer = csv.writer(fout)
        for row in data:
            writer.writerow(row)

def get_yaml_and_convert_to_json(fn):
    with open(fn, 'r') as fin:
        raw_text = fin.read()
        proc_yaml = yaml.load(raw_text)
        proc_json = json.dumps(proc_yaml, sort_keys=True, indent=2)

        return json.loads(proc_json)

def get_all_prism_uuids(json_data):
    return [row[0] for row in json_data['prisms']['records']]

def recreate_text_from_spans(json_data):
    """gives a tokenized list of the text in the prism"""
    all_words = []
    for row in json_data['prisms']['records']:
        words = [word.text for word in BeautifulSoup(row[5], 'lxml').select('.word')]
        all_words.append(words)
    return all_words
    # return [row[5] for row in ['prisms']['records'][0][5]]

class Prism(object):
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
    def __init__(self, record):
        self.id = record[0]
        self.index = record[1]
        self.created_at = record[2]
        self.updated_at = record[3]
        self.user_id = record[4]
        self.facet_id = record[5]
        self.prism_id = record[6]

class Facet(object):
    def __init__(self, record):
        self.id = record[0]
        self.color = record[1]
        self.description = record[2]
        self.created_at = record[3]
        self.updated_at = record[4]
        self.order = record[5]
        self.prism_id = record[6]


# word_markings = ['id', 'index', 'created_at', 'updated_at', 'user_id', 'facet_id', 'prism_id']
# we care about index, facet_id, and prism_id
#
# def get all_markings_for_a_prism('uuid'):
#     """take a uuid and return only the word_markings for that prism."""
#     pass

class Word(object):
    def __init__(self):
        self.facets
        self.markings

def produce_models(the_json):
    prisms = [Prism(record) for record in the_json['prisms']['records']]
    facets = [Facet(record) for record in the_json['facets']['records']]
    word_markings = [WordMarking(record) for record in the_json['word_markings']['records']]
    return prisms, facets, word_markings

def main():
    fn = 'db/data.yml'
    the_json = get_yaml_and_convert_to_json(fn)
    prisms, facets, word_markings = produce_models(the_json)
    # uuids = get_all_prism_uuids(the_json)
    # words = recreate_text_from_spans(the_json)

if __name__ == '__main__':
    main()
