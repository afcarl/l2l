import env
from explib.runs import datafile
from explib.runs import names

primname = 'mbab01K'
source = 0
secname = 'imbias'

def omega(t_max, exp_id):
    tick_p, avg_p, std_p = prim_res[exp_id]
    tick_s, avg_s, std_s = sec_res[exp_id]

    assert tick_s == tick_p

    err_p = sum(a for t, a in zip(tick_p, avg_p) if t <= t_max)
    err_s = sum(a for t, a in zip(tick_s, avg_s) if t <= t_max)

    #print err_p/err_s

    return (err_p-err_s)/err_p

if __name__ == '__main__':
    prim_res = datafile.load_results(names.key2jobname((names.kPrimaryResults, primname)))['results']
    sec_res  = datafile.load_results(names.key2jobname((names.kSecondaryResults, primname, source, secname)))['results']

    labels = ['source',     'symmetric',  'bigger',      'distal',
    'heavy cube', 'light cube', 'corner base', 'center base',
    'source', 'distal']


    for i in range(10):
#        print("Omega 1000 {} = {:2.3f}".format(i, omega( 700, i)))
        print("Omega 2000 {} = {:+2.3f}   ({})".format(i, omega( 2000, i), labels[i]))
        print("Omega10000 {} = {:+2.3f}   ({})".format(i, omega(10000, i), labels[i]))


    # negative transfer of corner base
    tick_p, avg_p, std_p = prim_res[6]
    tick_s, avg_s, std_s = sec_res[6]
    diff, diff_n = 0, 0
    for t, a_p, a_s in zip(tick_p, avg_p, avg_s):
        if 1500 < t:
            diff_n += 1
            diff += a_p-a_s
    print 700*diff/diff_n


    sec_res  = datafile.load_results(names.key2jobname((names.kSecondaryResults, primname, 8, secname)))['results']

    for i in range(8, 10):
    #        print("Omega 1000 {} = {:2.3f}".format(i, omega( 700, i)))
            print("Omega 2000 {} = {:+2.5f}   ({})".format(i, omega( 2000, i), labels[i]))
            print("Omega10000 {} = {:+2.5f}   ({})".format(i, omega(10000, i), labels[i]))
