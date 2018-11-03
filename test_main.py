import sys
import json
import csv
if sys.version < '3':
    from urllib2 import urlopen
    from urllib import quote as urlquote
else:
    from urllib.request import urlopen
    from urllib.parse import quote as urlquote

UD_DEFID_URL = 'https://api.urbandictionary.com/v0/define?defid='
UD_DEFINE_URL = 'https://api.urbandictionary.com/v0/define?term='
UD_RANDOM_URL = 'https://api.urbandictionary.com/v0/random'

WORD_URL = "https://raw.githubusercontent.com/words/an-array-of-english-words/master/corpus/originals.txt"

class UrbanDefinition(object):
    def __init__(self, word, definition, example, upvotes, downvotes):
        self.word = word
        self.definition = definition
        self.example = example
        self.upvotes = upvotes
        self.downvotes = downvotes

    def __str__(self):
        return '%s: %s%s (%d, %d)' % (
                self.word,
                self.definition[:50],
                '...' if len(self.definition) > 50 else '',
                self.upvotes,
                self.downvotes
            )

def _get_urban_json(url):
    f = urlopen(url)
    data = json.loads(f.read().decode('utf-8'))
    f.close()
    return data

def _parse_urban_json(json, check_result=True):
    result = []
    if json is None or any(e in json for e in ('error', 'errors')):
        raise Exception('UD: Invalid input for Urban Dictionary API')
    if check_result and ('list' not in json or len(json['list']) == 0):
        return result
    for definition in json['list']:
        d = UrbanDefinition(
                definition['word'],
                definition['definition'],
                definition['example'],
                int(definition['thumbs_up']),
                int(definition['thumbs_down'])
            )
        result.append(d)
    return result

def define(term):
    """Search for term/phrase and return list of UrbanDefinition objects.
    Keyword arguments:
    term -- term or phrase to search for (str)
    """
    json = _get_urban_json(UD_DEFINE_URL + urlquote(term))
    return _parse_urban_json(json)

def defineID(defid):
    """Search for UD's definition ID and return list of UrbanDefinition objects.
    Keyword arguments:
    defid -- definition ID to search for (int or str)
    """
    json = _get_urban_json(UD_DEFID_URL + urlquote(str(defid)))
    return _parse_urban_json(json)

def random():
    """Return random definitions as a list of UrbanDefinition objects."""
    json = _get_urban_json(UD_RANDOM_URL)
    return _parse_urban_json(json, check_result=False)

# accumaltor = 0
# for word_def in define("hello"):
#     accumaltor += word_def.upvotes

# print(accumaltor)

# data = urlopen(WORD_URL)  # it's a file like object and works just like a file
# for line in data:  # files are iterable
#     print(str(line[:-1], 'utf-8'))

with open('data.csv', 'w') as csvfile:
    data = urlopen(WORD_URL) # it's a file like object and works just like a file
    wordwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='\r', quoting=csv.QUOTE_MINIMAL)
    wordwriter.writerow(["word", "total_upvotes"])
    for line in data: # files are iterable
        accumaltor = 0
        for word_def in define(line):
            accumaltor += word_def.upvotes

        wordwriter.writerow([str(line[:-1], 'utf-8'), accumaltor])
        print(accumaltor)

#
# with open('eggs.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',',
#                             quotechar='\r', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])