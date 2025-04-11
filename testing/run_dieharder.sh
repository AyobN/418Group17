#!/bin/bash
# File: testing/run_dieharder.sh

mkdir -p diehard_results

for file in diehard_inputs/*.bin; do
    base=$(basename "$file" .bin)
    echo "[→] Testing $base..."
    dieharder -a -g 201 -f "$file" > "diehard_results/${base}_results.txt"
    echo "[✔] Results saved to diehard_results/${base}_results.txt"
done
