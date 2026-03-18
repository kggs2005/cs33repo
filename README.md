# CS 33 Implementation Repository

This repository contains implementations of data structures and algorithms in CS 33 so far. It is currently unfinished and not up-to-date with the latest CS 33 lessons. Below is a comprehensive list of the implementations currently included in this repository.

## LE 1

### Minimum Spanning Tree Algorithms
- Kruskal's Algorithm ([Python](le1/kruskal.py))
- Prim's Algorithm ([Python](le1/prim.py))

### Shortest Path Algorithms
- Floyd-Warshall Algorithm ([Python](le1/floyd_warshall.py))
- Dijkstra's Algorithm ([Python](le1/dijkstra.py))
- Bellman-Ford Algorithm ([Python](le1/bellman_ford.py))

### Binary Search Tree Data Structures
- Treap ([C](le1/treap.c), [Header](le1/treap.h))
- AVL Tree ([C](le1/avl.c), [Header](le1/avl.h))

## LE 2

## LE 3

## LE 4

## Utils
Some of the above implementations use already known data structures, so they are also in this repository.
Here is a list of these data structures:
- Union Find / Disjoint Set Union ([Python](utils/union_find.py))

## Notes
- The code in this repository uses verbose variable names and long comments to help you better understand a data structure or algorithm. However, you may want to use shorter variable names (`node_count` instead of `n`) and use types with less overhead (e.g. `list` instead of `dict` for adjacency lists) when you implement these data structures and algorithms yourself to save time and reduce code file sizes.