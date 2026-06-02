import json
import os

class Stack:
    def __init__(self):
        self.stack = []

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.stack, f)

    def load_from_json(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.stack = json.load(f)

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
        
    def checkout_pendaki(self, idTicket):
        for i in range(len(self.stack)-1, -1, -1):
            if isinstance(self.stack[i], dict) and self.stack[i].get("id") == idTicket:
                return self.stack.pop(i)
        return None

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
