#include "avl.h"
#include <stdlib.h>


// Prototypes
AVL *rebalance(AVL *avl);
AVL *rotate_left(AVL *avl);
AVL *rotate_right(AVL *avl);

int max(int a, int b);
int height(AVL *avl);
void update_height(AVL *avl);
// ===========


struct AVL {
    /**
     * An AVL tree is a binary search tree implementation that "rotates"
     * itself if its two subtrees are unbalanced after any operation to
     * ensure that it remains balanced.
     * 
     * Given an AVL with n nodes, these are its operations and their time complexities:
     *     avl_search: O(log n)
     *     avl_insert: O(log n)
     *     avl_delete: O(log n)
     */
    int64_t value;
    int height;
    struct AVL *left;
    struct AVL *right;
};


AVL *avl_init(int64_t value) {
    /**
     * Initializes an AVL node with the given value, initially with a
     * height of 0 and no left or right child.
     * 
     * Args:
     *     value (int64_t): The value the node will have.
     * 
     * Returns:
     *     AVL*: The initialized AVL node.
     */
    AVL *avl = (AVL*)malloc(sizeof(AVL));
    avl->value = value;
    avl->height = 0;
    avl->left = NULL;
    avl->right = NULL;
    return avl;
}


AVL *avl_search(AVL *avl, int64_t value) {
    /**
     * Searches for the node containing the given value in the AVL
     * tree and returns it if it exists. If it doesn't NULL is returned.
     * 
     * Args:
     *     avl (AVL*): The AVL tree where the value is searched in.
     *     value (int64_t): The value to search for.
     * 
     * Returns:
     *     AVL*: The node containing the given value.
     */
    if (avl == NULL) {
        return NULL;
    } else if (value < avl->value) {
        return avl_search(avl->left, value);
    } else if (value > avl->value) {
        return avl_search(avl->right, value);
    } else {
        return avl;
    }
}


AVL *avl_insert(AVL *avl, int64_t value) {
    /**
     * Inserts the given value into the AVL tree, then rebalances it to
     * maintain the AVL property.
     * =
     * Args:
     *     avl (AVL*): The AVL tree where the value is inserted in.
     *     value (int64_t): The value to insert.
     * 
     * Returns:
     *     AVL*: The new AVL tree post-insertion.
     */
    if (avl == NULL) {
        return avl_init(value);
    } else if (value < avl->value) {
        avl->left = avl_insert(avl->left, value);
    } else if (value > avl->value) {
        avl->right = avl_insert(avl->right, value);
    } else {
        // Do nothing
    }

    update_height(avl);
    return rebalance(avl);
}


AVL *avl_delete(AVL *avl, int64_t value) {
    /**
     * Deletes the given value from the AVL tree, then rebalances it to
     * maintain the AVL property.
     * =
     * Args:
     *     avl (AVL*): The AVL tree where the value is deleted from.
     *     value (int64_t): The value to delete.
     * 
     * Returns:
     *     AVL*: The new AVL tree post-deletion.
     */
    if (avl == NULL) {
        return NULL;
    } else if (value < avl->value) {
        avl->left = avl_delete(avl->left, value);
    } else if (value > avl->value) {
        avl->right = avl_delete(avl->right, value);
    } else {
        // Search for new root
        if (avl->left == NULL) {
            // No left subtree: Use right subtree as new root
            AVL *right = avl->right;
            free(avl);
            return right;
        } else if (avl->right == NULL) {
            // No right subtree: Use left subtree as new root
            AVL *left = avl->left;
            free(avl);
            return left;
        } else {
            // Both subtrees exist: Get leftmost node of right subtree
            AVL *new_root = avl->right;
            while (new_root->left != NULL) {
                new_root = new_root->left;
            }
            avl->value = new_root->value;
            avl->right = avl_delete(avl->right, new_root->value);
        }
    }

    update_height(avl);
    return rebalance(avl);
}


void avl_free(AVL *avl) {
    /**
     * Frees the memory of the given AVL tree recursively.
     * 
     * Args:
     *     avl (AVL*): The AVL tree to free.
     */
    if (avl == NULL) {
        return;
    }
    avl_free(avl->left);
    avl_free(avl->right);
    free(avl);
}


AVL *rebalance(AVL *avl) {
    /**
     * Checks if the AVL tree is balanced, that is, the height difference of
     * its subtrees is at most 1. If the tree is not balanced, it is rotated
     * accordingly. Does nothing if NULL is given.
     * 
     * Args:
     *     avl (AVL*): The AVL tree to rebalance.
     * 
     * Returns:
     *     AVL*: The rebalaned AVL tree.
     * 
     */
    if (avl != NULL) {
        update_height(avl); // Just to be safe
        if (height(avl->left) - height(avl->right) >= 2) {
            // Left subtree too tall: Rotate right
            if (height(avl->left->left) < height(avl->left->right)) {
                // avl->left->left shouldn't be shorter than avl->left->right before the rotation
                avl->left = rotate_left(avl->left);
            }
            avl = rotate_right(avl);
        } else if (height(avl->right) - height(avl->left) >= 2) {
            // Right subtree too tall: Rotate left
            if (height(avl->right->right) < height(avl->right->left)) {
                // avl->right->right shouldn't be shorter than avl->right->left before the rotation
                avl->right = rotate_right(avl->right);
            }
            avl = rotate_left(avl);
        }
    }

    return avl;
}


AVL *rotate_left(AVL *avl) {
    /**
     * Rotates the AVL tree left (counter-clockwise).
     * 
     * Args:
     *     avl (AVL*): The AVL tree to rotate.
     * 
     * Returns:
     *     AVL*: The rotated AVL tree.
     */
    AVL *right = avl->right;
    AVL *right_left = avl->right->left;

    right->left = avl;
    avl->right = right_left;

    update_height(avl);
    update_height(right);

    return right;
}


AVL *rotate_right(AVL *avl) {
    /**
     * Rotates the AVL tree right (clockwise).
     * 
     * Args:
     *     avl (AVL*): The AVL tree to rotate.
     * 
     * Returns:
     *     AVL*: The rotated AVL tree.
     */
    AVL *left = avl->left;
    AVL *left_right = avl->left->right;

    left->right = avl;
    avl->left = left_right;

    update_height(avl);
    update_height(left);

    return left;
}


int max(int a, int b) {
    /**
     * Helper C function for returning the greater number between two numbers.
     * 
     * Args:
     *     a (int): First number.
     *     b (int): Second number.
     * 
     * Returns:
     *     int: The greater of a and b.
     */
    return a > b ? a : b;
}


int height(AVL *avl) {
    /**
     * Helper function for returning the height of an AVL tree, allowing for
     * NULL to be evaluated to -1 instead of having to check for NULL before
     * using avl->height.
     * 
     * Args:
     *     avl (AVL*): The AVL tree whose height to check.
     * 
     * Returns:
     *     int: The height of the given AVL tree, or -1 if NULL was given.
     */
    return avl == NULL ? -1 : avl->height;
}


void update_height(AVL *avl) {
    /**
     * Updates the height property of the given AVL node. Note that it does not
     * recursivley update its children's heights.
     * 
     * Args:
     *     avl (AVL*): The node whose height is to be updated.
     */
    avl->height = max(height(avl->left), height(avl->right)) + 1;
}