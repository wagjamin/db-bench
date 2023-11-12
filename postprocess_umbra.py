#! /usr/bin/python3

import os
import re

backends = {'a': 'adaptive', 'o': 'optimized'}

written_files = []
print("Postprocessing results for Umbra")

for file in os.listdir('umbra_data'):
    if '_res_' in file:
        matched = re.search('^([_a-z0-9]*)_([ao])_res_([0-9.]*).csv', file)
        q_name = matched.group(1)
        mode = matched.group(2)
        sf = matched.group(3).replace('_', '.')
        with open(f'umbra_data/{file}') as f:
            fname = f'result_umbra_{backends[mode]}_{sf}.csv'
            fmode = 'a'
            if fname not in written_files:
                fmode = 'w'
            with open(fname, fmode) as out:
                written_files = written_files + [fname]
                for line in f:
                    times = re.search('execution: \(([0-9.]*).*compilation: \(([0-9.]*)', line)
                    # Seconds -> Milliseconds
                    time = int(1000 * (float(times.group(1)) + float(times.group(2))))
                    # Seconds -> Microseconds
                    stalled = 1000 * 1000 * float(times.group(2))
                    out.write(f'umbra_{backends[mode]},{q_name},{sf},{time},{stalled}\n')
