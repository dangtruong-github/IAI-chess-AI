HASH_SIZE = 4294967569

class Entry:
    def __init__(self, key, depth, score, flag, best_move):
        self.key = key
        self.depth = depth
        self.score = score
        self.flag = flag
        self.best_move = best_move

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, key):
        index = key % HASH_SIZE
        return self.table.get(index) 
    
    def store(self, entry):
        index = entry.key % HASH_SIZE
        self.table[index] = entry
