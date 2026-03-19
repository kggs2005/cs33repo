#include "treap.h"
#include <stdlib.h>


// Prototypes
typedef struct SplitResult SplitResult;

SplitResult *split(Treap *treap, int64_t middle_value);
Treap *merge(Treap *left, Treap *right);

SplitResult *split_result_init(Treap *left, Treap *middle, Treap *right);
int64_t randint64();
// ===========


struct SplitResult {
    /**
     * Since C functions cannot return tuples, we instead create a struct
     * containing the results of the treap's split function.
     */
    Treap *left;
    Treap *middle;
    Treap *right;
};


Treap *treap_init(int64_t value) {
    /**
     * Initializes a treap node with the given value and a random priority,
     * initially with no left or right child.
     * 
     * Args:
     *     value (int64_t): The value the node will have.
     * 
     * Returns:
     *     Treap*: The initialized treap.
     */
    Treap *treap = (Treap*)malloc(sizeof(Treap));
    treap->value = value;
    treap->priority = randint64();
    treap->left = NULL;
    treap->right = NULL;
    return treap;
}


Treap *treap_search(Treap *treap, int64_t value) {
    /**
     * Performs binary search on the treap and returns the node in the treap
     * with the given value if it exists, or NULL if it doesn't exist.
     * 
     * Args:
     *     treap (Treap*): The given treap.
     *     value (int64_t): The value to search for.
     * 
     * Returns:
     *     Treap*: The node containing the given value if it exists, or NULL
     *         if it doesn't exist.
     */
    if (treap == NULL) {
        return NULL;
    } else if (value < treap->value) {
        return treap_search(treap->left, value);
    } else if (value > treap->value) {
        return treap_search(treap->right, value);
    } else {
        return treap;
    }
}


Treap *treap_insert(Treap *treap, int64_t value) {
    /**
     * Inserts a node with the given value into the treap and returns the
     * new treap. Does nothing if the value is already in the treap and just
     * returns the given treap.
     * 
     * Args:
     *     treap (Treap*): The given treap.
     *     value (int64_t): The value to add to the treap.
     * 
     * Returns:
     *     Treap*: The new treap.
     */
    if (treap_search(treap, value) != NULL) {
        return treap;
    }

    SplitResult *split_result = split(treap, value);
    Treap *left = split_result->left;
    Treap *middle = treap_init(value); // split_result->middle should be NULL
    Treap *right = split_result->right;
    free(split_result);
    return merge(merge(left, middle), right);
}


Treap *treap_delete(Treap *treap, int64_t value) {
    /**
     * Deletes the node with the given value in the treap and returns the
     * new treap. Does nothing if there is no node with the given value in
     * the treap and just returns the given treap.
     * 
     * Args:
     *     treap (Treap*): The given treap.
     *     value (int64_t): The value to remove from the treap.
     * 
     * Returns:
     *     Treap*: The new treap.
     */
    if (treap_search(treap, value) == NULL) {
        return treap;
    }

    SplitResult *split_result = split(treap, value);
    Treap *left = split_result->left;
    free(split_result->middle); // split_result->middle should not be NULL
    Treap *right = split_result->right;
    free(split_result);
    return merge(left, right);
}


void treap_free(Treap *treap) {
    /**
     * Frees the memory of the treap.
     * 
     * Args:
     *     treap (Treap*): The treap to free.
     */
    if (treap == NULL) {
        return;
    }
    treap_free(treap->left);
    treap_free(treap->right);
    free(treap);
}


SplitResult *split(Treap *treap, int64_t middle_value) {
    /**
     * Given a treap and an int64_t v, splits the treaps into 3 partitions: a treap
     * containing all nodes with values less than v, a treap containing the node
     * with value v (or NULL if v is not in the treap), and a treap containing all
     * nodes with values greater than v, then returns the 3 resulting treaps.
     * 
     * Note that this operation mutates the given treap.
     * 
     * Args:
     *     treap (Treap*): The treap to be split.
     *     middle_value (int64_t): The integer v.
     * 
     * Returns:
     *     SplitResult*: The result of the split.
     */
    if (treap == NULL) {
        // Treap is empty: Return (NULL, NULL, NULL).
        return split_result_init(NULL, NULL, NULL);
    } else if (middle_value < treap->value) {
        // Middle node is in left subtree: Split left subtree recursively and
        // set the result's right subtree to be this node's left child, then
        // return (result.left, result.middle, self).
        SplitResult *split_result = split(treap->left, middle_value);
        treap->left = split_result->right;
        Treap *result_left = split_result->left;
        Treap *result_middle = split_result->middle;
        Treap *result_right = treap;
        free(split_result);
        return split_result_init(result_left, result_middle, result_right);
    } else if (middle_value > treap->value) {
        // Middle node is in right subtree: Split right subtree recursively and
        // set the result's left subtree to be this node's right child, then
        // return (self, result.middle, result.right).
        SplitResult *split_result = split(treap->right, middle_value);
        treap->right = split_result->left;
        Treap *result_left = treap;
        Treap *result_middle = split_result->middle;
        Treap *result_right = split_result->right;
        free(split_result);
        return split_result_init(result_left, result_middle, result_right);
    } else {
        // This node contains middle value: Simply disconnect self from children
        // then return (left, self, right).
        Treap *left = treap->left;
        Treap *right = treap->right;
        treap->left = NULL;
        treap->right = NULL;
        return split_result_init(left, treap, right);
    }
}


Treap *merge(Treap *left, Treap *right) {
    /**
     * Given two treaps, merge them. Their roots' priority dictates
     * which of the two roots is the resulting merged treap's root,
     * which is the root with the higher priority. For this operation
     * to work, all values of the first treap must all be less than any
     * value in the second treap.
     * 
     * Note that this operation mutates the given treaps.
     * 
     * Args:
     *     left (Treap*): The treap with the lesser node values.
     *     right (Treap*): The treap with the greater node values.
     * 
     * Returns:
     *     Treap*: The merged treap.
     */

    if (left == NULL || right == NULL) {
        return left == NULL ? right : left;
    }

    if (left->priority < right->priority) {
        // Right's priority is higher:
        // Recursively merge left with right's left child.
        right->left = merge(left, right->left);
        return right;
    } else {
        // Left's priority is higher:
        // Recursively merge right with left's right child.
        left->right = merge(left->right, right);
        return left;
    }
}


SplitResult *split_result_init(Treap *left, Treap *middle, Treap *right) {
    /**
     * Initializes a SplitResult given the left, middle, and right treaps.
     * 
     * Args:
     *     left (Treap*): The resulting left treap of the split operation.
     *     middle (Treap*): The resulting middle treap of the split operation.
     *     right (Treap*): The resulting right treap of the split operation.
     * 
     * Returns:
     *     SplitResult*: The initialized SplitResult.
     */
    SplitResult *split_result = (SplitResult*)malloc(sizeof(SplitResult));
    split_result->left = left;
    split_result->middle = middle;
    split_result->right = right;
    return split_result;
}


int64_t randint64() {
    /**
     * Generates a random 64-bit integer by generating 8 8-bit numbers and
     * concatenating their bits. Admittedly not the strongest or most efficient
     * method.
     * 
     * Returns:
     *     int64_t: The resulting random number.
     */
    int64_t result = 0;
    for (int i = 0; i < 8; i++) {
        result = (result << 8) | (rand() & 0xFF);
    }
    return result;
}
