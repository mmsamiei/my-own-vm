class Memory:
    def __init__(self, size=256):
        self.size = size
        self.memory = [0] * size
        # Add a stack for function calls
        self.stack = []
        
    def read(self, address):
        """Read a value from memory at the given address."""
        if not 0 <= address < self.size:
            raise IndexError(f"Memory address {address} out of bounds (0-{self.size-1})")
        return self.memory[address]
        
    def write(self, address, value):
        """Write a value to memory at the given address."""
        if not 0 <= address < self.size:
            raise IndexError(f"Memory address {address} out of bounds (0-{self.size-1})")
        self.memory[address] = value
        
    def push(self, value):
        """Push a value onto the stack."""
        self.stack.append(value)
        
    def pop(self):
        """Pop a value from the stack."""
        if not self.stack:
            raise IndexError("Stack underflow")
        return self.stack.pop()
        
    def peek(self):
        """Peek at the top value on the stack without removing it."""
        if not self.stack:
            raise IndexError("Empty stack")
        return self.stack[-1]
        
    def stack_size(self):
        """Return the current size of the stack."""
        return len(self.stack)