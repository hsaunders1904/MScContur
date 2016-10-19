import sqlite3 as db
import re

INIT = False

INVALID = (-1,'','')

lumis = {}
pools = {}
whitelists = {}
blacklists = {}

class listdict(dict):
    def __missing__(self, key):
        self[key] = []
        return self[key]

subpools = listdict()
    
name_pat = re.compile(r'([A-Z0-9]+_\d{4}_[IS]\d{6,8}[^/]*)/(d\d+-x\d+-y\d+)')


def init_dbs():
    
    conn = db.connect('analyses.db')
    c = conn.cursor()
    
    for row in c.execute('SELECT id,lumi,pool FROM analysis;'):
        ana,lumi,pool = row
        lumis[ana] = lumi
        pools[ana] = pool if pool else ''
    
    for row in c.execute('SELECT id,group_concat(pattern) FROM whitelist GROUP BY id;'):
        ana, patterns = row
        patterns = patterns.split(',')
        whitelists[ana] = patterns
    
    for row in c.execute('SELECT id,group_concat(pattern) FROM blacklist GROUP BY id;'):
        ana, patterns = row
        patterns = patterns.split(',')
        blacklists[ana] = patterns
    
    for row in c.execute('SELECT id,group_concat(pattern),subid FROM subpool GROUP BY id,subid;'):
        ana, patterns, subid = row
        patterns = patterns.split(',')
        subid = 'R%s' % (subid + 1)
        subpools[ana].append((patterns, subid))
    
    conn.close()

    global INIT
    INIT = True
    
def LumiFinder(h):

    if not INIT:
        init_dbs()

    m = name_pat.search(h)
    if not m:
        return INVALID

    ana = m.group(1);
    tag = m.group(2);

    try:
        lumi, pool = lumis[ana], pools[ana]
    except KeyError:
        return INVALID


    if ana in whitelists:
        for pattern in whitelists[ana]:
            if pattern in tag:
                break
        else:
            return INVALID

    if ana in blacklists:
        for pattern in blacklists[ana]:
            if pattern in tag:
                return INVALID

    subpool = ''

    if ana in subpools:
        for patterns, subid in subpools[ana]:
            for p in patterns:
                if re.search(p,tag):
                    subpool = subid
                    break
        #else:
            # not in any subpools
            # strict mode should exit here
            #return INVALID

    return lumi,pool,subpool

#############################################################################################
### Special function to help with plots normalised to total xs
def isNorm(h):
    if not INIT:
        init_dbs()
    return isNorm, normFac



