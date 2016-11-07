# DigitalWallet

## Summary
This is a program implementing features to prevent fraudulent payment requests from untrusted users. 
https://github.com/InsightDataScience/digital-wallet

## Details of implementation

The run.sh script implement the fraud detection algorithm with a python file antifraud.py.

The design of antifraud.py file's arguments involves the consideration of scalability.
There are at least 4 arguments for antifraud.py:

1. The first argument, batch_payment.txt, contains past data that can be used to track users who have previously paid one another. These transactions should be used to build the initial state of the entire user network.

2. The second argument, stream_payment.txt should be used to determine whether there's a possibility of fraud and a warning should be triggered.

3. From the third argument, each two arguments is a pair. The first one in the pair is the output file, and the second one in the pair is max_degree, which means this program warns users only when they're outside the "max_degree-th degree friends network".
 
 The difference between these 3 features is only max_degree value, therefore:

 * max_degree for Feature 1 should be 1

 * max_degree for Feature 2 should be 2

 * max_degree for Feature 3 should be 4

 More generally, the program can extend to any degree's social networks.

##Ideas of additional features
