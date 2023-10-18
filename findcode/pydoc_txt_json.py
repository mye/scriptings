from pathlib import Path
from textwrap import dedent
import re, json

def convert_txt_json(filepath):
	path = Path(f)
	jsonpath = path.with_suffix('.json')
	passages = re.split(r'\n\n', open(path).read())
	linecnt = 0
	extracts = []
	for p in passages:
		newlines = p.count('\n') + 2
		acme_linenum = linecnt + 1 # acme start linecount at 1
		linecnt += newlines
		if len(p) > 87:
			ex = {
				'backlink': f"{path}:{acme_linenum}",
				'passage': dedent(p)
			}
			extracts.append(ex)
	json.dump(extracts, open(jsonpath, 'w'), indent=2)

if __name__ == '__main__':
	import sys
	f = sys.argv[1]
	convert_txt_json(f)
	print('converted', f)
