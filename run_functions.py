#!/usr/bin/env python3
"""
SimpleScript with Functions - Demo

This script demonstrates a basic implementation of function support
for the SimpleScript language.
"""

from src.memory import Memory
from src.cpu import CPU

def main():
    # Create a simple virtual machine with function support
    memory = Memory(256)
    cpu = CPU(memory)
    
    # Initialize memory-mapped I/O
    IO_OUTPUT_BUFFER = 0xF1  # Address 241 for output
    IO_OUTPUT_COUNT = 0xF2   # Address 242 for output counter
    memory.write(IO_OUTPUT_COUNT, 0)  # Initialize output counter
    
    # Sample program with function definitions and calls
    program = [
        # Start with jump to main
        ("JMP", 20),  # Jump to main (adjust as needed)
        
        # Function: add(a, b) - returns a + b
        # Function starts at address 1
        # Parameters are passed on stack, result returned in register A
        ("POP", None),      # Pop first parameter (b) into A
        ("STA", 16),        # Store A to temporary variable (address 16)
        ("POP", None),      # Pop second parameter (a) into A
        ("LDB_MEM", 16),    # Load B with first parameter
        ("ADD", None),      # Add A + B, result in A
        ("RET", None),      # Return (with result in A)
        
        # Function: square(n) - returns n * n
        # Function starts at address 7
        ("POP", None),      # Pop parameter (n) into A
        ("STA", 17),        # Store to temp variable
        ("LDB_MEM", 17),    # Load same value into B
        ("MUL", None),      # Multiply A * B
        ("RET", None),      # Return with result in A
        
        # Function: double(n) - returns n + n (using add function)
        # Function starts at address 12
        ("POP", None),      # Pop parameter into A
        ("STA", 18),        # Store to temp variable
        ("LDA_MEM", 18),    # Load the value into A
        ("PUSH", None),     # Push first parameter (same value)
        ("LDA_MEM", 18),    # Load the value again
        ("PUSH", None),     # Push second parameter (same value)
        ("CALL", 1),        # Call add function (at address 1)
        ("RET", None),      # Return with result in A
        
        # Main program - starts at address 20
        # First push a return address for the main program (to prevent stack underflow)
        ("LDA", 0),         # Load a dummy return address
        ("PUSH", None),     # Push it on the stack
        
        # Main program continues
        ("LDA", 5),         # Load A with 5
        ("STA", 30),        # Store 5 at variable 'x' (address 30)
        
        # Call square(5)
        ("LDA_MEM", 30),    # Load A with value of x
        ("PUSH", None),     # Push parameter for square
        ("CALL", 7),        # Call square function
        ("STA", 31),        # Store result at variable 'result1' (address 31)
        ("STA", 0xF1),      # Print result (should be 25)
        
        # Increment output counter
        ("LDA_MEM", 0xF2),  # Load current output count
        ("LDB", 1),         # Load B with 1
        ("ADD", None),      # Add 1 to output count
        ("STA", 0xF2),      # Store updated output count
        
        # Call add(5, 10)
        ("LDA", 5),         # Load A with 5
        ("PUSH", None),     # Push first parameter
        ("LDA", 10),        # Load A with 10
        ("PUSH", None),     # Push second parameter
        ("CALL", 1),        # Call add function
        ("STA", 32),        # Store result at variable 'result2' (address 32)
        ("STA", 0xF1),      # Print result (should be 15)
        
        # Increment output counter
        ("LDA_MEM", 0xF2),  # Load current output count
        ("LDB", 1),         # Load B with 1
        ("ADD", None),      # Add 1 to output count
        ("STA", 0xF2),      # Store updated output count
        
        # Call double(7)
        ("LDA", 7),         # Load A with 7
        ("PUSH", None),     # Push parameter
        ("CALL", 12),       # Call double function
        ("STA", 33),        # Store result at variable 'result3' (address 33)
        ("STA", 0xF1),      # Print result (should be 14)
        
        # Increment output counter
        ("LDA_MEM", 0xF2),  # Load current output count
        ("LDB", 1),         # Load B with 1
        ("ADD", None),      # Add 1 to output count
        ("STA", 0xF2),      # Store updated output count
        
        # End program
        ("HALT", None),     # Halt execution
    ]
    
    # Load and run the program
    print("Running SimpleScript with Functions demo...")
    print("===========================================")
    
    # Load program
    cpu.running = True
    
    # Execute each instruction
    pc = 0
    outputs = []
    while cpu.running and pc < len(program):
        instruction, operand = program[pc]
        cpu.pc = pc
        cpu.execute(instruction, operand)
        pc = cpu.pc
        
        # Check for new output
        output_count = memory.read(IO_OUTPUT_COUNT)
        if output_count > len(outputs):
            output = memory.read(IO_OUTPUT_BUFFER)
            outputs.append(output)
            print(f"Output: {output}")
    
    print("===========================================")
    print("Program execution completed.")
    
if __name__ == "__main__":
    main() 