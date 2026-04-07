import pandas as pd
from scipy.special import comb
from scipy.stats import ttest_ind
from statsmodels.stats.proportion import proportions_ztest
import ast
import math
import numpy as np

def prob(sequence):
    return sum(sequence) / len(sequence)

def split(sequence):

    n1 = math.ceil(len(sequence) / 2)

    s1 = sequence[:n1] # includes the first n1 elements
    s2 = sequence[n1:] # the rest of the elements

    return s1,s2

### Returns Model 1 metric. Sequence is type list. n2 is type int (defaults to second half).

def c1(sequence, n2=None):
    if n2 is None:
        _, s2 = split(sequence) 
        n2 = len(s2)
        k2 = sum(s2)
    else:
        s2 = sequence[len(sequence) - n2:]
        k2 = sum(s2)

    p = prob(sequence)

    sum_ = 0
    for i in range(k2 + 1):
        sum_ += comb(n2, i) * p**i * (1-p)**(n2-i)

    return 1 / sum_ if sum_ > 0 else float('inf')

### Returns Model 2 metric. Sequence is type list. n2 is type int (defaults to second half).
    
def c2(sequence, n2=None):
    if n2 is None:
        s1, s2 = split(sequence)
        k1 = sum(s1)
        k2 = sum(s2)
        n1 = len(s1)
        n2 = len(s2)
    else:
        s1 = sequence[:len(sequence) - n2]
        s2 = sequence[len(sequence) - n2:]
        k1 = sum(s1)
        k2 = sum(s2)
        n1 = len(s1)

    _, p = proportions_ztest([k1, k2], [n1, n2], alternative = "larger")

    if (p == 0):
        return math.inf
    else:
        return 1 / p
    
def c3(sequence, N, n2=None):

    sequence = np.asarray(sequence)
    M = 0

    if n2 is None:
        _, s2 = split(sequence)
        k2 = np.sum(s2)
    else:
        k2 = np.sum(sequence[len(sequence) - n2:])

    for _ in range(N):
        shuffled = np.random.permutation(sequence)
        if n2 is None:
            _, tmp = split(shuffled)
        else:
            tmp = shuffled[len(shuffled) - n2:]

        if np.sum(tmp) <= k2:
            M += 1

    return N / M if M != 0 else math.inf

def c1_argmax_n2(seq, n2):
    candidates = range(1, n2 + 1)

    n1_star = None
    max_val = -math.inf

    for n in candidates:
        val = c1(seq, n)

        if val > max_val:
            max_val = val
            n1_star = n

    return n1_star, max_val

def c2_argmax_n2(seq, n2):
    candidates = range(1, n2 + 1)

    n2_star = None
    max_val = -math.inf

    for n in candidates:
        val = c2(seq, n)

        if val > max_val:
            max_val = val
            n2_star = n

    return n2_star, max_val

### Returns Model 3 metric. Sequence is type list. N is type int. n2 is type int (defaults to second half).


def c3_argmax_n2(seq, N):
    seq = np.asarray(seq)
    L = len(seq)
    n2 = L // 2

    c3_vec = np.full(n2, math.inf)

    for n in range(1, n2 + 1):
        # Observed second-half sum for this split
        k2 = np.sum(seq[L - n:])

        # N random permutations, take the last n elements as the "second half"
        idx = np.argpartition(np.random.rand(N, L), L - n, axis=1)[:, L - n:]
        tail_sums = seq[idx].sum(axis=1)   # shape (N,)

        # M = permutations with second-half sum <= observed k2
        M = np.sum(tail_sums <= k2)
        c3_vec[n - 1] = N / M if M != 0 else math.inf

    best = int(np.argmax(c3_vec))
    return best + 1, float(c3_vec[best])


def c3_argmax_n2_fast(seq, N):
    seq = np.asarray(seq)
    L = len(seq)
    n2 = L // 2

    c3_vec = np.full(n2, math.inf)

    # Generate N random permutations (rows)
    perms = np.argsort(np.random.rand(N, L), axis=1)

    # Observed second-half sums for each n will be computed in loop
    for n in range(1, n2 + 1):
        # Observed second-half sum
        k2 = np.sum(seq[L - n:])

        # Row-wise indexing: take last n elements of each permutation
        tail_idx = perms[:, -n:]              # shape (N, n)

        # Efficient sum using indexing
        tail_sums = seq[tail_idx].sum(axis=1)  # shape (N,)

        # Count how many satisfy condition
        M = np.sum(tail_sums <= k2)

        c3_vec[n - 1] = N / M if M != 0 else math.inf

    best = int(np.argmax(c3_vec))
    return best + 1, float(c3_vec[best])
