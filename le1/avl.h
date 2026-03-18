#ifndef AVL_H
#define AVL_H

#include <stdint.h>

typedef struct AVL AVL;

AVL *avl_init(int64_t value);
AVL *avl_search(AVL *avl, int64_t value);
AVL *avl_insert(AVL *avl, int64_t value);
AVL *avl_delete(AVL *avl, int64_t value);
void avl_free(AVL *avl);

#endif