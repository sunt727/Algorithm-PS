class BST:
    def __init__(self, key = None, parent = None):
        '''Initialize a BST node'''
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    def minimum(self):
        '''Return a node with minimum key of self's sub-tree, else None'''
        if self.key is not None:
            if self.left:
                return self.left.minimum()
            return self
        return None

    def find(self, key): 
        '''Return a highest node having key in self's sub-tree, else None'''
        if self.key is not None:
            if key == self.key:
                return self
            if key < self.key and self.left:
                return self.left.find(key)
            if key > self.key and self.right:
                return self.right.find(key)
        return None

    def successor(self):
        '''Return a node in tree with next larger key, else None'''
        if self.key is not None:
            if self.right:
                return self.right.minimum()
            node = self                         # (might be None)
            while (node.parent and 
                   node.parent.right is node):
                node = node.parent
            return node.parent
        return None

    def insert(self, key):
        '''Insert key into self's sub-tree'''
        if self.key is None:
            self.key = key
            self.maintain()
        elif key < self.key:
            if self.left is None:
                self.left = self.__class__(None, self)
            self.left.insert(key)
        else:
            if self.right is None:
                self.right = self.__class__(None, self)
            self.right.insert(key)

    def replace(self, node):
        '''Replace self's attributes with node's attributes'''
        self.key = node.key
        self.left = node.left
        self.right = node.right
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self
        
    def delete(self):
        '''Remove self's key from sub-tree'''
        if self.left and self.right:
            node = self.right.minimum()
            self.key = node.key
            node.delete()
            return
        if self.right:
            self.replace(self.right)
        elif self.left:
            self.replace(self.left)
        else:
            if self.parent is None:
                self.key = None
            elif self.parent.right is self:
                self.parent.right = None
            elif self.parent.left is self:
                self.parent.left = None
        self.maintain()

    def maintain(self):
        '''
        Perform maintenance after a dynamic operation
        Called by lowest node with sub-tree modified by insert or delete
        '''
        pass

    def iterative_traversal(self):
        A = []
        node = self.minimum()
        while node:
            A.append(node.key)
            node = node.successor()
        return A

    def recursive_traversal(self, A = None):
        if A is None: 
            A = []
        if self.left:
            self.left.recursive_traversal(A)
        A.append(self.key)
        if self.right:
            self.right.recursive_traversal(A)
        return A

    def __str__(self):
        '''Return ASCII drawing of the tree'''
        s = str(self.key)
        if self.left is None and self.right is None:
            return s
        sl, sr = [''], ['']
        if self.left:
            s = '_' + s
            sl = str(self.left).split('\n')
        if self.right:
            s = s + '_'
            sr = str(self.right).split('\n')
        wl, cl = len(sl[0]), len(sl[0].lstrip(' _'))
        wr, cr = len(sr[0]), len(sr[0].rstrip(' _'))
        a = [(' ' * (wl - cl)) + ('_' * cl) + s +
             ('_' * cr) + (' ' * (wr - cr))]
        for i in range(max(len(sl), len(sr))):
            ls = sl[i] if i < len(sl) else ' ' * wl
            rs = sr[i] if i < len(sr) else ' ' * wr
            a.append(ls + ' ' * len(s) + rs) 
        return '\n'.join(a)

class AVL(BST):
    def __init__(self, key = None, parent = None):
        '''Augment BST with height and skew'''
        super().__init__(key, parent)
        self.height = 0
        self.skew = 0

    def update(self):
        '''Update height and skew'''
        left_height  = self.left.height  if self.left  else -1
        right_height = self.right.height if self.right else -1
        self.height = max(left_height, right_height) + 1
        self.skew = right_height - left_height

    def right_rotate(self):
        '''
        Rotate left to right, assuming left is not None
         __s__      __n__
        _n_  c  =>  a  _s_
        a b            b c
        '''
        node, c = self.left, self.right
        a, b = self.left.left, self.left.right 
        self.key, node.key = node.key, self.key
        if a:
            a.parent = self
        if c:
            c.parent = node
        self.left, self.right = a, node
        node.left, node.right = b, c
        node.update()
        self.update()

    def left_rotate(self):
        '''
        Rotate right to left, assuming right is not None
        __s__        __n__
        a  _n_  =>  _s_  c
           b c      a b   
        '''
        node, a = self.right, self.left 
        b, c = self.right.left, self.right.right
        self.key, node.key = node.key, self.key
        if a:
            a.parent = node
        if c:
            c.parent = self
        self.left, self.right = node, c
        node.left, node.right = a, b
        node.update()
        self.update()

    def maintain(self):
        '''Update height and skew and rebalance up the tree'''
        self.update()
        if self.skew == 2:      # must have right child
            if self.right.skew == -1:
                self.right.right_rotate() 
            self.left_rotate()
        elif self.skew == -2:   # must have left child
            if self.left.skew == 1:
                self.left.left_rotate() 
            self.right_rotate()
        if self.parent:
            self.parent.maintain()

    def __str__(self):
        '''Return ASCII drawing of the tree (visualize skew)'''
        key = self.key
        self.key = str(key) + (
            '=' if self.skew == 0 else
            '>' if self.skew < 0 else 
            '<')
        s = super().__str__()
        self.key = key
        return s

##################
# Test your code #
##################
def test_random(tree, population, num_insert, num_delete):
    from random import sample, choice
    a = []
    a.append('Building new tree on %s random keys' % num_insert)
    keys = sample(population, num_insert)
    a.append('Keys: %s' % keys)
    for key in keys:
        a.append('Inserting %s...' % key)
        tree.insert(key)
        a.append(str(tree)) 
    a.append('Now deleting %s random keys' % num_delete)
    a.append('Keys: %s' % keys)
    for i in range(num_delete):
        key = choice(population)
        a.append('Attemping to remove %s...*' % key)
        node = tree.find(key)
        if node is None:
            a.append('%s not found... :(' % key)
        else:
            node.delete()
            a.append('%s removed!' % key)
            a.append(str(tree))
    a.append('Iterative in-order traversal:')
    a.append('%s' % tree.iterative_traversal())
    a.append('Recursive in-order traversal:')
    a.append('%s' % tree.recursive_traversal())
    return '\n'.join(a)

def test_BST(max_key, num_inserts, num_deletes):
    a = []
    a.append('*' * 11)
    a.append('Testing BST')
    a.append('*' * 11)
    tree = BST()
    a.append(test_random(tree, range(max_key), num_inserts, num_deletes))
    a.append('Test worst case: inserting 10 keys in order')
    tree = BST()
    for i in range(max_key):
        tree.insert(i)
    a.append(str(tree))
    return '\n'.join(a)

def test_AVL(max_key, num_inserts, num_deletes):
    a = []
    a.append('*' * 11)
    a.append('Testing AVL')
    a.append('*' * 11)
    tree = AVL()
    a.append(test_random(tree, range(max_key), num_inserts, num_deletes))
    return '\n'.join(a)

if __name__ == '__main__':
    print(test_BST(20, 20, 5))
    print(test_AVL(20, 20, 5))
