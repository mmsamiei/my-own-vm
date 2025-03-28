from src.memory import Memory
from src.cpu import CPU

class Computer:
    def __init__(self, memory_size=256):
        self.memory = Memory(memory_size)
        self.cpu = CPU(self.memory)
        
        # Define memory-mapped I/O addresses
        self.IO_INPUT_BUFFER = 0xF0  # Address 240 for input
        self.IO_OUTPUT_BUFFER = 0xF1  # Address 241 for output
        self.IO_OUTPUT_COUNT = 0xF2   # Address 242 for output counter
        
        # Initialize the output counter
        self.memory.write(self.IO_OUTPUT_COUNT, 0)
        
        # Store outputs for easy access
        self.outputs = []
        
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
        
        # Ensure all labels are resolved
        for i, (instruction, operand) in enumerate(self.program):
            if isinstance(operand, str):
                raise ValueError(f"Unresolved label in program: {operand} at position {i}")
        
        while self.cpu.running and self.cpu.pc < len(self.program):
            instruction, operand = self.program[self.cpu.pc]
            self.cpu.execute(instruction, operand)
            
            # Check if output was written
            if self.has_new_output():
                self.record_output()
    
    def set_input(self, value):
        self.memory.write(self.IO_INPUT_BUFFER, value)
        
    def get_output(self):
        """Get the most recent output value"""
        if self.outputs:
            return self.outputs[-1]
        return self.memory.read(self.IO_OUTPUT_BUFFER)
    
    def get_all_outputs(self):
        """Get all outputs from the program execution"""
        return self.outputs
    
    def has_new_output(self):
        """Check if there's new output written to the buffer"""
        # This simplistic approach just checks if the output buffer has a non-zero value
        return self.memory.read(self.IO_OUTPUT_BUFFER) != 0
    
    def record_output(self):
        """Record the current output value"""
        output_value = self.memory.read(self.IO_OUTPUT_BUFFER)
        self.outputs.append(output_value)
        
        # Update output counter
        count = self.memory.read(self.IO_OUTPUT_COUNT)
        self.memory.write(self.IO_OUTPUT_COUNT, count + 1)
        
        # Clear the output buffer
        self.memory.write(self.IO_OUTPUT_BUFFER, 0)
    
    def print_output(self):
        """Print all outputs generated by the program"""
        if not self.outputs:
            print("No output produced by the program")
            return
            
        print("\nProgram Output:")
        for i, value in enumerate(self.outputs):
            print(f"Output {i+1}: {value}")
    
    def debug_mode(self):
        self.cpu.pc = 0  # Reset program counter
        self.cpu.running = True
        
        # Ensure all labels are resolved
        for i, (instruction, operand) in enumerate(self.program):
            if isinstance(operand, str):
                raise ValueError(f"Unresolved label in program: {operand} at position {i}")
        
        while self.cpu.running and self.cpu.pc < len(self.program):
            instruction, operand = self.program[self.cpu.pc]
            print(f"PC: {self.cpu.pc}, Executing: {instruction} {operand if operand is not None else ''}")
            print(f"Registers - A: {self.cpu.register_a}, B: {self.cpu.register_b}")
            print(f"Flags - Zero: {self.cpu.zero_flag}, Carry: {self.cpu.carry_flag}")
            print(f"-"*10)
            
            self.cpu.execute(instruction, operand)
            
            # Check if output was written
            if self.has_new_output():
                output_value = self.memory.read(self.IO_OUTPUT_BUFFER)
                print(f"Output: {output_value}")
                self.record_output()
                
            input("Press Enter to continue...")