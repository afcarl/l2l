import platform, sys

import exp_bias

write_config_files = False
if len(sys.argv) > 1 and sys.argv[1] == '-r':
    write_config_files = True

jobgraph = exp_bias.current_exp(write_config_files = write_config_files)
jobgraph.update()
joblist = jobgraph.to_run()

code = ''
for job in joblist:
    if platform.system() == 'Linux':
        code += 'qsub run.pbs -v configfile={}.cfg -N {} {}\n'.format(job.name, job.name, job.qsub_options())
    elif platform.system() == 'Darwin':
        code += 'python run.py {}.cfg\n'.format(job.name)
    else:
        assert False

print code
