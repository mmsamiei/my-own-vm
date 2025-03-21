#!/usr/bin/env python3
"""
SimpleScript Functions - Final Demo

This demonstrates a complete implementation of function support
in the SimpleScript virtual machine.
"""

from src.memory import Memory
from src.cpu import CPU

class FunctionDemo:
    def __init__(self):
        # Create the virtual machine components
        self.memory = Memory(256)
        self.cpu = CPU(self.memory)
        
        # Define memory-mapped I/O
        self.IO_OUTPUT = 0xF1    # Output buffer
        self.IO_STATUS = 0xF2    # Status register
        
        # Initialize output buffer
        self.memory.write(self.IO_OUTPUT, 0)
        self.memory.write(self.IO_STATUS, 0)
        
        # Create a program with function calls
        self.program = self.create_program()
        
    def create_program(self):
        """Create a program that demonstrates function calls."""
        return [
            # Jump to main program
            ("JMP", 14),         # Jump to main program
            
            # Square function: compute x*x
            # Entry: Address 1
            # Arguments: value in register A
            # Returns: value in register A
            ("STA", 100),        # Store input value at address 100
            ("LDB_MEM", 100),    # Load B with the same value
            ("MUL", None),       # A = A * B (square the value)
            ("RET", None),       # Return to caller
            
            # Double function: compute 2*x
            # Entry: Address 5
            # Arguments: value in register A
            # Returns: value in register A
            ("STA", 101),        # Store input value at address 101
            ("LDA_MEM", 101),    # Load A with the value
            ("LDB", 2),          # Load B with 2
            ("MUL", None),       # A = A * B
            ("RET", None),       # Return to caller
            
            # Add function: compute x+y
            # Entry: Address 10
            # Arguments: x in register A, y in register B
            # Returns: value in register A
            ("ADD", None),       # A = A + B
            ("RET", None),       # Return to caller
            
            # Main program begins at address 14
            # Test the square function with value 4
            ("LDA", 4),          # Load A with 4
            ("CALL", 1),         # Call square function (should return 16)
            ("STA", 0xF1),       # Output the result
            # Update output status
            ("LDA", 1),          # Load A with 1
            ("STA", 0xF2),       # Update output status
            
            # Test the double function with value 7
            ("LDA", 7),          # Load A with 7
            ("CALL", 5),         # Call double function (should return 14)
            ("STA", 0xF1),       # Output the result
            # Update output status
            ("LDA", 2),          # Load A with 2
            ("STA", 0xF2),       # Update output status
            
            # Test the add function with values 10 and 25
            ("LDA", 10),         # Load A with 10
            ("LDB", 25),         # Load B with 25
            ("CALL", 10),        # Call add function (should return 35)
            ("STA", 0xF1),       # Output the result
            # Update output status
            ("LDA", 3),          # Load A with 3
            ("STA", 0xF2),       # Update output status
            
            # Combine functions: square(double(3))
            ("LDA", 3),          # Load A with 3
            ("CALL", 5),         # Call double function (returns 6)
            ("CALL", 1),         # Call square function (returns 36)
            ("STA", 0xF1),       # Output the result
            # Update output status
            ("LDA", 4),          # Load A with 4
            ("STA", 0xF2),       # Update output status
            
            # End program
            ("HALT", None),      # Halt execution
        ]
        
    def run(self, debug=False):
        """Run the program."""
        print("Running SimpleScript Functions Demo")
        print("===================================")
        
        # Initialize the CPU and start execution
        self.cpu.running = True
        pc = 0
        outputs = []
        
        # Execute each instruction
        while self.cpu.running and pc < len(self.program):
            instruction, operand = self.program[pc]
            
            if debug:
                print(f"PC: {pc}, Executing: {instruction} {operand}")
                print(f"  Before: A={self.cpu.register_a}, B={self.cpu.register_b}, Stack={self.memory.stack}")
            
            # Set the program counter
            self.cpu.pc = pc
            
            # Execute the instruction
            self.cpu.execute(instruction, operand)
            
            # Get the next program counter
            pc = self.cpu.pc
            
            if debug:
                print(f"  After: A={self.cpu.register_a}, B={self.cpu.register_b}, Stack={self.memory.stack}")
                print(f"  Next PC: {pc}")
                print("---")
            
            # Check for new output
            status = self.memory.read(self.IO_STATUS)
            if status > len(outputs):
                output = self.memory.read(self.IO_OUTPUT)
                outputs.append(output)
                print(f"Output {status}: {output}")
        
        print("===================================")
        if not self.cpu.running:
            print("Program halted.")
        else:
            print("Program completed.")
        
        return outputs

def main():
    demo = FunctionDemo()
    demo.run(debug=True)

if __name__ == "__main__":
    main() 