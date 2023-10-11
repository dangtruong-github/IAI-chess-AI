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
        return self.table.get(key) 
    
    def store(self, entry):
        self.table[entry.key] = entry
