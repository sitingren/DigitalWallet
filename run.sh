#!/usr/bin/env bash

# the run script for running the fraud detection algorithm with a python file

# Arguments for antifraud.py program:
# The first argument, batch_payment.txt, contains past data that can be used to track users who have previously paid one another. These transactions should be used to build the initial state of the entire user network.
# The second argument, stream_payment.txt should be used to determine whether there's a possibility of fraud and a warning should be triggered.
# From the third argument, each two arguments is a pair. 
# The first one in the pair is the output file, and the second one in the pair is max_degree, which means this program warns users only when they're outside the "max_degree-th degree friends network".
# max_degree for Feature 1 should be 1
# max_degree for Feature 2 should be 2
# max_degree for Feature 3 should be 4
# More generally, the program can extend to any degree's social networks.

python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt 1 ./paymo_output/output2.txt 2 ./paymo_output/output3.txt 4
