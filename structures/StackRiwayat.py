class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        if isinstance(item, dict) and "id" in item:
            if any(entry.get("id") == item["id"] for entry in self.stack):
                return False
        self.stack.append(item)
        return True

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("Stack is empty")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("Stack is empty")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def find_by_id(self, idTicket):
        for entry in self.stack:
            if isinstance(entry, dict) and entry.get("id") == idTicket:
                return entry
        return None

    def contains_id(self, idTicket):
        return self.find_by_id(idTicket) is not None
