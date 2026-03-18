#ifndef TREAP_H
#define TREAP_H

#include <stdint.h>

typedef struct Treap Treap;

Treap *treap_init(int64_t value);
Treap *treap_search(Treap *treap, int64_t value);
Treap *treap_insert(Treap *treap, int64_t value);
Treap *treap_delete(Treap *treap, int64_t value);
void treap_free(Treap *treap);

struct Treap {
    /**
     * A binary search tree (BST) implementation that uses randomization to keep
     * itself balanced. Whenever a node is initialized, it is assigned a random
     * priority. This priority will then decide which root ends up being the
     * parent when merging two treaps together.
     * 
     * Given a treap with n nodes, these are its operations and their time complexities:
     *     treap_search: O(log n)
     *     treap_insert: O(log n)
     *     treap_delete: O(log n)
     */
    int64_t value;
    int64_t priority;
    struct Treap *left;
    struct Treap *right;
};

#endif