#! /usr/bin/python3

import duckdb
import argparse
import subprocess
import os
import time

def load_query(q_name):
    with open(f'tpch/{q_name}.sql') as query:
        return query.read()


def set_up_schema(con):
    print('Setting up schema')
    schema_q = load_query('schema')
    con.execute(schema_q)


def load_data(con):
    tables = [
            'part',
            'supplier',
            'partsupp',
            'customer',
            'orders',
            'lineitem',
            'nation',
            'region'
            ]
    for table in tables:
        print(f'Loading {table}')
        con.execute(f"INSERT INTO {table} SELECT * FROM read_csv_auto('data/{table}.tbl', delim='|', header=False)")


def run_query(con, query):
    query = load_query(query)
    t_start = time.time()
    con.execute(query)
    t_end = time.time()
    return int(1000 * (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Benchmark DuckDB')
    parser.add_argument('scale_factor', type=str, help='The factor to run the experiment on')
    parser.add_argument('--repeat', type=int, default=10, help='How often should each query be run?')
    parser.add_argument('--no-regen', dest='regen', action='store_false', help="Don't regenerate data")
    parser.set_defaults(regen=True)
    args = parser.parse_args()

    if args.regen:
        # Generate the data. Trailing | generated by dbgen are stripped.
        ret = subprocess.run(['bash', 'generate_tpch.sh', args.scale_factor, 'duckdb'])
        assert ret.returncode == 0

    # Set up the schema and load data.
    con = duckdb.connect(database=':memory:')
    set_up_schema(con)
    load_data(con)

    with open(f'result_duckdb_{args.scale_factor}.csv', 'w') as results:
        # Run the queries.
        for file in os.listdir('tpch'):
            if file != 'schema.sql' and file != 'load.sql':
                q_name = file[:-4]
                print(f'Reproducing q{q_name} on DuckDB')
                for _ in range(args.repeat):
                    dur = run_query(con, q_name)
                    # Last item is always 0, since DuckDB is never stalled on compilation.
                    results.write(f'duckdb,{q_name},{args.scale_factor},{dur},0\n')

