#! /usr/bin/python3

import duckdb
import os
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size': 20})

system_choices = ['duckdb', 'umbra_optimized', 'umbra_adaptive']
colors = ['#04718a', '#c5d31f', '#8d9511']
global_hatch = '///'

# Legend labels of the different systems
label_map = {
    'duckdb': 'DuckDB',
    'umbra_adaptive': 'Umbra (Hybrid)',
    'umbra_optimized': 'Umbra (LLVM)',
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Reproducibility Plotting',
                    description='Genreate plots for the db-bench reproducibility infrastructure.')
    parser.add_argument('sf', help='The scale factor for which we want to generate a plot')
    parser.add_argument('systems', metavar='N', nargs='+',
                        help=f'The systems we want to compare. Choices: {system_choices}.', choices=system_choices)
    args = parser.parse_args()

    sf = args.sf
    systems = args.systems

    con = duckdb.connect(database=':memory:')
    con.execute("CREATE TABLE results (engine text, query text, sf text, latency int, codegen_stalled int);")

    # Insert engine results
    for engine in systems:
      f_name = f'result_{engine}_{sf}.csv'
      con.execute(f"INSERT INTO results SELECT * FROM read_csv_auto('{f_name}', header=False)")

    con.execute('INSTALL icu; LOAD icu;')

    queries = [f'Q{i}' for i in np.arange(1, 23) ]
    x_vals = np.arange(1, 23)

    fig, axs = plt.subplots(1, 1, sharex=True)
    fig.set_size_inches(40, 9)
    plt.set_cmap('Set3')
    barwidth = 0.8 / len(systems)
    offset = -barwidth * (float(len(systems)) / 2) + (0.5 * barwidth)
    for engine_idx, engine in enumerate(systems):
        # Get the queries with minimal latency for the different queries and engines.
        res = con.execute(
            f"SELECT query, engine, first(latency) as latency, first(codegen_stalled) as codegen_stalled "
            f"FROM results o WHERE sf = '{sf}' and engine = '{engine}' "
            f"  and latency = (SELECT min(latency) FROM results i WHERE sf = '{sf}' and engine = '{engine}' and i.query = o.query)"
            f"GROUP BY query, engine "
            # ORDER BY int to make sure that ordering works as expected 
            f"ORDER BY query::INT").fetchnumpy()
        if len(res['latency']) != len(queries):
            print(f'missing benchmark results for {engine}, {sf}')
        # If we completely cut the x bars it looks like there is no data.
        # Some queries on sf0.01 do take 0 ms (rounded). Put them at 1 nevertheless to show there is data.
        # Note that xmax on that plot lies around 50, so this is still representative.
        res['latency'] = np.maximum(res['latency'], [1.5])
        # Set the color of the current engine
        bar_color = len(queries) * [colors[engine_idx]]
        stalled = res['codegen_stalled'] / 1_000_000
        non_stalled = res['latency'] / 1_000 - stalled
        axs.bar(x_vals + offset, stalled, width=barwidth, color=bar_color, edgecolor= 'black', hatch = global_hatch)
        axs.bar(x_vals + offset, non_stalled, bottom=stalled, width=barwidth, label=label_map[engine], color=bar_color, edgecolor= 'black')
        axs.set_xticks(x_vals, queries)
        axs.set_ylabel('Latency [s]')
        axs.set_title(f'TPC-H Scale Factor {sf}', y=0.85)
        offset += barwidth
    # HACK - Add empty bar to just get the legend to contain compliation latency
    axs.bar(x_vals + offset - 0.19, np.repeat(0, len(x_vals)), bottom=np.repeat(0, len(x_vals)), width=0.00001, label='Compilation Latency', hatch = global_hatch, color='white', edgecolor = 'black')
    fig.legend(loc='upper center', ncol=len(systems) + 1, fancybox=True, labelspacing=0.1, handlelength=1.8, handletextpad=0.4, columnspacing=1.0)
    # Different style things
    # 4. Space legend (actually okay)
    # plt.subplots_adjust(top=0.82)
    plt.subplots_adjust(left=0.01, right=0.99)
    # plt.show()
    os.makedirs('plots', exist_ok=True)
    plt.savefig(f'plots/sf_{sf}.pdf', bbox_inches='tight', dpi=300)
    plt.savefig(f'plots/sf_{sf}.png', bbox_inches='tight', dpi=300)
