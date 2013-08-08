import names
import datafile
import qstat

from functools import total_ordering

_finished = set()
_running  = set()

def update():
    global _finished, _running
    _finished = set()
    _running  = set()

    datafile.update()
    available = datafile.data_available()
    for filename in available:
        key = names.name2key(filename)
        assert key is not None
        _finished.add(key)

    running_jobs = qstat.get_running_jobs()
    for jobname, jobid in running_jobs:
        if names.split_jobname(jobname) is not None:
            _running.add(names.name2key(jobname))

def is_finished(key):
    """Return true if the job is missing"""
    return key in _finished

def is_missing(key):
    """Return true if the job is missing"""
    return not (key in _finished or key in _running)

class DependencyForest(object):

    def __init__(self):
        self._nodes = {}

    def add_job(self, jobname, cfg, dependencies = tuple()):
        node = DependencyNode(jobname, cfg, dependencies = dependencies)
        self._nodes[jobname] = node

    def update(self):
        update()
        for name, node in self._nodes.items():
            key = names.name2key(name)

            if key in _finished:
                node.finished = True
            if key in _running:
                node.running = True

    def job_status(self, jobname):
        node = self._nodes[jobname]
        finished, running, missing = [], [], []
        for depname in node.dependencies:
            if self._nodes[depname].finished:
                finished.append(depname)
            elif self._nodes[depname].running:
                running.append(depname)
            else:
                missing.append(depname)

        if node.finished:
            status = 'finished'
        elif node.running:
            status = 'running'
        else:
            status = 'missing'
        return status, finished, running, missing

    def to_run(self):
        jobs = []
        for jobname, node in self._nodes.items():
            if not (node.finished or node.running):
                if all(self._nodes[depname].finished for depname in node.dependencies):
                    jobs.append(node)
        return sorted(jobs)


@total_ordering
class DependencyNode(object):

    def __init__(self, name, cfg, dependencies = tuple()):
        self.name = name
        self.cfg  = cfg
        self.dependencies = list(dependencies)
        self.finished = False
        self.running  = False

    def add_dependency(self, name):
        self.dependencies.append(name)

    def qsub_options(self):
        if 'qsub.resources' in self.cfg:
            options = ['{}={}'.format(key, value) for key, value in self.cfg.qsub.resources.items()]
            if len(options) > 0:
                return ' -l {} '.format(','.join(sorted(options)))
        return ''

    def __lt__(self, other):
        return self.name < other.name
