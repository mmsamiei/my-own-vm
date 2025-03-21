class Memory:
    def __init__(self, size=256):
        # Initialize memory with zeros
        self.data = [0] * size
        self.size = size
    
    def read(self, address):
        if 0 <= address < self.size:
            return self.data[address]
        raise Exception(f"Memory access error: {address}")
    
    def write(self, address, value):
        if 0 <= address < self.size:
            self.data[address] = value & 0xFF  # Ensure 8-bit value
        else:
            raise Exception(f"Memory write error: {address}")