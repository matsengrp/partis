#!/usr/bin/env python
from subprocess import check_call, Popen
import sys
sys.path.insert(1, './python')
import os
import csv

from clusterpath import ClusterPath
import utils

def run_cluster(cl, iclust=None):
    cmd = './bin/run-driver.py --label ' + label + ' --action run-viterbi --is-data --datafname VRC01_heavy_chains-dealigned.fasta'  # --simfname ' + os.path.dirname(infname) + '/simu-foo-bar.csv'
    # cmd += ' --outfname '
    extras = ['--n-sets', len(cl), '--queries', ':'.join(cl), '--debug', 1, '--sw-debug', 0, '--n-procs', 1, '--n-best-events', 1]
    cmd += utils.get_extra_str(extras)
    print cmd
    # check_call(cmd.split())
    Popen(cmd + ' >_tmp/chaim/' + str(iclust) + '.csv', shell=True)

label = 'chaim-test'
# infname = '/fh/fast/matsen_e/dralph/work/partis-dev/_output/' + label + '/partitions.csv'
infname = 'chaim.csv'

cp = ClusterPath(-1)
cp.readfile(infname)

print '---> annotations for clusters in best partition:'
iclust = 0
for cluster in cp.partitions[cp.i_best]:
    run_cluster(cluster, iclust)
    iclust += 1
    # sys.exit()
    # if iclust > 3:
    #     break

sys.exit()

for ipart in range(cp.i_best, cp.i_best + 10):
    if ipart >= len(cp.partitions):
        break
    print '---> annotation for intersection of partitions %d and %d:' % (ipart - 1, ipart)
    cp.print_partition(ipart - 1)
    cp.print_partition(ipart)

    parents = cp.get_parent_clusters(ipart)
    if parents is None:
        print '   skipping synthetic rewind step'
        continue
    run_cluster(parents[0] + parents[1])