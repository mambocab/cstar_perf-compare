for v in git:trunk git:cassandra-2.2 ; do
  set -x
  ccm remove
  ccm create trunk-long-column-names -n 3 -v $v
  ccm start --wait-for-binary-proto
  ccm stress -- user 'profile=long_names.yaml' n=500K ops\(insert=1\) -rate threads=10
  python analyze.py
done
