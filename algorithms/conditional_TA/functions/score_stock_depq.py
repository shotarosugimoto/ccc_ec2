from depq import DEPQ


class ScoreStockDepq:
    def __init__(self, max_size=5000):
        self.max_size = max_size
        self.min_penalty = float('inf')
        self.depq = DEPQ()
        self.now_size = 0

    def push(self, item, penalty):
        if self.depq.size() < self.max_size:
            self.depq.insert(item, penalty)
            self.min_penalty = self.min_penalty if self.min_penalty < penalty else penalty
            self.now_size += 1
        else:
            if penalty < self.min_penalty:
                self.depq.poplast()
                self.depq.insert(item, penalty)
                self.min_penalty = self.depq.low()

    def pop(self):
        return self.depq.poplast() if self.depq else None

    def __len__(self):
        return self.depq.size()
