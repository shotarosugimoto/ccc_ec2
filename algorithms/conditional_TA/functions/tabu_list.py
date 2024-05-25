class TabuList:
    def __init__(self, max_length):
        self.max_length = max_length
        self.list = []

    def add(self, item):
        if item in self.list:
            self.list.remove(item)
        self.list.append(item)
        if len(self.list) > self.max_length:
            self.list.pop(0)

    def contains(self, item):
        return item in self.list
