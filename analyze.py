"""
Usage: analyze.py [--id TESTID] [-o OUTPUT_DIR] [-f]

-o OUTPUT_DIR  # output directory
-f             # force download data. overwrites cached data
--id TESTID    # optionally provide an id for cstar perf
               # if not provided, use the currently-running cluster on ccm
"""
from __future__ import print_function

import json
import os
import sys
from pprint import pprint
from uuid import uuid4

import sh
from docopt import docopt

sh.ErrorReturnCode.truncate_cap = 999999


def get_space_used_lines(s):
    for line in [x for x in s.splitlines() if 'space used' in x.lower()]:
        yield line.strip()


if __name__ == '__main__':
    args = docopt(__doc__)
    pprint(args)
    testid = args['--id'] or 'local-{}'.format(uuid4())
    force = args['-f']

    output_dir = os.path.join(args['-o'] or 'output',
                              testid)
    stats_file = os.path.join(output_dir, 'stats.json')

    if args['--id']:  # if we're looking at cstar_perf
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
        for datum in cfstats_data:
            print('Revision:')
            print('\t{}:'.format(datum['label']), datum['revision'])

            command_sequence = [x['command'] for x in stats['stats']
                                if (x['revision'], x['label']) == (datum['revision'], datum['label'])]
            print('Commands:')
            for cmd in command_sequence:
                print('\t' + cmd)

            print('Results:')
            map(print, ('\t' + line for line in
                        get_space_used_lines(datum['output']['blade-11-2a'])))
            print()

    else:  # if we're looking locally
        # for version in ('github:mambocab/with-JAVA-571-driver', 'git:cassandra-2.2'):
            # try:
            #     print(sh.ccm.remove())
            # except:
            #     pass
            # print(sh.ccm.create('test-with-{}'.format(version.split(':')[1].split('/')[-1]),
            #                     '-v', version, '-n', '3'))
            # print(sh.ccm.start('--wait-for-binary-proto', _err=sys.stdout))
            # stress = sh.ccm.stress.bake('user profile=https://raw.githubusercontent.com/mambocab/'
            #                             'cstar_perf/row-format-tests/regression_suites/long_names.yaml '
            #                             'n=3M ops(insert=1) '
            #                             # '-rate threads=50'
            #                             )
            # print(stress)
            # print(stress(_err=sys.stdout))
            cfstats = sh.ccm.node1.nodetool.cfstats.bake('keyspace1.standard1')
            print('ccm command: {}'.format(cfstats))
            print('c* version: {}'.format(sh.ccm.node1.nodetool.version().strip()))
            map(print, get_space_used_lines(cfstats()))
