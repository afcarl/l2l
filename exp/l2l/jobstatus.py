import platform

from toolbox import gfx

import exp_bias
import sys

exp_bias.origin_exp()
exp_bias.bias_exp(expname = 'bias')
exp_bias.bias_exp(expname = 'nobias')

babbling = [100, 200, 500, 1000, 2000, 3000, 4000, 5000, 7000, 10000]
for min_orderbabble in babbling:
    exp_bias.param_exp(min_orderbabble, bias = True)
    exp_bias.param_exp(min_orderbabble, bias = False)

exp_bias.deps.update()

jobname = sys.argv[1]
status, finished, running, missing = exp_bias.deps.job_status(jobname)

for job in finished:
    print('[{}DONE   {}] {}{}{}'.format(gfx.green,  gfx.end, gfx.purple, job, gfx.end))

for job in running:
    print('[{}RUNNING{}] {}{}{}'.format(gfx.yellow, gfx.end, gfx.purple, job, gfx.end))

for job in missing:
    print('[{}MISSING{}] {}{}{}'.format(gfx.red,    gfx.end, gfx.purple, job, gfx.end))

print('done/running/missing: {}/{}/{}'.format(len(finished), len(running), len(missing)))
print('{}{}{} is {}{}{}.'.format(gfx.bold, jobname, gfx.end,
                                 gfx.red if len(missing) > 0 else (gfx.yellow if len(running) > 0 else gfx.green),
                                 status, gfx.end))