import re



kPrimaryData      = 0
kPrimaryTest      = 1
kSecondaryData    = 2
kSecondaryTest    = 3
kPrimaryResults   = 4
kSecondaryResults = 5
kExamples         = 6
kTestset          = 7

kData    = set([kPrimaryData, kSecondaryData])
kTest    = set([kPrimaryTest, kSecondaryTest])
kResults = set([kPrimaryResults, kSecondaryResults])
kPre     = set([kExamples, kTestset])


extension = {kPrimaryData      : 'd',
             kSecondaryData    : 'd',
             kPrimaryTest      : 't',
             kSecondaryTest    : 't',
             kPrimaryResults   : 'r',
             kSecondaryResults : 'r',
             kExamples         : 'e',
             kTestset          : 'ts'}

datare     = re.compile('.*\.d$')
testre     = re.compile('.*\.t$')
resultsre  = re.compile('.*\.r$')
examplesre = re.compile('.*\.e$')
testsetre  = re.compile('.*\.ts$')

primre        = re.compile('.*\[.*\]\.p\..$')
secre         = re.compile('.*\[.*\].*\[.*\]\.s\..$')
primresultsre = re.compile('.*\.p\.r$')
secresultsre  = re.compile('.*\[.*\].*\.s\.r$')


def sim_uid(sim_id, rep):
    return '{}.{:02d}'.format(sim_id, rep)

def p_name(cat, expname, psim_id, rep):
    return '{}[{}].p.{}'.format(expname, sim_uid(psim_id, rep), extension[cat])

def s_name(cat, primname, psim_id, secname, ssim_id, rep, ):
    return '{}[{}]{}[{}].s.{}'.format(primname, sim_uid(psim_id, rep),
                                      secname,  sim_uid(ssim_id, rep), extension[cat])

def r_pname(cat, expname):
    return '{}.p.{}'.format(expname, extension[cat])

def r_sname(cat, primname, source, secname):
    return '{}[{}].{}.s.{}'.format(primname, source, secname, extension[cat])

def e_name(cat, primname, source, uid, number):
    return '{}[{}.{}].{}.{}'.format(primname, source, uid, number, extension[cat])

def ts_name(cat, primname, source, size):
    return '{}[{}].{}.{}'.format(primname, source, size, extension[cat])

def split_jobname(name):
    if datare.match(name) is not None:
        if primre.match(name) is not None:
            return kPrimaryData
        else:
            assert secre.match(name) is not None
            return kSecondaryData
    elif testre.match(name) is not None:
        if primre.match(name) is not None:
            return kPrimaryTest
        else:
            assert secre.match(name) is not None
            return kSecondaryTest
    elif primresultsre.match(name) is not None:
        return kPrimaryResults
    elif secresultsre.match(name) is not None:
        return kSecondaryResults
    elif examplesre.match(name) is not None:
        return kExamples
    elif testsetre.match(name) is not None:
        return kTestset
    else:
        return None

def split_key(key):
    return key[0]

def name2key(name):
    if resultsre.match(name) is not None:
        return _results_key(name)
    elif primre.match(name) is not None:
        return _primary_key(name)
    elif secre.match(name) is not None:
        return _secondary_key(name)
    elif examplesre.match(name) is not None:
        return _examples_key(name)
    elif testsetre.match(name) is not None:
        return _testset_key(name)


_namefunc = {kPrimaryData      : p_name,
             kPrimaryTest      : p_name,
             kSecondaryData    : s_name,
             kSecondaryTest    : s_name,
             kPrimaryResults   : r_pname,
             kSecondaryResults : r_sname,
             kExamples         : e_name,
             kTestset          : ts_name,
            }

def key2jobname(key):
    cat = split_key(key)
    return _namefunc[cat](*key)

key2name = key2jobname

def _primary_key(name):
    """from 'exp[0.01].p.t' returns (kPrimaryTest, 'exp', 0, 1)"""
    assert primre.match(name) is not None

    expname, uid = name.split('[')
    uid = uid .split(']')[0]
    cfg, iteration = uid.split(".")

    if testre.match(name) is not None:
        return kPrimaryTest, expname, int(cfg), int(iteration)
    else:
        return kPrimaryData, expname, int(cfg), int(iteration)

def _secondary_key(name):
    """from 'origin[0.01]exp[2.01].d' returns (kSecondaryData, 'origin', 0, 'exp', 2, 1)"""
    assert secre.match(name) is not None

    primname, puid, suid = name.split('[')
    puid, secname = puid.split(']')
    suid = suid.split(']')[0]
    pcfg, piteration = puid.split(".")
    scfg, siteration = suid.split(".")
    assert piteration == siteration

    if testre.match(name) is not None:
        return kSecondaryTest, primname, int(pcfg), secname, int(scfg), int(piteration)
    else:
        assert datare.match(name) is not None
        return kSecondaryData, primname, int(pcfg), secname, int(scfg), int(piteration)

def _results_key(name):
    if primresultsre.match(name) is not None:
        expname = name.split('.')[0]
        return (kPrimaryResults, expname)
    if secresultsre.match(name) is not None:
        primname, source = name.split('[')
        source, secname= source.split(']')
        secname = secname.split('.')[1]
        return (kSecondaryResults, primname, int(source), secname)

def _examples_key(name):
        expname, cfg_id = name.split('[')
        cfg_id, size = cfg_id.split(']')
        cfg_id, uid = cfg_id.split('.')
        size = size.split('.')[1]
        return (kExamples, expname, int(cfg_id), uid, int(size))


def _testset_key(name):
    expname, cfg_id = name.split('[')
    cfg_id, size = cfg_id.split(']')
    size = size.split('.')[1]
    return (kExamples, expname, int(cfg_id), int(size))
