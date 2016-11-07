# DigitalWallet

## Summary
This is a program implementing features to prevent fraudulent payment requests from untrusted users. 
https://github.com/InsightDataScience/digital-wallet

## Details of implementation

The `run.sh` script implement the fraud detection algorithm with a python file `antifraud.py`.

The design of `antifraud.py` file's arguments involves the consideration of scalability.
There are at least 4 arguments for `antifraud.py`:

1. The first argument, `batch_payment.txt`, contains past data that can be used to track users who have previously paid one another. These transactions should be used to build the initial state of the entire user network.

2. The second argument, `stream_payment.txt` should be used to determine whether there's a possibility of fraud and a warning should be triggered.

3. From the third argument, each two arguments is a pair. The first one in the pair is the output file, and the second one in the pair is `max_degree`, which means this program warns users only when they're outside the "`max_degree`-th degree friends network".
 
 The difference between these 3 features is only `max_degree` value, therefore:

 * `max_degree` for Feature 1 should be 1

 * `max_degree` for Feature 2 should be 2

 * `max_degree` for Feature 3 should be 4

 More generally, the program can extend to any degree's social networks.

The `antifraud.py` file mainly implements the following tasks:

1. Build "friends network" based on payment data in `batch_payment.txt`. The "friends network" is an undirected graph, each node represents an user, and each edge represents a payment between two users. Hashmap (Dictionary in python) is used as the data structure for storing the "friends network". The key is a userID and the value is a set of its neighbors' userIDs.

2. Extract payment information from `stream_payment.txt`. The fields in the payment record we only care about is IDs of users making/receiving the payment. So `time`, `amount` and `message` fields are ignored. All payment information is stored in a list. Each payment is represented as a tuple (`userID1`, `userID2`).

3. For each payment record, check whether one user can reach the other user within max_degree steps. BFS (Breadth-first search) is used to implement the fraud detection algorithm. If one user is outside the "friends network" (has no payment record before, in other words, not a key in hashmap) or cannot reach the other user within max_degree steps, then this payment is unverified.

##Ideas of additional features

There are additional features that might be useful to prevent fraudulent payments based on what data we have. One idea is comparing sequences of transactions (their amount or frequency) to detect a change in behaviour for a particular user. Another idea is doing semantic analysis on the `message` field, and detect suspicious words.
