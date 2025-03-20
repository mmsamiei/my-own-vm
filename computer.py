from memory import Memory
from cpu import CPU

class Computer:
    def __init__(self, memory_size=256):
        self.memory = Memory(memory_size)
        self.cpu = CPU(self.memory)
    
    def load_program(self, program, start_address=0):
        for i, value in enumerate(program):
            self.memory.write(start_address + i, value)
    
    def run(self):
        self.cpu.pc = 0  # Reset program counter
        self.cpu.run()
        
if __name__ == "__main__":
    program = [
        0x01, 0x05,  # LDA 5 (Load 5 into register A)
        0x02, 0x0A,  # LDB 10 (Load 10 into register B)
        0x03,        # ADD (Add B to A)
        0x05, 0x0F,  # STA 15 (Store result at address 15)
        0xFF         # HALT
    ]

    # Create and run the computer
    computer = Computer()
    computer.load_program(program)
    computer.run()

    # Check the result
    print(f"Result at memory address 15: {computer.memory.read(15)}")  # Should be 15
