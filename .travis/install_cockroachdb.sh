#!/bin/bash
cd /tmp
wget -qO- https://binaries.cockroachdb.com/cockroach-v1.0.5.linux-amd64.tgz | tar xvz
cp -i cockroach-v1.0.5.linux-amd64/cockroach /tmp
/tmp/cockroach start --insecure --host=localhost > /tmp/cockroachdb.log 2>&1 &
while [[ -z `grep nodeID /tmp/cockroachdb.log` ]]; do sleep 1; done
/tmp/cockroach user set brainaic --insecure
/tmp/cockroach sql --insecure -e 'CREATE DATABASE cortex'
/tmp/cockroach sql --insecure -e 'GRANT ALL ON DATABASE cortex TO brainiac'
