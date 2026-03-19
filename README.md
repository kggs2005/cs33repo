# CS 33 Algorithm Repository

## This repository is a work in progress.

- This repository contains Python implementations of algorithms in CS 33 so far.
- This repository will NOT include data structures that would usually be made in C, such as treaps, AVL trees, and persistent data structures.

## Table of Contents

## LE 1

### Minimum Spanning Tree Algorithms
- [Kruskal's Algorithm](le1/kruskal.py)
- [Prim's Algorithm](le1/prim.py)

### Shortest Path Algorithms
- [Floyd-Warshall Algorithm](le1/floyd_warshall.py)
- [Dijkstra's Algorithm](le1/dijkstra.py)
- [Bellman-Ford Algorithm](le1/bellman_ford.py)

## LE 2

### Maximum Matching Algorithms
- [Kuhn's Algorithm](le2/kuhn.py)

## LE 3

## LE 4

## Utils
Some of the above implementations use already known data structures, so they are also in this repository.
Here is a list of these data structures:
- [Union Find / Disjoint Set Union](utils/union_find.py)

## Notes
- The code in this repository uses verbose variable names and long comments to help you better understand a data structure or algorithm. However, you may want to use shorter variable names (`node_count` instead of `n`) and use types with less overhead (e.g. `list` instead of `dict` for adjacency lists) when you implement these data structures and algorithms yourself to save time and reduce code file sizes.