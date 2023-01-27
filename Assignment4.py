# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 4 - Empirical Performance of String Search Algorithms
# Satar Hassni

# Acknowledgements:
# I followed the lecture
# I used the following sites: geeks4geeks

import Assignment2
import time
import numpy as np
import random


def native_search(text, pattern, verbose=False):
    return text.index(pattern)


# https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
def brute_force(text, pattern, verbose=False):
    m = len(pattern)
    n = len(text)
    for i in range(n - m + 1):
        j = 0
        while j < m:
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i
    return -1


# https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/
def rabin_karp(text, pattern, verbose=False):
    m = len(pattern)
    n = len(text)
    i = 0
    j = 0
    p = 0
    t = 0
    h = 1
    d = 256
    q = 101
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t:
            for j in range(m):
                if text[i + j] != pattern[j]:
                    break
                else:
                    j += 1
            if j == m:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
            if verbose:
                print("Rabin Karp: i = ", i, " t = ", t, " p = ", p)
    return -1


# https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
def knuth_morris_pratt(text, pattern, verbose=False):
    m = len(pattern)
    n = len(text)
    lps = knp_compute_lps_array(pattern)
    if verbose:
        print("KNP LPS Array is ", lps)
    j = 0
    i = 0
    while n - i >= m - j:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
def knp_compute_lps_array(pattern):
    m = len(pattern)
    lps = [0] * m
    len_lps = 0
    lps[0] = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[len_lps]:
            len_lps += 1
            lps[i] = len_lps
            i += 1
        else:
            if len_lps != 0:
                len_lps = lps[len_lps - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


# https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
def boyer_moore(text, pattern, verbose=False):
    m = len(pattern)
    n = len(text)
    bad_char = bm_bad_char(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    return -1


def bm_bad_char(pattern):
    size = len(pattern)
    no_of_chars = 256
    bad_char = [-1] * no_of_chars
    for i in range(size):
        bad_char[ord(pattern[i])] = i;
    return bad_char


def random_string(size):
    return "".join([chr(random.randint(65, 90)) for _ in range(size)])


def run_algs(algs, sizes, trials, pattern_length):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            text = random_string(size)
            idx = random.randint(0, size - pattern_length)
            pattern = text[idx: idx + pattern_length]
            for alg in algs:
                start_time = time.time()
                idx_found = alg(text, pattern, False)
                print(alg.__name__, pattern, idx_found)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def read_file(file_name):
    with open(file_name, "r") as file:
        text = file.read().strip()
        return text.upper()


def mini_test():
    verbose = False
    text = read_file("input/Assignment4_Text1.txt")
    patterns = read_file("input/Assignment4_Patterns.txt").split("\n")
    for pattern in patterns:
        pattern = pattern.upper()
        print("Text: ", text)
        print("Pattern: ", pattern)
        print("Native search: ", native_search(text, pattern, verbose))
        print("Brute Force: ", brute_force(text, pattern, verbose))
        print("Rabin Karp: ", rabin_karp(text, pattern, verbose))
        print("Knuth Morris Pratt: ", knuth_morris_pratt(text, pattern, verbose))
        print("Boyer moore: ", boyer_moore(text, pattern, verbose))


def main():
    assn = "Assignment4"
    sizes = [100, 1000, 10000, 100000]
    algs = [native_search, brute_force, rabin_karp, knuth_morris_pratt, boyer_moore]
    trials = 10
    for pattern_length in [4, 8, 12, 16]:
        title = "Runtime of String Search Algorithms for Pattern Length " + str(pattern_length)
        dict_algs = run_algs(algs, sizes, trials, pattern_length)
        Assignment2.print_times(dict_algs)
        Assignment2.plot_times(dict_algs, sizes, trials, algs, title, assn + ".png")
    # mini_test()


if __name__ == "__main__":
    main()
