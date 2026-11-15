"""Builds ../index.html: the "So you're sure about…" shell (src/shell) over the arguing-with data.  Run: python3 src/build.py
chatter → topic → position → three replies (serious, bait, rage bait = written columns 1, 4 and 5). The position's full paraphrase sits above its replies."""
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, 'shell')); import shell
D = json.load(open(os.path.join(here, 'data.json'), encoding='utf-8')); PF = json.load(open(os.path.join(here, 'pfps.json')))
LV = [('○', 'serious', 0), ('◐', 'bait', 3), ('●', 'rage bait', 4)]
P = []
for c in sorted(D, key=lambda c: (c.get('s') or c['n']).lower()):
    s = {'n': c.get('s') or c['n'], 'i': '@' + c['u'], 'u': [], 't': []}
    for tp in c['t']:
        u = {'n': tp['t'], 't': []}
        for k in tp['k']:
            u['t'].append(len(s['t']))
            s['t'].append({'t': '“' + (k['b'] or k['p']) + '”', 'p': k['p'], 'k': [{'q': g + '  ' + n, 'f': k['l'][i]} for g, n, i in LV]})
        s['u'].append(u)
    P.append(s)
pf = {c['u']: PF[c['u']] for c in D if c['u'] in PF}
size = shell.build(P, os.path.join(here, '..', 'index.html'), title='So you’re arguing with…', lead='So you’re arguing with', key='aw',
    words=['chatter', 'topic', 'position', 'reply'], steps=['chatter', 'topic', 'position', 'replies'], plurals={'reply': 'replies'}, pfps=pf)
print('built index.html', size, '|', len(P), 'chatters,', sum(len(s['u']) for s in P), 'topics,', sum(len(s['t']) for s in P), 'positions | no pfp:', [s['n'] for s in P if s['i'][1:] not in pf])
