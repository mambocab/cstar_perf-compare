"""
Usage: analyze.py <testid> [-o OUTPUT_DIR] [-f]

-o OUTPUT_DIR  # output directory
-f             # force download data. overwrites cached data
"""
from __future__ import print_function

import json
import os

import sh
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    testid = args['<testid>']
    force = args['-f']
    output_dir = os.path.join(args['-o'] or 'output',
                              testid)
    stats_file = os.path.join(output_dir, 'stats.json')

    if force or (not os.path.isfile(stats_file)):
        sh.mkdir('-p', os.path.join(output_dir, testid))
        output = sh.curl('http://cstar.datastax.com/tests/artifacts/{testid}/stats'.format(testid=testid)).stdout
        with open(stats_file, 'w') as f:
            f.write(output)
    try:
        stats = json.loads(output)
    except NameError:
        with open(stats_file, 'r') as f:
            stats = json.load(f)

    cfstats_data = [x for x in stats['stats'] if 'cfstats' in x['command']]
    for c in cfstats_data:
        print(c['revision'])
        map(print, ('\t' + line.strip() for line in c['output']['blade-11-2a'].splitlines()
                    if 'space used' in line.lower()))
        print()
