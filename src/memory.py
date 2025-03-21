class Memory:
    def __init__(self, size=256):
        self.size = size
        self.memory = [0] * size
        
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