#!/usr/bin/env python3
"""
Sanity check script for SimpleScript.

This script provides a basic test to ensure that the compiler and computer components 
are working together correctly.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.compiler import SimpleCompiler
from src.computer import Computer


def debug_print_instructions(instructions):
    """Print instructions in a readable format."""
    print("\nGenerated Instructions:")
    for i, (op, arg) in enumerate(instructions):
        if arg is not None:
            print(f"{i}: {op} {arg}")
        else:
            print(f"{i}: {op}")


def main():
    """Run a simple program to verify SimpleScript is working."""
    print("SimpleScript Sanity Check")
    print("=========================")
    
    # Create simple test program
    program = """
x = 5
print x
"""
    print(f"\nTest Program:\n{program}")
    
    # Create compiler and compile the program
    print("\nCompiling program...")
    compiler = SimpleCompiler()
    instructions = compiler.compile(program)
    
    # Display the instructions
    debug_print_instructions(instructions)
    
    # Debug output - variable mapping
    print("\nVariable Mapping:")
    for var_name, address in compiler.variables.items():
        print(f"  {var_name}: Memory location {address}")
    
    # Create a computer and run the program
    print("\nRunning program...")
    computer = Computer()
    computer.load_program(instructions)
    computer.run()
    
    # Get and print outputs
    outputs = computer.get_all_outputs()
    print("\nProgram Output:")
    if outputs:
        for i, output in enumerate(outputs):
            print(f"  Output {i+1}: {output}")
    else:
        print("  No output produced!")
    
    # Check memory at variable locations
    print("\nMemory state after execution:")
    print("  x (at address 16): ", end="")
    try:
        value = computer.memory.read(16)
        print(f"{value}")
    except IndexError:
        print("Invalid memory address")
    
    print("\nSanity check complete.")
    

if __name__ == "__main__":
    main() 