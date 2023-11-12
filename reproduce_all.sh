#!/bin/bash

# Install requirements.
pip3 install -r requirements.txt

# Benchmark DuckDB
echo "Reproducing DuckDB"
./reproduce_duckdb.py 0.1
./reproduce_duckdb.py 1
./reproduce_duckdb.py 10

# Benchmark Umbra
echo "Reproducing Umbra"
./reproduce_umbra.sh 0.1
./reproduce_umbra.sh 1
./reproduce_umbra.sh 10

# Generate Plots
echo "Generating Plots"
./plot.py 1 duckdb umbra_adaptive umbra_optimized
./plot.py 10 duckdb umbra_adaptive umbra_optimized

echo "Result plots can be found in `plots`"

