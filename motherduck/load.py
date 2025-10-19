#!/usr/bin/env python3

import duckdb
import timeit
import psutil

## TODO: delete this

con = duckdb.connect(database="md:", read_only=False)
# ELENA PUT IT BACK
#con.execute('CREATE OR REPLACE DATABASE clickbench')
con.execute('USE clickbench')

# disable preservation of insertion order
con.execute("SET preserve_insertion_order=false")

# perform the actual load
start = timeit.default_timer()
# con.execute(open("create.sql").read())
file = '''https://datasets.clickhouse.com/hits_compatible/hits.parquet'''
# The parquet file doen't have the timestamps as timestamps, so we
# need to coerce them into proper timestamps.
# con.execute(f"""
#     INSERT INTO hits
#     SELECT *
#     REPLACE
#     (epoch_ms(EventTime * 1000) AS EventTime,
#      epoch_ms(ClientEventTime * 1000) AS ClientEventTime,
#      epoch_ms(LocalEventTime * 1000) AS LocalEventTime,
#      DATE '1970-01-01' + INTERVAL (EventDate) DAYS AS EventDate)
#     FROM read_parquet('{file}', binary_as_string=True)
#      """)
end = timeit.default_timer()
print(f"\t\"load_time\": \"${round(end - start, 3)}\"")

print('\t"Data size": ', end='')
# Print the database size. For MotherDuck, we get a formatted string.
result = con.execute("""
   SELECT database_size
   FROM pragma_database_size()
   WHERE database_name = 'clickbench'
   """).fetchone()

if result and result[0]:
    size_str = result[0]
    # Parse the size string (e.g., "22.0 GiB", "100 MB", "0 bytes")
    parts = size_str.split()
    if len(parts) == 2:
        value = float(parts[0])
        unit = parts[1].lower()

        # Convert to bytes
        multipliers = {
            'bytes': 1,
            'byte': 1,
            'kb': 1024,
            'kib': 1024,
            'mb': 1024**2,
            'mib': 1024**2,
            'gb': 1024**3,
            'gib': 1024**3,
            'tb': 1024**4,
            'tib': 1024**4
        }

        bytes_value = int(value * multipliers.get(unit, 1))
        print(bytes_value)
    else:
        print(size_str)
else:
    print(0)

