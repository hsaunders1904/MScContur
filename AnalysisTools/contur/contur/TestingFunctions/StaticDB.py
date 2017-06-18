import sqlite3 as db
import re
from os.path import dirname, join

INIT = False

INVALID = (-1,'','')

lumis = {}
pools = {}
whitelists = {}
blacklists = {}
pool_names = []

class listdict(dict):
    def __missing__(self, key):
        self[key] = []
        return self[key]

subpools = listdict()
norms = listdict()
    
name_pat = re.compile(r'([A-Z0-9]+_\d{4}_[IS]\d{6,8}[^/]*)/(d\d+-x\d+-y\d+)')


def init_dbs():
    
    dbfile = join(dirname(__path__), 'analyses.db')
    conn = db.connect(dbfile)
    c = conn.cursor()
    
    for row in c.execute('SELECT id,lumi,pool FROM analysis;'):
        ana,lumi,pool = row
        lumis[ana] = lumi
        if pool:
            pools[ana] = pool
            pool_names.append(pool)
        else:
            pools[ana] = ''
    
    for row in c.execute('SELECT id,group_concat(pattern) FROM whitelist GROUP BY id;'):
        ana, patterns = row
        patterns = patterns.split(',')
        whitelists[ana] = patterns
    
    for row in c.execute('SELECT id,group_concat(pattern) FROM blacklist GROUP BY id;'):
        ana, patterns = row
        patterns = patterns.split(',')
        blacklists[ana] = patterns
    
    for row in c.execute('SELECT id,pattern,subid FROM subpool;'):
        ana, pattern, subid = row
        subid = 'R%s' % (subid + 1)
        subpools[ana].append((pattern, subid))

    for row in c.execute('SELECT id,pattern,norm FROM normalization;'):
        ana, pattern, norm = row
        norms[ana].append((pattern, norm))
    
    conn.close()

    global INIT
    INIT = True

class InvalidPath(Exception):
    pass

def splitPath(path):
    m = name_pat.search(path)

    if not m:
        raise InvalidPath('Parse error in "%s"' % path)

    analysis = m.group(1);
    tag = m.group(2);

    return analysis, tag

    
def LumiFinder(h):

    if not INIT:
        init_dbs()

    ana, tag = splitPath(h)

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
        for p, subid in subpools[ana]:
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

    ana, tag = splitPath(h)

    isNorm=False
    normFac=1.0

    # remove once it's clear this is just a compatibility
    # preservation issue
    if 'ATLAS_2014_I1279489' in h:
        isNorm=True

    if ana in norms:
        for p, norm in norms[ana]:
            if re.search(p,tag):
                isNorm = True
                normFac = norm
                break

    return isNorm, normFac

# workaround for old interface
global anapool
anapool = pool_names
