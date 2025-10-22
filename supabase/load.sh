#!/bin/bash

set -eu

# Load data: wrap TRUNCATE and \copy FREEZE in a single transaction
# If we dont' do this, Postgres will throw an error:
#     "ERROR: cannot perform COPY FREEZE because the table was not created or truncated in the current subtransaction"
# (i.e. Postgres requires that the table be either created or truncated in the current subtransaction)
psql -h ${SUPABASE_HOST} -p 5432 -U postgres -d test <<'EOF'
set statement_timeout = '60min';
BEGIN;
TRUNCATE TABLE hits;
\copy hits FROM 'hits.tsv' with freeze;
COMMIT;
EOF

psql -h ${SUPABASE_HOST} -p 5432 -U postgres -d test -t -c 'VACUUM ANALYZE hits'
