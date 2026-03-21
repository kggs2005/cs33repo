# CS 33 Data Structures and Algorithms Repository

## This repository is a work in progress.

- This repository contains Python implementations of algorithms in CS 33 so far.

## Table of Contents

## LE 1

### Minimum Spanning Tree Algorithms
- [Kruskal's Algorithm](le1/kruskal.py)
- [Prim's Algorithm](le1/prim.py)

### Shortest Path Algorithms
- [Floyd-Warshall Algorithm](le1/floyd_warshall.py)
- [Dijkstra's Algorithm](le1/dijkstra.py)
- [Bellman-Ford Algorithm](le1/bellman_ford.py)

### Self-Balancing Binary Search Trees
- [Treap](le1/treap.py)
- [AVL Tree](le1/avl.py)

### Algorithms for Obtaining Strongly Connected Components
- [Kosaraju's Algorithm](le1/kosaraju.py)
- [Tarjan's SCC Algorithm](le1/tarjan_scc.py)

### Lowest Common Ancestor and Range Queries
- [Lowest Common Ancestor](le1/lca.py)
- [Heavy Light Decomposition](le1/hld.py)
- [Centroid Decomposition](le1/centroid.py)

## LE 2

### Persistent Data Structures
- [Persistent Stack](le2/persistent_stack.py)

### Max Flow Min Cut Algorithms
- [Edmonds-Karp Algorithm](le2/edmonds_karp.py)

### Maximum Matching Algorithms
- [Kuhn's Algorithm](le2/kuhn.py)

## LE 3

## LE 4

## Utils
Some of the above implementations use already known data structures.
- [Union Find](utils/union_find.py)
- [Segment Tree](utils/segment_tree.py)

## Notes
- The code in this repository uses verbose variable names and long comments to help you better understand a data structure or algorithm. However, you may want to use shorter variable names (`n` instead of `node_count`) and use types with less overhead (e.g. `list` instead of `dict` for adjacency lists) when you implement these data structures and algorithms yourself to save time and reduce code file sizes.