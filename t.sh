for v in git:trunk git:cassandra-2.2 ; do
  for c in 100 500 1000 ; do
    set -x
    set +e
    ccm remove
    set -e
    ccm create trunk-long-column-names -n 3 -v $v
    ccm start --wait-for-binary-proto
    # ccm stress -- user 'profile=long_names.yaml' n=500K ops\(insert=1\) -rate threads=10
    ccm stress -- write n=500K -rate threads=5 -col n=FIXED\($c\)
    python analyze.py
  done
done
