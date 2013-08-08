import env
from explib.analysis import graphs

if __name__ == "__main__":
    labels = ['a. source',     'b. symmetric',  'c. bigger',      'd. distal',
              'e. heavy cube', 'f. light cube', 'g. corner base', 'h. center base',
              'a. source', 'b. distal']
    line_colors_dict = {"source": (  0/255.0,  21/255.0,  80/255.0),
                        "imbias": (189/255.0,  21/255.0,  80/255.0),
    }
    secnames = ["imbias"]
    grid = [[0],
            [1],
            [5],
            [6],
            [7]]

    graphs.generate_secgraph("mbab01K", 0, secnames, [[7]], labels, max_tick = 10000, line_colors = [line_colors_dict[name] for name in ["source"]+secnames], size = (600, 350))

    grid = [[8]]
    graphs.generate_secgraph("mbab01K", 8, secnames, grid, labels, max_tick = 10000, line_colors = [line_colors_dict[name] for name in ["source"]+secnames], size = (600, 350))

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

    # generate_primgraph('som', [[0]], ['goal babbling at 500'])