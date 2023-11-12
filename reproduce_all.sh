#!/bin/bash

if [[ $# < 1 ]]; then
  echo "Run as ./generate_tpch.sh <scale factor>" 
  exit 1
fi

# Install requirements.
pip3 install -r requirements.txt

# Benchmark DuckDB
echo "Reproducing DuckDB"
./reproduce_duckdb.py $1

# Benchmark Umbra
echo "Reproducing Umbra"
./reproduce_umbra.sh $1

# Generate Plots
echo "Generating Plots"
./plot.py $1 duckdb umbra_adaptive umbra_optimized

echo "Result plots can be found in plots/sf_${1}.pdf"

