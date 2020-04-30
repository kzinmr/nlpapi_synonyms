# SimpleEntityResolverが読める形にデータを前処理

from io import StringIO
import csv
from collections import defaultdict
import json

sense2synonyms = defaultdict(list)
entries = []
with open('synonyms.txt') as fp:
    for scsv in fp.read().split('\n\n'):
        f = StringIO(scsv)
        reader = csv.reader(f, delimiter=',')
        for r in reader:
            if len(r) > 8:
                sense2synonyms[r[0]].append(r[8])

entries = [{'id': sense, 'title': synonyms[0], 'aliases': synonyms} for sense, synonyms in sense2synonyms.items()]

with open('sudachi_entry_aliases.jsonl', 'wt') as fp:
    for data in entries:
        line = json.dumps(data, ensure_ascii=False)
        fp.write(line)
        fp.write('\n')

print(len(sense2synonyms))