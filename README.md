# db-bench - Performance Benchmarking of Single-Node Runtimes

This repository contains utility scripts to easily measure the performance of 
popular high-performance database runtimes.

It is a variation of the reproducibility infrastructure of [inkfuse](https://github.com/wagjamin/inkfuse/tree/main/reproduce).

## How to Run?
If you simply want to generate data at SF1 and SF10 for every system we support, run:
```
./reproduce_all.sh
```
This runs all queries and creates plots in `/plots/sf_{1|10}.pdf`.

You can be more fine-grained in what you are reproducing as well.
If you for example want to reproduce DuckDB at SF0.1, simply run:
```
pip3 install -r requirements.txt
./reproduce_duckdb.py 0.1
python3 plot.py 0.1 duckdb
```
This runs all queries and creates a plot in `/plots/sf_0.1.pdf`.

## Running on your Macbook
On MacOS, we currently only support running the DuckDB reproductions.
You also need to explicitly invoke the script with Python 3.

Run the following to e.g. reproduce DuckDB on SF0.1.
```
pip3 install -r requirements.txt
python3 reproduce_duckdb.py 0.1
python3 plot.py 0.1 duckdb
```

