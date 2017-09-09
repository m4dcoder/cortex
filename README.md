# cortex

### Database Setup
 1. Follow instructions at https://www.cockroachlabs.com/docs/stable/install-cockroachdb.html to install CockroachDB.
 2. Setup certificate to encrypt network communication.  Copy the certificate directory to `${HOME}/.cockroach-certs`.  The `cockroach` command uses this directory by default for the `--certs-dir` option.
 3. Setup CockroachDB to run as background service.  On Ubuntu 16.04, copy `./etc/cockroachdb.service` in this project to `/lib/systemd/system` on the system. Copy the certs directory to `/etc/cockroachdb`.  Start the `cockroachdb` service.
 4. Setup the database and user for this project.
```
cockroach user set brainaic --password
cockroach sql -e 'CREATE DATABASE cortex'
cockroach sql -e 'GRANT ALL ON DATABASE cortex TO brainiac'
