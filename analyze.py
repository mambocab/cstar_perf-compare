"""
Usage: analyze.py <testid> [-o OUTPUT_DIR]

-o OUTPUT_DIR  # output directory
"""
from __future__ import print_function

import os

import sh
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    testid = args['<testid>']
    output_dir = os.path.join(args['-o'] or 'output',
                              testid)

    unpacked_dir = os.path.join(output_dir, 'cassandra_logs.{testid}'.format(testid=testid))

    stats_filename_trunk, stats_filename_2_2 = (os.path.join(unpacked_dir, revision_dir, 'blade-11-2a', )
                                                for revision_dir in
                                                ('revision_01', 'revision_02'))

    sh.mkdir('-p', os.path.join(output_dir, testid))
    sh.tar(
        sh.curl('http://cstar.datastax.com/tests/artifacts/{testid}/stats'.format(testid=testid)),
        '-zxv',
        '-C', output_dir
    )
