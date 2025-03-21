#!/usr/bin/env python3
"""
SimpleScript Functions - Minimal Demo

This is a simplified demo of function support in the SimpleScript virtual machine.
"""

from src.memory import Memory
from src.cpu import CPU

def main():
    # Create a simple virtual machine
    memory = Memory(256)
    cpu = CPU(memory)
    
    # Very simple program with one function
    program = [
        # Jump to main
        ("JMP", 7),         # Jump to main (address 7)
        
        # Function: double(n) - returns n + n
        # Function starts at address 1
        ("STA", 16),        # Store return address
        ("POP_PARAM", None),  # Pop parameter (n) into A
        ("STA", 17),        # Store n to memory
        ("LDB_MEM", 17),    # Load B with n
        ("ADD", None),      # A = A + B (n + n)
        ("LDA_MEM", 16),    # Load return address
        ("JMP", None),      # Jump to return address
        
        # Main program - starts at address 7        
        ("LDA", 5),         # Load A with 5
        ("PUSH", None),     # Push parameter for function
        ("LDA", 0),         # Load A with the next instruction address (PC + 2)
        ("ADD", None),      # Add current PC (9) + A (0) = 9
        ("PUSH", None),     # Push return address
        ("JMP", 1),         # Jump to function
        # Return here (address 12)
        ("STA", 0xF1),      # Output result
        
        # End program
        ("HALT", None),     # Halt execution
    ]
    
    # Run the program with debug output
    print("Running simple function demo...")
    print("===============================")
    
    # Initialize CPU
    cpu.running = True
    
    # Execute with debug output
    pc = 0
    while cpu.running and pc < len(program):
        instruction, operand = program[pc]
        print(f"PC: {pc}, Executing: {instruction} {operand}")
        print(f"  Before: A={cpu.register_a}, B={cpu.register_b}, Stack={memory.stack}")
        
        # Special case for the computed jump at the end of function
        if pc == 6 and instruction == "JMP" and operand is None:
            operand = cpu.register_a
            program[pc] = (instruction, operand)
            print(f"  Modified instruction to: JMP {operand}")
        
        cpu.pc = pc
        cpu.execute(instruction, operand)
        pc = cpu.pc
        
        print(f"  After:  A={cpu.register_a}, B={cpu.register_b}, Stack={memory.stack}")
        print(f"  Next PC: {pc}")
        print("---")
        
        # Prevent infinite loops
        if pc >= len(program):
            print("PC out of bounds! Halting.")
            break
    
    print("===============================")
    if not cpu.running:
        print("CPU halted.")
    else:
        print("Program completed.")
    
    if memory.read(0xF1) != 0:
        print(f"Output: {memory.read(0xF1)}")
    
if __name__ == "__main__":
    main() 