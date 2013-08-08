import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cPickle
from toolbox import gfx

import env
from runs import datafile, paths, names

global_line_colors = ((  0/255.0,  21/255.0,  80/255.0),
                      (189/255.0,  21/255.0,  80/255.0),
                      (189/255.0,  21/255.0,  80/255.0))


background_color = (215/255.0,  215/255.0,  215/255.0)

class Graph(object):

    def __init__(self, size = (500, 800), columns = 2, rows = 4, line_colors = None, stddev = True):
        self._size    = size
        self._columns = columns
        self._rows    = rows
        self._figure = plt.figure(figsize = (size[0]/100.0, size[1]/100.0), dpi = 100, facecolor = background_color, edgecolor = background_color)
        self._line_colors = line_colors if line_colors is not None else global_line_colors
        self.stddev = stddev

    def setup_plot(self, pos, name, graph_data, min_tick = -float('inf'), max_tick = float('inf')):

        assert 0 <= pos[0] < self._columns and 0 <= pos[1] < self._rows
        grid_pos = self._rows*100 + self._columns*10 + self._columns*pos[1] + pos[0] + 1

        if any(perfs is not None for ticks, perfs, stds in graph_data):
            p = self._figure.add_subplot(grid_pos, axisbg=(235/255.0,  235/255.0,  235/255.0))
            #p.set_title(name, size = 10)

            for (ticks, perfs, stds), color in zip(graph_data, self._line_colors):
                if perfs is not None:
                    frame_ticks = [t for t in ticks if min_tick <= t <= max_tick]
                    frame_perfs = [e for t, e in zip(ticks, perfs) if min_tick <= t <= max_tick]
                    frame_perfs = np.array([700.0*e for e in frame_perfs])
                    frame_stds  = np.array([e for t, e in zip(ticks, stds) if min_tick <= t <= max_tick])
                    frame_stds  = np.array([700.0*e for e in frame_stds])
                    p.plot(frame_ticks, frame_perfs, color = color)
                    if self.stddev:
                        p.fill_between(frame_ticks, frame_perfs+frame_stds,
                                                    frame_perfs-frame_stds,
                                       facecolor=color, edgecolor=(1.0,1.0,1.0,0.1), alpha=0.3)

            p.tick_params(labelsize = 12)
            p.set_ylim((0, 370))

            return p

    def savefig(self, filename):
        if self._rows > 1:
            self._figure.subplots_adjust(bottom=0.05, left=0.1, right=0.9, top=0.95, hspace=0.55)
        self._figure.set_facecolor('black')
        filepath = '{}/{}.png'.format(paths.pngdir, filename)
        plt.savefig(filepath, dpi=300, format='png', facecolor = background_color)
        print('{}exp:{} graph saved in {}{}{}'.format(gfx.purple, gfx.grey, gfx.cyan, filepath, gfx.end))


def generate_secgraph(primname, source, secnames, grid, labels, min_tick = -float('inf'), max_tick = float('inf'), line_colors = None, size = (250, 200)):

    primresults = datafile.load_results(names.key2jobname((names.kPrimaryResults, primname)))['results']
    secresults_list = [datafile.load_results(names.key2jobname((names.kSecondaryResults, primname, source, secname)))['results'] for secname in secnames]

#    print primresults
#    print secresults_list[0]['results']

    columns, rows = len(grid[0]), len(grid)
    graph = Graph(columns = columns, rows = rows, size = (columns*size[0], rows*size[1]), line_colors = line_colors)

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            k = grid[r][c]
            results = [primresults[k]]
            for secresults in secresults_list:
                results.append(secresults[k])
            graph.setup_plot((c, r), labels[k], results, min_tick = min_tick, max_tick = max_tick)

    filename = names.key2jobname((names.kSecondaryResults, primname, source, "_".join(secnames)))
    graph.savefig(filename)

def generate_primgraph(primnames, grid, labels, size = (500, 200), min_tick = -float('inf'), max_tick = float('inf'), line_colors = None):

    columns, rows = len(grid[0]), len(grid)
    graph = Graph(columns = columns, rows = rows, size = size, line_colors = line_colors)


    for r in range(len(grid)):
        for c in range(len(grid[r])):
            k = grid[r][c]
            primresults_list = []
            for primname in primnames:
                data = datafile.load_results(names.key2jobname((names.kPrimaryResults, primname)))
                primresults_list.append(data['results'][k])

            graph.setup_plot((c, r), labels[k], primresults_list, min_tick = min_tick, max_tick = max_tick)

    filename = '_'.join(names.key2jobname((names.kPrimaryResults, primname)) for primname in primnames)
    graph.savefig(filename)

if __name__ == '__main__':
    labels = ['source',     'symmetric',  'bigger',      'distal',
              'heavy cube', 'light cube', 'corner base', 'center base']
    grid = [[0, 1],
            [2, 3],
            [4, 5],
            [6, 7]]

    grid = [[0, 1, 2, 3],
            [4, 5, 6, 7]]

    secnames = ["srbias05K", "imbias05K", "nobias05K"]
    line_colors_dict = {"source":    (  0/255.0,  21/255.0,  80/255.0),
                        "imbias05K": (189/255.0,  21/255.0,  80/255.0),
                        "nobias05K": (255/255.0, 156/255.0,  91/255.0),
                        "srbias05K": (122/255.0, 179/255.0,  23/255.0),
                       }
    # generate_secgraph("mbab05K", 0, secnames, grid, labels, max_tick = 10000, line_colors = [line_colors_dict[name] for name in ["source"]+secnames])

    #
    # datafile.update()
    # for sec_res in datafile.sec_res_available():
    #     cat, primname, source, secname = names.name2key(sec_res)
    #     generate_secgraph(primname, source, secname, grid, labels)

    # generate_primgraph('mbab100', [[0]], ['goal babbling at 100'])
    # generate_primgraph('mbab200', [[0]], ['goal babbling at 200'])
    # generate_primgraph('mbab500', [[0]], ['goal babbling at 500'])
    # generate_primgraph('mbab01K', [[0]], ['goal babbling at 1000'])
    # generate_primgraph('mbab02K', [[0]], ['goal babbling at 2000'])
    # generate_primgraph('mbab03K', [[0]], ['goal babbling at 3000'])
    # generate_primgraph('mbab05K', [[0]], ['goal babbling at 5000'])
    # generate_primgraph('mbab07K', [[0]], ['goal babbling at 7000'])
    # generate_primgraph('mbab10K', [[0]], ['pure motor babbling'])

    generate_primgraph('som', [[0]], ['goal babbling at 500'])
