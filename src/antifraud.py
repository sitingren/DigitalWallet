# Copyright (c) 2021, Siting Ren <ren_siting@hotmail.com>
# All rights reserved.

# Author: Siting Ren
# Version: 11/06/2016
# Description: This program detects unverified payments.

import sys
import os.path
import Queue


def buildNetwork(batch_payment_file):
    """
        Open batch_payment_file and extract two user IDs from each payment.
        Use a hashmap to store neighborhood information for each user ID.
    """
    # key: a user ID   value: a set of its neighbors IDs
    network = {}

    with open(batch_payment_file, "r") as f:
        f.readline() # skip the header
        for line in f:
            cell = line.strip().split(',')
            id1 = cell[1].strip()
            id2 = cell[2].strip()
            if id1 not in network:
                network[id1] = set()
            if id2 not in network:
                network[id2] = set()
            network[id1].add(id2)
            network[id2].add(id1)
    return network


def getPayments(stream_payment_file):
    """
        Open stream_payment_file and extract two user IDs from each payment.
        Store each payment as a tuple (userID1, userID2).
    """
    payments = []
    with open(stream_payment_file, "r") as f:
        f.readline() # skip the header
        for line in f:
            cell = line.strip().split(',')
            id1 = cell[1].strip()
            id2 = cell[2].strip()
            payments.append((id1, id2))
    return payments


def detectDegrees(network, s, t, max_degree):
    """
        Given the network, two user IDs and max_degree,
        check whether one user can reach the other user within max_degree steps.
    """
    # Corner cases
    if s == t:
        return "trusted\n"
    # the node is isolated
    if s not in network or t not in network:
        return "unverified\n"

    # BFS
    queue = Queue.Queue()
    queue.put(s)
    visited = set()
    visited.add(s)
    level = 0
    while not queue.empty():
        level += 1
        if level > max_degree:
            break
        size = queue.qsize()
        for i in xrange(size):
            head = queue.get()
            # find user t within max_degree steps.
            if t in network[head]:
                return "trusted\n"
            for n in network[head]:
                if n not in visited:
                    queue.put(n)
                    visited.add(n)
    return "unverified\n"


def detectFraud(network, payments, paymo_output_file, max_degree):
    """
        Call detectDegrees function to detect suspicious payments and
        output a line containing one of two words, trusted or unverified, 
        for each payment.
    """
    with open(paymo_output_file, "w") as fout:       
        for id1, id2 in payments:
            fout.write(detectDegrees(network, id1, id2, max_degree))
    

if __name__ == "__main__":
    # Call format should be:
    #   python antifraud.py <paymo_input_batch_payment_file> 
    #       <paymo_input_stream_payment_file> 
    #       <paymo_output_file1> <max_degree1>
    #       [<paymo_output_file2> <max_degree2> ...]
     
    if len(sys.argv) < 5 or (len(sys.argv) - 3) % 2 == 1:
        sys.stderr.write("Usage: python antifraud.py <paymo_input_batch_payment_file>\n\t" + \
            "<paymo_input_stream_payment_file>\n\t<paymo_output_file1> <max_degree1>\n\t" + \
            "[<paymo_output_file2> <max_degree2> ...]\n")
        sys.exit()
 
    batch_payment_file = sys.argv[1]
    if not os.path.isfile(batch_payment_file):
        sys.stderr.write('Operation failed: No such file: %s\n' % batch_payment_file)
        sys.exit()

    stream_payment_file = sys.argv[2]
    if not os.path.isfile(stream_payment_file):
        sys.stderr.write('Operation failed: No such file: %s\n' % stream_payment_file)
        sys.exit()

    network = buildNetwork(batch_payment_file)
    payments = getPayments(stream_payment_file)

    for i in xrange(3, len(sys.argv), 2):
        paymo_output_file = sys.argv[i]
        try:
            max_degree = int(sys.argv[i + 1])
        except ValueError as e:
            sys.stderr.write('Operation failed: %s\n' % e)
            continue
        detectFraud(network, payments, paymo_output_file, max_degree)

        
