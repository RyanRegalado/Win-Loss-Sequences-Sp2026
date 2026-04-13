import pandas as pd
from scipy.special import comb
from scipy.stats import ttest_ind
from statsmodels.stats.proportion import proportions_ztest
import ast
import math
import numpy as np


def prob(sequence):
    """
    Computes the win probability of a sequence as the proportion of wins.

    Parameters:
        sequence (list): A binary win/loss sequence (1 = win, 0 = loss).

    Returns:
        float: The fraction of wins in the sequence.
    """
    return sum(sequence) / len(sequence)


def split(sequence):
    """
    Splits a sequence into two halves, with the first half taking the extra
    game if the sequence length is odd.

    Parameters:
        sequence (list): A binary win/loss sequence.

    Returns:
        tuple: (s1, s2) where s1 is the first half and s2 is the second half.
    """
    n1 = math.ceil(len(sequence) / 2)
    s1 = sequence[:n1]
    s2 = sequence[n1:]
    return s1, s2


def c1(sequence, n2=None):
    """
    Computes the C1 collapse score using a binomial model (Method I).

    Models wins as i.i.d. Bernoulli trials with probability p equal to the
    overall win rate. Returns 1 divided by the probability of achieving k2 or
    fewer second-half wins under this model, where a higher score indicates a
    more extreme collapse.

    Parameters:
        sequence (list): A binary win/loss sequence.
        n2 (int, optional): Number of end-of-season games to treat as the
            second half. Defaults to the natural second half via split().

    Returns:
        float: The C1 collapse score. Returns inf if the binomial probability
            is zero.
    """
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


def c2(sequence, n2=None):
    """
    Computes the C2 collapse score using a two-proportion z-test (Method II).

    Tests whether the first-half win rate is significantly greater than the
    second-half win rate. Returns 1 divided by the one-sided p-value, so a
    higher score indicates a more statistically significant collapse.

    Parameters:
        sequence (list): A binary win/loss sequence.
        n2 (int, optional): Number of end-of-season games to treat as the
            second half. Defaults to the natural second half via split().

    Returns:
        float: The C2 collapse score. Returns inf if the p-value is zero.
    """
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

    _, p = proportions_ztest([k1, k2], [n1, n2], alternative="larger")

    return math.inf if p == 0 else 1 / p


def c1_argmax_n2(seq, n2):
    """
    Computes C1*(s) and n1*: the maximum C1 collapse score over all end-of-season
    window sizes from 1 to n2.

    Parameters:
        seq (list): A binary win/loss sequence.
        n2 (int): Maximum number of end-of-season games to consider.

    Returns:
        tuple: (n1_star, max_val) where n1_star is the window size achieving
            the maximum C1 score and max_val is that score.
    """
    n1_star = None
    max_val = -math.inf

    for n in range(1, n2 + 1):
        val = c1(seq, n)
        if val > max_val:
            max_val = val
            n1_star = n

    return n1_star, max_val


def c2_argmax_n2(seq, n2):
    """
    Computes C2*(s) and n2*: the maximum C2 collapse score over all end-of-season
    window sizes from 1 to n2.

    Parameters:
        seq (list): A binary win/loss sequence.
        n2 (int): Maximum number of end-of-season games to consider.

    Returns:
        tuple: (n2_star, max_val) where n2_star is the window size achieving
            the maximum C2 score and max_val is that score.
    """
    n2_star = None
    max_val = -math.inf

    for n in range(1, n2 + 1):
        val = c2(seq, n)
        if val > max_val:
            max_val = val
            n2_star = n

    return n2_star, max_val


def c3(sequence, N, n2=None, perms=None):
    """
    Computes the C3 collapse score using Monte Carlo simulation (Method III).

    Generates N random permutations of the sequence and counts how many
    produce a second-half win total <= the observed value k2. Returns N/M
    where M is that count, so a higher score indicates a more extreme collapse.
    A pre-generated permutation matrix can be supplied to share the same
    random shuffles across multiple calls (e.g. within c3_argmax_n2).

    Parameters:
        sequence (array-like): A binary win/loss sequence.
        N (int): Number of random permutations to generate.
        n2 (int, optional): Number of end-of-season games to treat as the
            second half. Defaults to the natural second half via split().
        perms (np.ndarray, optional): A pre-generated (N, L) integer index
            matrix representing N permutations. If None, a new matrix is
            generated internally.

    Returns:
        float: The C3 collapse score. Returns inf if no permutation produced
            a second-half win total <= k2.
    """
    sequence = np.asarray(sequence)
    L = len(sequence)

    if n2 is None:
        _, s2 = split(sequence)
        k2 = np.sum(s2)
    else:
        k2 = np.sum(sequence[L - n2:])

    if perms is None:
        perms = np.argsort(np.random.rand(N, L), axis=1)

    tail_idx = perms[:, -n2:]
    tail_sums = sequence[tail_idx].sum(axis=1)
    M = np.sum(tail_sums <= k2)

    return N / M if M != 0 else math.inf


def c3_argmax_n2(seq, N):
    """
    Computes C3*(s) and n3*: the maximum C3 collapse score over all end-of-season
    window sizes from 1 to n//2 (reference implementation).

    Generates a single shared permutation matrix and passes it to c3 for each
    window size, ensuring all scores are evaluated against the same set of
    random shuffles. This is the readable reference implementation; for large
    N or long sequences prefer c3_argmax_n2_fast.

    Parameters:
        seq (array-like): A binary win/loss sequence.
        N (int): Number of random permutations to use.

    Returns:
        tuple: (n3_star, max_val) where n3_star is the window size achieving
            the maximum C3 score and max_val is that score.
    """
    seq = np.asarray(seq)
    L = len(seq)
    n2_max = L // 2

    perms = np.argsort(np.random.rand(N, L), axis=1)

    scores = []
    for n2 in range(1, n2_max + 1):
        score = c3(seq, N, n2=n2, perms=perms)
        scores.append(score)

    best_idx = int(np.argmax(scores))
    best_n2 = best_idx + 1
    best_score = scores[best_idx]

    return best_n2, float(best_score)

def c3_argmax_n2_fast(seq, N):
    """
    Computes C3*(s) and n3*: the maximum C3 collapse score over all end-of-season
    window sizes from 1 to n//2 (optimised implementation).

    Inlines the c3 logic directly and uses a single shared permutation matrix
    across all window sizes, avoiding repeated function call overhead. Preferred
    over c3_argmax_n2 for large N or long sequences.

    Parameters:
        seq (array-like): A binary win/loss sequence.
        N (int): Number of random permutations to use.

    Returns:
        tuple: (n3_star, max_val) where n3_star is the window size achieving
            the maximum C3 score and max_val is that score.
    """
    seq = np.asarray(seq)
    L = len(seq)
    n2 = L // 2

    c3_vec = np.full(n2, math.inf)

    perms = np.argsort(np.random.rand(N, L), axis=1)

    for n in range(1, n2 + 1):
        k2 = np.sum(seq[L - n:])
        tail_idx = perms[:, -n:]
        tail_sums = seq[tail_idx].sum(axis=1)
        M = np.sum(tail_sums <= k2)
        c3_vec[n - 1] = N / M if M != 0 else math.inf

    best = int(np.argmax(c3_vec))
    return best + 1, float(c3_vec[best])