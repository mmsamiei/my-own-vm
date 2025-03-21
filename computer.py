from memory import Memory
from cpu import CPU

class Computer:
    def __init__(self, memory_size=256):
        self.memory = Memory(memory_size)
        self.cpu = CPU(self.memory)
        
        # Define memory-mapped I/O addresses
        self.IO_INPUT_BUFFER = 0xF0  # Address 240 for input
        self.IO_OUTPUT_BUFFER = 0xF1  # Address 241 for output
        
    def load_program(self, program):
        """
        Loads a program into memory.
        
        Program is a list of tuples (instruction, operand).
        Operand can be None for instructions that don't need one.
        """
        self.program = program
    
    def run(self):
        self.cpu.pc = 0  # Reset program counter
        self.cpu.running = True
        
        while self.cpu.running and self.cpu.pc < len(self.program):
            instruction, operand = self.program[self.cpu.pc]
            self.cpu.execute(instruction, operand)
    
    def set_input(self, value):
        self.memory.write(self.IO_INPUT_BUFFER, value)
        
    def get_output(self):
        return self.memory.read(self.IO_OUTPUT_BUFFER)
    
    def debug_mode(self):
        self.cpu.pc = 0  # Reset program counter
        self.cpu.running = True
        
        while self.cpu.running and self.cpu.pc < len(self.program):
            instruction, operand = self.program[self.cpu.pc]
            print(f"PC: {self.cpu.pc}, Executing: {instruction} {operand if operand is not None else ''}")
            print(f"Registers - A: {self.cpu.register_a}, B: {self.cpu.register_b}")
            print(f"Flags - Zero: {self.cpu.zero_flag}, Carry: {self.cpu.carry_flag}")
            print(f"-"*10)
            
            self.cpu.execute(instruction, operand)
            input("Press Enter to continue...")