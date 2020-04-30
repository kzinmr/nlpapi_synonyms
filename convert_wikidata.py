from pathlib import Path
import gzip
import json
from tqdm import tqdm


cnt = 0

with open('20191125-split-ja-title.jsonl') as fp:
    for l in tqdm(fp):
        if len(l.strip()[:-1]) < 3:
            continue
        d = json.loads(json.loads(l))
        if d['aliases_ja']:
            cnt += 1
            data = {'id': d['id'], 'title': d['title_ja']['value'], 'aliases': d['aliases_ja']}
            ol = json.dumps(data, ensure_ascii=False)
            outlines.append(ol)

with open('wikipedia_entry_aliases.jsonl', 'wt') as fp:
    for l in outlines:
        fp.write(ol)
        fp.write('\n')

print(cnt)