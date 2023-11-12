# db-bench - Database Performance Benchmarking 

This repository contains utility scripts to easily measure the performance of 
popular high-performance database runtimes.

It is a variation of the reproducibility infrastructure of [inkfuse](https://github.com/wagjamin/inkfuse/tree/main/reproduce).

## How to Run?
If you simply want to generate data at SF `k` for every system we support, run:
```
./reproduce_all.sh <k>
```
This runs all queries and creates plots in `/plots/sf_<k>.pdf`.

You can be more fine-grained in what you are reproducing as well.
If you for example want to reproduce DuckDB at SF0.1, simply run:
```
pip3 install -r requirements.txt
./reproduce_duckdb.py 0.1
./plot.py 0.1 duckdb
```
This runs all queries and creates a plot in `/plots/sf_0.1.pdf`.

## Example Plot
You can find an example plot in `example_plots`. The plots are bar plots for all TPC-H queries:

![](example_plots/sf_0.1.png)

## Running on your Macbook
On MacOS, we currently only support running the DuckDB reproductions.
You also need to explicitly invoke the script with Python 3.

Run the following to e.g. reproduce DuckDB on SF0.1.
```
pip3 install -r requirements.txt
python3 reproduce_duckdb.py 0.1
python3 plot.py 0.1 duckdb
```

