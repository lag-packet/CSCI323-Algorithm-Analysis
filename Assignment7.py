# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 6 - Empirical Performance of Graph Shortest Path Algorithms
# Satar Hassni

# Acknowledgements:
# I followed the lecture
# I used the following sites: geeks4geeks

import Assignment2
import time
import random
import numpy as np
import copy


def random_graph(num_vertices, max_cost):
    cm = [[0] * num_vertices for i in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i == j:
                cm[i][j] = max_cost + 1
            else:
                cm[i][j] = random.randint(1, max_cost)
    return cm


def init_dist(matrix):
    dist = copy.deepcopy(matrix)
    for i in range(len(dist)):
        dist[i][i] = 0
    return dist

def floyd_apsp(matrix):
    n = len(matrix)
    dist = init_dist(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


def bellman_apsp(matrix):
    n = len(matrix)
    dist = init_dist(matrix)
    for i in range(n):

    dist = [float("Inf")] * self.V
    dist[src] = 0

    for _ in range(self.V - 1):

        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graph contains negative weight cycle")
                return
        self.printArr(dist)


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


def mini_test():
    n = 10
    matrix = random_graph(n, 99)
    dist = floyd_apsp(matrix)
    print_matrix(matrix)
    print_matrix(dist)


def print_matrix(matrix):
    print(np.array(matrix))


def main():
    assn = "Assignment7"
    # sizes = [100, 1000, 10000, 100000]
    # algs = [native_search, brute_force, rabin_karp, knuth_morris_pratt, boyer_moore]
    # trials = 10
    # title = "Runtime of String Search Algorithms"
    # dict_algs = run_algs(algs, sizes, trials)
    # Assignment2.print_times(dict_algs)
    # Assignment2.plot_times(dict_algs, sizes, trials, algs, title, assn + ".png")
    mini_test()


if __name__ == "__main__":
    main()
