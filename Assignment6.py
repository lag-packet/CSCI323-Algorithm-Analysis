# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 6 - Empirical Performance of Search Structures
# Satar Hassni

# Acknowledgements:
# I followed the lecture
# I used the following sites: geeks4geeks

import Assignment2
import time
import random


def display_hash(hash_table):
    for i in range(len(hash_table)):
        print(i, hash_table[i])
    print()


def hash_chaining_build(arr):
    size = int(len(arr) / 10)
    hash_table = [[] for _ in range(size)]
    for key in arr:
        hash_key = hash_function(key, size)
        hash_table[hash_key].append(key)
    return hash_table


def hash_probing_build(arr):
    size = len(arr) * 2
    hash_table = [None for _ in range(size)]
    for key in arr:
        hash_key = hash_function(key, size)
        i = 0
        while hash_table[hash_key]:  # collision
            i += 1
            hash_key = hash_function_probing(hash_key, size, i)
        hash_table[hash_key] = key
    return hash_table


def hash_function(key, size):
    return key % size


def hash_chaining_search(hash_table, arr):
    size = len(hash_table)
    found = [False] * len(arr)
    for j in range(len(arr)):
        key = arr[j]
        hash_key = hash_function(key, size)
        for item in hash_table[hash_key]:
            if item == key:
                found[j] = True
                break
    return found


def hash_probing_search(hash_table, arr):
    size = len(hash_table)
    found = [False] * len(arr)
    for j in range(len(arr)):
        key = arr[j]
        hash_key = hash_function(key, size)
        i = 0
        while hash_table[hash_key] != key:
            i += 1
            hash_key = hash_function_probing(hash_key, size, i)
        found[j] = True
    return found


def hash_function_probing(hash_key, size, i):
    a, b, c = 5, 7, 9
    hash_key = (hash_key + a * i ** 2 + b * i + c) % size
    return hash_key


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            text = random_string(size)
            idx = random.randint(0, size - 5)
            pattern = text[idx: idx + 5]
            for alg in algs:
                start_time = time.time()
                idx_found = alg(text, pattern, False)
                print(alg.__name__, pattern, idx_found)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def random_list(size):
    arr = [i ** 3 for i in range(size)]
    random.shuffle(arr)
    return arr


def mini_test():
    size = 100
    arr = random_list(size)
    ht_chaining = hash_chaining_build(arr)
    ht_probing = hash_probing_build(arr)
    display_hash(ht_chaining)
    display_hash(ht_probing)
    random.shuffle(arr)
    found = hash_chaining_search(ht_chaining, arr)
    print("hashing chaining search ")
    print(found)
    found = hash_probing_search(ht_probing, arr)
    print("hashing probing search ")
    print(found)

def big_test():
    pass


# sizes = [100, 1000, 10000, 100000]
# algs = [native_search, brute_force, rabin_karp, knuth_morris_pratt, boyer_moore]
# trials = 10
# title = "Runtime of String Search Algorithms"
# dict_algs = run_algs(algs, sizes, trials)
# Assignment2.print_times(dict_algs)
# Assignment2.plot_times(dict_algs, sizes, trials, algs, title, assn + ".png")


def main():
    assn = "Assignment6"
    # big_test()
    mini_test()


if __name__ == "__main__":
    main()
