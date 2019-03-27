
def delta(p,q):
    if p == q:
        return 0
    return 1


 def initialize_D(m,n):
    D = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(m+1):
        D[i][0] = i
    for j in range(n+1):
        D[0][j] = j
    return D

def LD(s,t):
    """
    Copmute the Levenshtein distance between two strings
    Arguemnts:
    s -- string 1
    t -- string 2
    Returns:
    Levenshtein distance between s and t
    """
    # m -- number of rows
    # n -- number of cols
    m, n = len(s), len(t)
    if not (m and n):
        return max(m,n)
    D = initialize_D(m,n)
    for i in range(1,m + 1):
        for j in range(1,n + 1):
            cost = delta(s[i-1], t[j-1])
            D[i][j] = min( 
                D[i-1][j] + 1,
                D[i][j-1] + 1,
                D[i-1][j-1] + cost
            )
    return D[m][n]
    
class BKNode:
    """
    Class representing a node on a BK tree.
    BK trees are n-ary for an arbitrary n.
    """
    def __init__(self, word):
        self.word = word
        self.children = {}

        
    def insert(self, word, metric):
        """
        Insert a new word into the BK Node
        """
        d =  metric(self.word, word)
        if d == 0:
            # The word is already in the tree!
            return
        if d not in self.children:
            self.children[d] = BKNode(word)
        else:
            self.children[d].insert(word, metric)
    
    def __repr__(self):
        """
        Convert the tree to a string (dictionary)
        """
        return "{}:{}".format(self.word, self.children)
    
    def query(self, word, n, metric):
        """
        Find all words 
        """
        self.ret = {}
        # pass the root  node into the function
        self._query(word, n, metric, root=self)
        return self.ret
        
    def _query(self, word, n, metric, root):
        d = metric(word, self.word)
        #print(word, self.word, d)
        if d <= n:
            #print("***ADDED***")
            root.ret[self.word] = d
        for i in range( max(0, d-n), n+d+1):
            if i in self.children:
                self.children[i]._query(word, n, metric, root)
    
    def find(self, word):
        return self._find(word, path = [])
        
    def _find(self, word, path):
        if self.word == word:
            #print("{}={}, {}".format(self.word, word, self.word == word))
            print(path)
            return path 
        for i in self.children:
            self.children[i]._find(word, path + [i])
            
    

class BKTree:
    def __init__(self, word, metric):
        self.root = BKNode(word)
        self.metric  = metric
    
    def __repr__(self):
        return str(self.root)
    
    def insert(self, word):
        self.root.insert(word, self.metric)
    
    def query(self, word, n):
        self.root.query(word, n, self.metric)
        return self.root.ret

    def find(self, word):
        return self.root.find(word)
        
        
    