#!/bin/bash
# File: testing/run_dieharder.sh

mkdir -p diehard_results

TESTS=(0 2 9 10 100)  # birthdays, rank, sums, runs, monobit

for file in diehard_inputs/*.bin; do
    base=$(basename "$file" .bin)
    outfile="diehard_results/${base}_results.txt"
    echo "[→] Testing $base..." > "$outfile"
    for test_id in "${TESTS[@]}"; do
        echo "Running test -d $test_id..." >> "$outfile"
        dieharder -d $test_id -g 201 -f "$file" >> "$outfile"
    done
    echo "[✔] All selected tests complete for $base"
done
